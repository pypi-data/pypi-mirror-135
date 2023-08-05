import numpy as np

def interpc(x, xp, fp):
  """ Alternative to numpy interp for complex numbers where the abs and phase are interpolated"""
  return np.interp(x, xp, np.abs(fp))*np.exp(1j*np.interp(x, xp, np.abs(fp)))