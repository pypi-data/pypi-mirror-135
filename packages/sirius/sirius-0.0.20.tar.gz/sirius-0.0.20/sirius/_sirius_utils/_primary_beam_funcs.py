#   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import numpy as np
from sirius_data._constants import c
import scipy.constants
from scipy.special import j1, jn
from numba import jit
import numba_scipy.special
import numba

# The twiddle factor is needed to improve agreement between CASA PBMATH airy disk and SiRIUS. 
# This arrises because CASA makes use of truncated constants. The twiddle factor 0.9998277835716939 is very close to 1. 
# Even with the twiddle there will not be machine precission agreement, because CASA calculates a 1D PB at 1 GHz for 10000 points and then frequency scales and interpolates to desired value.
# CASA also discards the fractional part when calculating the index (use Int instead of (int(np.floor(r/r_inc + 0.5)).
# See PBMath1D.cc Complex version ImageInterface<Complex>&PBMath1D::apply
# SkyComponent&PBMath1D::apply makes a small angle approximation while ImageInterface<Complex>&PBMath1D::apply does not. We have decided to not make the small angle approximation.
casa_twiddle = (180*7.016*c)/((np.pi**2)*(10**9)*1.566*24.5) # 0.9998277835716939

@jit(nopython=True,nogil=True)
def _casa_airy_pb(l,m,freq_chan,dish_diameter, blockage_diameter, ipower, max_rad_1GHz, n_sample=10000):
    """
    Airy disk function to model the antenna response, that has been adapted to match the PBMATH class in CASA. CASA PBMath does not directly calculate the airy function. It generates 10000 points at 1 GHz and then scales and samples from that when apply_pb/vp is called. As part of the scaling someone truncated some factors, so to get a python function that matches CASA a twiddle factor: casa_twiddle = (1807.016c)/((np.pi**2)(10**9)*1.56624.5)=0.9998277835716939 is added. It also does integer rounding. This function should agree with CASA up to 7 significant figures.
    
    Parameters
    ----------
    l: float, radians
        Coordinate of a point on the image plane (the synthesis projected ascension and declination).
    m: float, radians
        Coordinate of a point on the image plane (the synthesis projected ascension and declination).
    freq_chan: float, Hz
        Frequency.
    dish_diameter: float, meters
        The diameter of the dish.
    blockage_diameter: float, meters
        The central blockage of the dish.
    ipower: int
        ipower = 1 single dish response.
        ipower = 2 baseline response for identical dishes.
    max_rad_1GHz: float, radians
        The max radius from which to sample scaled to 1 GHz.
        This value can be found in sirius_data.dish_models_1d.airy_disk.
        For example the Alma dish model (sirius_data.dish_models_1d.airy_disk import alma)
        is alma = {'pb_func': 'airy', 'dish_diam': 10.7, 'blockage_diam': 0.75, 'max_rad_1GHz': 0.03113667385557884}.
    n_sample=10000
        The sampling used in CASA for PB math.
    Returns
    -------
    val : float
        The dish response.
    """
    r_max = max_rad_1GHz/(freq_chan/10**9)
    k = (2*np.pi*freq_chan)/c
    aperture = dish_diameter/2

    if n_sample is not None:
        r = np.sqrt(l**2 + m**2)
        r_inc = ((r_max)/(n_sample-1))
        r = (int(r/r_inc)*r_inc)*aperture*k #Int rounding instead of r = (int(np.floor(r/r_inc + 0.5))*r_inc)*aperture*k
        r = r*casa_twiddle
    else:
        r = np.arcsin(np.sqrt(l**2 + m**2)*k*aperture)
        
    if (r != 0):
        if blockage_diameter==0.0:
            return (2.0*j1(r)/r)**ipower
        else:
            area_ratio = (dish_diameter/blockage_diameter)**2
            length_ratio = (dish_diameter/blockage_diameter)
            return ((area_ratio * 2.0 * j1(r)/r   - 2.0 * j1(r * length_ratio)/(r * length_ratio) )/(area_ratio - 1.0))**ipower
    else:
        return 1


