from typing import List, Optional, Any
from freesif import open_sif    
import shutil
import numpy as np
import sys
import os
import uuid
import random
import string

def id_generator(size:int=6, chars:str=string.ascii_uppercase + string.digits) -> str:
    """Generates a random string for use as a unique identifier (id).

    Args:
        size (int, optional): Length of random string (id) to be generated. Defaults to 6.
        chars (str, optional): String from which to randomly extract characters for the id. Defaults to string.ascii_uppercase+string.digits.

    Returns:
        str: id
        
    TODO: Move to an external library
    """
    return ''.join(random.choice(chars) for _ in range(size))


def get_wadam_strings(folder:str, filename:str, wdfactors:List[float]=[1]*6, 
    pmin:List[float]=[10]*6, pmax:List[float]=[30]*6, ppeak:List[float]=[18.0]*6, 
    scaling:List[str] = ["cos2"]*6, return_arrays:bool=False, 
    return_hz_dirs:bool=False)->List[List[Any]]:
    """Reads a WADAM SIF file and returns [raoStrings, wavedriftStrings]
    which are lists of length 6, where the 6 entries relate to the degrees of 
    freedom of body motion (surge, sway, heave, roll, pitch, yaw) respectively. 
    
    Each entry is a string which is in SIMO (sys.dat) format, where e.g.
        raoStrings[0] is the surge RAO as a single string
        wavedriftStrings[3] is the mean wavedrift coefficients in roll.
        
    In addition to the strings, the user can get the coefficients as value arrays,
    and can request the frequencies (Hz) and directions (degrees)::
    
        raoStr, wdStr = get_wadam_strings(folder,filename)
        freqs, dirs, raoStr, wdStr = get_wadam_strings(folder,filename,return_hz_dirs=True)
        freqs, dirs, raoStr, wdStr, raos, wds = get_wadam_strings(folder,filename,return_hz_dirs=False)      

    Optionally the user can scale the wave drift coefficients using a scaling function.
    The scaling function is specified by the "scaling" argument and can take the values:
    
        "constant": constant scaling
        "linear":   linear scaling. At wave periods <= pmin and >= pmax the scaling factor takes the value of 1.0
                    i.e. no scaling. At wave period ppeak, where pmin < ppeak < pmax, the scaling factor takes a
                    value specified by the corresponding entry in the wdfactors list for the response.
        "cos2" :    Similar to linear except the scaling function between pmin/pmax and ppeak is cosine-squared
        "gauss":    Similar to cos2 except the scaling function is Guassian and the scaling values at pmin/pmin
                    10% the value specified by the wdfactor array

    Args:
        folder (str): folder of the SIF file
        filename (str): filename of the SIF file
        wdfactors (List[float], optional): Maximum value of scaling function to apply at ppeak. Defaults to [1]*6.
        pmin (List[float], optional): Minimum period for scaling. Defaults to [10]*6.
        pmax (List[float], optional): Maximum period for scaling. Defaults to [30]*6.
        ppeak (List[float], optional): Peak period for scaling. Defaults to [18.0]*6.
        scaling (List[str], optional): Type of scaling. Defaults to ["cos2"]*6.
        return_arrays (bool, optional): Set true to return values of raos and wavedrift coefficients. Defaults to False.
        return_hz_dirs (bool, optional): Set True to return wave frequencies (Hz) and directions. Defaults to False.

    Returns:
        List[List[Any]]: See docstring
    """
    # Read the mean wave drift coefficients and raos on the SIF file
    id = id_generator()
    filename_tmp = "r" + id + filename[:-4].replace(".","_") + '.SIF'
    shutil.copyfile(f"{folder}/{filename}", filename_tmp)
    # Open the sif and read the data
    sif = open_sif(filename_tmp)
    periods = sif.get_periods()
    directions = sif.get_directions()
    raos = sif.get_motion_raos()
    pressure = sif.get_meandrift()
    momentum = sif.get_horiz_meandrift()
    raos = raos[:, :, ::-1] # flip the last field
    momentum = momentum[:,:,::-1]
    pressure = pressure[:,:,::-1]
    periods = periods[::-1] # for consistency (superfluous for function)
    wavedrift = pressure
    wavedrift[0] = momentum[0]
    wavedrift[1] = momentum[1]
    wavedrift[5] = momentum[2]

    # Establish some blending functions to scale the wavedrifts
    alpha = np.zeros((6,len(periods))) # storage for blending function
    for i in range(0, 6):
        print(i, scaling[i])
        ix_lower = (periods >= pmin[i]) & (periods <= ppeak[i]) 
        ix_upper = (periods <= pmax[i]) & (periods >= ppeak[i])
        coord_lower = 1-(ppeak[i]-periods[ix_lower])/(ppeak[i] - pmin[i])
        coord_upper = 1-(periods[ix_upper]-ppeak[i])/(pmax[i] - ppeak[i])
        if scaling[i] == "constant":
            alpha[i,:] = 1
        if scaling[i] == "linear":
            alpha[i,ix_lower] = coord_lower
            alpha[i,ix_upper] = coord_upper
        if scaling[i] == "cos2":
            alpha[i,ix_lower] = (0.5*(1 - np.cos(coord_lower*np.pi)))**2
            alpha[i,ix_upper] = (0.5*(1 - np.cos(coord_upper*np.pi)))**2
        if scaling[i] == "gauss":
            fwtm_lower = 2*(ppeak[i]-pmin[i]) # full width at tenth of the maximum
            fwtm_upper = 2*(pmax[i]-ppeak[i]) # full width at tenth of the maximum
            c_lower = fwtm_lower/4.29193
            c_upper = fwtm_upper/4.29193
            alpha_lower = np.exp(-(periods-ppeak[i])**2/2/c_lower**2)
            alpha_upper = np.exp(-(periods-ppeak[i])**2/2/c_upper**2)
            alpha[i] = np.where(periods < ppeak[i], alpha_lower, alpha_upper)
        if scaling[i] == "exwave":
            # TODO: requires hs snd other arguments, disallow for now
            hs = 12.0
            D = 96
            U = 0.73 # would need to enter
            G = 10 # s
            Cp = 0.25
            w = 2*np.pi/periods
            k = w**2/9.80665
            p = np.exp(-1.25*(k*D)**2)
            Dsum = D
            B = k*p*Dsum
            fd2 = B*(G*U +  hs)
            alpha[i] = (1+Cp*U)   

    # if the factor is 1.0 want no change. If factor 1.1 we want some change
    wavedrift_original = wavedrift*1.0 # make a copy for checking (then remove!)
    wavedrift_peak = wavedrift*1.0 # make storage for peak scaling
    for idof in range(len(raos)):
        for idir in range(len(directions)):
            if scaling[idof] == "exwave":
                #wavedrift[idof,idir] = wavedrift_original[idof,idir] + 1.0*B*(G*U +  hs)*1000
                #wavedrift[idof,idir] = wavedrift_original[idof,idir] + 1.0*B*(26.4)*1000
                wavedrift[idof,idir] = wavedrift_original[idof,idir] + B*1000*wdfactors[idof]
            else:
                wavedrift_peak[idof,idir] = wavedrift_original[idof,idir]*wdfactors[idof]
                wavedrift[idof,idir] = alpha[idof]*wavedrift_peak[idof,idir] + (1-alpha[idof])*wavedrift_original[idof,idir]

    # Establish storage
    raoStrings = [[],[],[],[],[],[]]
    wavedriftStrings = [[],[],[],[],[],[]]
    for idof in range(len(raos)):
        for idir in range(len(directions)):
            for ifreq in range(len(periods)):
                h = raos[idof,idir,ifreq]
                a, p = np.abs(h), np.angle(h)*180/np.pi
                v = wavedrift[idof,idir,ifreq] / 1000 # convert from N => kN 
                raoStrings[idof].append(f"{idir+1:5d} {ifreq+1:5d} {a:20.9e} {p:20.9e}") 
                wavedriftStrings[idof].append(f"{idir+1:5d} {ifreq+1:5d} {v:20.9e}") 

    sif.close()
    os.remove(filename_tmp)
    dataset = [1/periods, directions] if return_hz_dirs else []
    dataset += [raoStrings, wavedriftStrings]
    dataset += [raos, wavedrift] if return_arrays else []
    return dataset



