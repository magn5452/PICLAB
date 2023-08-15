# -*- coding: utf-8 -*-
"""
ANDO Test
Created on Mon Feb 14 14:37:09 2022

@author: Peter Tønning
"""

import numpy as np
import time
import Python_lib.ANDO_OSA as OSA
import matplotlib.pyplot as plt
import ctypes
from ctypes import*
import os
import math  


ANDO= OSA.ANDO_OSA()
ANDO.SetupOSA(948.5,1,-60,0.05,1)
# ANDO.ContinousSweep()
# ANDO.stop()

# 

ANDO.SingleSweep()
[Power, WL]=ANDO.GetSpectrum()


fname='SFG_1612.txt'
#header = fname+" ; 1st column: Wavelength [nm], 2nd column: power [dBm]"
#FirstAxis=np.asarray(WL)
#SecondAxis=np.asarray(Power)
#np.savetxt(fname, np.transpose([FirstAxis,SecondAxis]), delimiter=',',header=header)

plt.plot(WL,Power)
plt.xlabel('SHG wavelength [nm]')
plt.ylabel('Output [dBm]')
plt.savefig('OSA_trace.pdf')
plt.show()