#@jit(nopython=True,cache=True,nogil=True)
@jit(nopython=True,nogil=True)
def _3d_casa_airy_pb(l,m,freq_chan,dish_diameter, blockage_diameter, ipower, max_rad_1GHz, n_sample=10000):
    """
    3-dimensional Airy disk function to model the antenna response, that has been adapted to match the PBMATH class in CASA. CASA PBMath does not directly calculate the airy function. It generates 10000 points at 1 GHz and then scales and samples from that when apply_pb/vp is called. As part of the scaling someone truncated some factors, so to get a python function that matches CASA a twiddle factor: casa_twiddle = (1807.016c)/((np.pi**2)(10**9)*1.56624.5)=0.9998277835716939 is added. It also does integer rounding. This function should agree with CASA up to 7 significant figures.
    Parameters
    ----------
    l: float np.array, n_pix_x, radians
        Coordinate of a point on the image plane (the synthesis projected ascension and declination).
    m: float np.array, n_pix_y, radians
        Coordinate of a point on the image plane (the synthesis projected ascension and declination).
    freq_chan: float np.float, n_chan, Hz
        Frequency.
    dish_diameter: float, meters
        The diameter of the dish.
    blockage_diameter: float, meters
        The central blockage of the dish.
    ipower: int
        ipower = 1 single dish response.
        ipower = 2 baseline response for identical dishes.
    max_rad_1GHz: float, radians
        The max radius from which to sample scaled to 1 GHz.
        This value can be found in sirius_data.dish_models_1d.airy_disk.
        For example the Alma dish model (sirius_data.dish_models_1d.airy_disk import alma)
        is alma = {'pb_func': 'airy', 'dish_diam': 10.7, 'blockage_diam': 0.75, 'max_rad_1GHz': 0.03113667385557884}.
    n_sample=10000
        The sampling used in CASA for PB math.
    Returns
    -------
    beam : float np.array, [n_chan,n_pix_x,n_pix_y]
        The dish response.
    """
    beam = np.zeros(freq_chan.shape + l.shape + m.shape,dtype=numba.float64)
    
    for i_freq,freq in enumerate(freq_chan):
            r_max = max_rad_1GHz/(freq/10**9)
            k = (2*np.pi*freq)/c
            aperture = dish_diameter/2

            for i_l, l_val in enumerate(l):
                for i_m, m_val in enumerate(m):
                    if n_sample is not None:
                        r = np.sqrt(l_val**2 + m_val**2)
                        r_inc = ((r_max)/(n_sample-1))
                        r = (int(r/r_inc)*r_inc)*aperture*k #Int rounding instead of r = (int(np.floor(r/r_inc + 0.5))*r_inc)*aperture*k
                        r = r*casa_twiddle
                    else:
                        r = np.sqrt(l_val**2 + m_val**2)*k*aperture
                        
                    if (r != 0):
                        if blockage_diameter==0.0:
                            beam[i_freq,i_l,i_m] = (2.0*j1(r)/r)**ipower
                        else:
                            area_ratio = (dish_diameter/blockage_diameter)**2
                            length_ratio = (dish_diameter/blockage_diameter)
                            beam[i_freq,i_l,i_m] = ((area_ratio * 2.0 * j1(r)/r   - 2.0 * j1(r * length_ratio)/(r * length_ratio) )/(area_ratio - 1.0))**ipower
                    else:
                        beam[i_freq,i_l,i_m] = 1
    return beam
        

#@jit(nopython=True,cache=True,nogil=True)
@jit(nopython=True,nogil=True)
def _airy_pb(l,m,freq_chan,dish_diameter, blockage_diameter, ipower):
    """
    Airy disk function to model the antenna response.
    
    Parameters
    ----------
    l: float, radians
        Coordinate of a point on the image plane (the synthesis projected ascension and declination).
    m: float, radians
        Coordinate of a point on the image plane (the synthesis projected ascension and declination).
    freq_chan: float, Hz
        Frequency.
    dish_diameter: float, meters
        The diameter of the dish.
    blockage_diameter: float, meters
        The central blockage of the dish.
    ipower: int
        ipower = 1 single dish response.
        ipower = 2 baseline response for identical dishes.
    Returns
    -------
    val : float
        The dish response.
    """

    k = (2*np.pi*freq_chan)/c
    aperture = dish_diameter/2
    r = np.sqrt(l**2 + m**2)*k*aperture
        
    if (r != 0):
        if blockage_diameter==0.0:
            return (2.0*j1(r)/r)**ipower
        else:
            e = blockage_diameter/dish_diameter
            return (( 2.0 * j1(r)/r   - 2.0 * e * j1(r * e)/r )/(1.0 - e**2))**ipower
            #Changed r_grid to r ^^^
    else:
        return 1
        