def read_SIF_rao(folder:str, filename:str, wadir:float, 
                 mapping_index:List[int]=[0,1,2,3,4,5],
                 mapping_sign:List[int]=[1,1,1,1,1,1]):
    """Returns the RAOs on the SIF file for a given wave direction.

    Args:
        folder (str): folder containing the SIF file
        filename (str): filename of the SIF file
        wadir (float): wave direction of interest
        mapping_index (List[int], optional): Maps the degrees of freedom to another order. Defaults to [1,0,2,4,3,5].

    Returns:
        [type]: [description]
    """
    
    # Need to replace prefix dots (.) due to REGEX method in freesif
    id = id_generator()
    filename_tmp =  "r" + id + filename[:-4].replace(".","_") + '.SIF'
    shutil.copyfile(f"{folder}/{filename}", filename_tmp)
    sif = open_sif(filename_tmp)
    periods = sif.get_periods()
    directions = sif.get_directions()
    raos = sif.get_motion_raos()
    sif.close()
    os.remove(filename_tmp)
    ix = np.nonzero(wadir==directions)
    factor = [1,1,1,180./np.pi,180./np.pi,180./np.pi]
    # Correcting for the chosen coordinate system :/
    return 1./periods[::-1], [mapping_sign[dof]*factor[dof]*np.squeeze(raos[dof, ix, ::-1]) for dof in mapping_index]