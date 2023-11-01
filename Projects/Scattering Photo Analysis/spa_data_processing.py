# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 11:04:10 2023

@author: frede
"""

from PIL import Image

from time import time
import sys
sys.path.append("C:/Users/frede/OneDrive/Skrivebord/Civil/Speciale/PICLAB/Projects/Scattering Photo Analysis")
from SPA import SPA
import numpy as np


path = "C:/Users/frede/Downloads/2023-10-10_11_ST2_Toptica_980_80mW_1450nm_TE_Focused_Exp1000000mus_gain23.9dB.bmp"
path = "C:/Users/frede/Downloads/2023-09-07_16_10_03_312_chip14_waveguide4_straight.png"
image = Image.open(path)


spa = SPA(True,3870) #set flag to False to tunr off plotting

image = spa.rotate_image(image,"left")
#plt.imshow(image)

begin = time()

left_indent = 0
right_indent = 0
rows = 20
bins = 10
sum_width = 20

print(spa.analyze_image(image,left_indent,right_indent,rows,bins,sum_width))
#spa.plot_histogram(np.array(image))
print(f"Timing analyze_image: {time()-begin:.4f} s")


#%%
from PIL import Image

from time import time
import sys
sys.path.append("C:/Users/frede/OneDrive/Skrivebord/Civil/Speciale/PICLAB/Projects/Scattering Photo Analysis")
from SPA import SPA
import numpy as np
import matplotlib.pyplot as plt

path = "C:/Users/frede/Downloads/2023-10-10_11_ST2_Toptica_980_80mW_1450nm_TE_Focused_Exp1000000mus_gain23.9dB.bmp"
image = Image.open(path)


spa = SPA(False,3870) #set flag to False to tunr off plotting

image = spa.rotate_image(image,"flip")

left_indent = 100
#right_indent = 150
rows = 20
bins = 10
sum_width = 20
alphas = []
r_values = []
right_indent = range(50, 1500,10)
for indent in right_indent:
    alpha, r_squared, alpha_upper, alpha_lower = spa.analyze_image(image,left_indent,indent,rows,bins,sum_width)
    alphas.append(alpha)
    r_values.append(r_squared)

#%%
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

ax1.plot(right_indent, alphas,"b-",label="Alpha")
ax2.plot(right_indent, r_values, "r-",label="R squared");

ax1.set_xlabel("Right indent")
ax1.set_ylabel("Alpha (dB/cm)")
ax2.set_ylabel("R squared")
ax2.legend(loc=0)
ax1.legend(loc=1)

#%% 
from PIL import Image
import sys
sys.path.append("C:/Users/frede/OneDrive/Skrivebord/Civil/Speciale/PICLAB/Projects/Scattering Photo Analysis") #Path to repository with SPA.py and Lab_cam.py
from SPA import SPA
import os


chip_length = 3870
spa = SPA(True,chip_length) #set flag to False to turn off plotting, 

left_indent = 500
right_indent = 400
rows = 20 # number of rows used to mean pixels
bins = 10 # number of sections to split up signal for IQR outlier removal
sum_width = 20 #used when plotting moving average



path = 'Pictures/'
f_ending = '.bmp'
contains = 'GST3'
image_filter = '1933nm'

filenames = []
for file in os.listdir(path):
        if file.endswith(f_ending):
            if contains in file:
                if image_filter in file:
                    filenames.append(file)
print(len(filenames))

filenames.sort()

for file in filenames:
    original_image = Image.open(path + file)
    original_image = spa.rotate_image(original_image,"flip") # 
    alpha_dB, r_squared, alpha_upper, alpha_lower = spa.analyze_image(original_image,left_indent,right_indent,rows,bins,sum_width)