@jit(nopython=True,nogil=True)
def _3d_airy_pb(l,m,freq_chan,dish_diameter, blockage_diameter, ipower, max_rad_1GHz, n_sample=10000):
    """
    3-dimensional Airy disk function to model the antenna response.
    
    Parameters
    ----------
    l: float np.array, n_pix_x, radians
        Coordinate of a point on the image plane (the synthesis projected ascension and declination).
    m: float np.array, n_pix_y, radians
        Coordinate of a point on the image plane (the synthesis projected ascension and declination).
    freq_chan: float np.float, n_chan, Hz
        Frequency.
    dish_diameter: float, meters
        The diameter of the dish.
    blockage_diameter: float, meters
        The central blockage of the dish.
    ipower: int
        ipower = 1 single dish response.
        ipower = 2 baseline response for identical dishes.
    max_rad_1GHz: float, radians
        The max radius from which to sample scaled to 1 GHz.
        This value can be found in sirius_data.dish_models_1d.airy_disk.
        For example the Alma dish model (sirius_data.dish_models_1d.airy_disk import alma)
        is alma = {'pb_func': 'airy', 'dish_diam': 10.7, 'blockage_diam': 0.75, 'max_rad_1GHz': 0.03113667385557884}.
    n_sample=10000
        The sampling used in CASA for PB math.
    Returns
    -------
    beam : float np.array, [n_chan,n_pix_x,n_pix_y]
        The dish response.
    """
    beam = np.zeros(freq_chan.shape + l.shape + m.shape,dtype=numba.float64)
    
    for i_freq,freq in enumerate(freq_chan):
            r_max = max_rad_1GHz/(freq/10**9)
            k = (2*np.pi*freq)/c
            aperture = dish_diameter/2

            for i_l, l_val in enumerate(l):
                for i_m, m_val in enumerate(m):
                    k = (2*np.pi*freq_chan)/c
                    aperture = dish_diameter/2
                    r = np.sqrt(l_val**2 + m_val**2)*k*aperture
                        
                    if (r != 0):
                        if blockage_diameter==0.0:
                            beam[i_freq,i_l,i_m] = (2.0*j1(r)/r)**ipower
                        else:
                            e = blockage_diameter/dish_diameter
                            beam[i_freq,i_l,i_m] = (( 2.0 * j1(r)/r   - 2.0 * e * j1(r * e)/r )/(1.0 - e**2))**ipower
                    else:
                        beam[i_freq,i_l,i_m] = 1
    return beam
    
    
##############################################################################################################
#Non-jitted version:
def _casa_airy_pb_njit(lmn,freq_chan,pb_parms):
    #print('lmn is',lmn)
    
    if (lmn[0] != 0) or (lmn[1] != 0):
        dish_diameter = pb_parms['dish_diameter']
        blockage_diameter = pb_parms['blockage_diameter']
        ipower = pb_parms['ipower']
        
        k = (2*np.pi*freq_chan)/c
        
        aperture = dish_diameter/2
        r = np.sqrt(lmn[0]**2 + lmn[1]**2)*k*aperture
        
        if blockage_diameter==0.0:
            return (2.0*jn(1,r)/r)**ipower
        else:
            area_ratio = (dish_diameter/blockage_diameter)**2
            length_ratio = (dish_diameter/blockage_diameter)
            return ((area_ratio * 2.0 * jn(1,r)/r   - 2.0 * jn(1, r * length_ratio)/(r * length_ratio) )/(area_ratio - 1.0))**ipower
    else:
        return 1


def _airy_pb_njit(lmn,freq_chan,pb_parms):
    #print('lmn is',lmn)
    
    if (lmn[0] != 0) or (lmn[1] != 0):
        dish_diameter = pb_parms['dish_diameter']
        blockage_diameter = pb_parms['blockage_diameter']
        ipower = pb_parms['ipower']
        
        k = (2*np.pi*freq_chan)/c
        
        aperture = dish_diameter/2
        r = np.sqrt(lmn[0]**2 + lmn[1]**2)*k*aperture
        
        if blockage_diameter==0.0:
            return (2.0*jn(1,r)/r)**ipower
        else:
            e = blockage_diameter/dish_diameter
            return (( 2.0 * jn(1,r)/r   - 2.0 * e * jn(1, r * e)/r )/(1.0 - e**2))**ipower
    else:
        return 1
