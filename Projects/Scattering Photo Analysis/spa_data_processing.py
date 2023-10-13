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



path = "C:/Users/frede/OneDrive/Skrivebord/Civil/Speciale/convergence_test/data/2023-10-10_11_ST2_Toptica_980_40mW_1450nm_TE_Focused_Exp1000000mus_gain15dB.bmp"
image = Image.open(path)


spa = SPA(True,3870) #set flag to False to tunr off plotting

image = spa.rotate_image(image,"flip")
#plt.imshow(image)

begin = time()
print(spa.analyze_image(image,400,100,20,10))
print(f"Timing analyze_image: {time()-begin:.4f} s")


#%% Right and left indent

image = Image.open(path)


spa = SPA(False,3870)

image = spa.rotate_image(image,"flip")


right_indent = list(range(100,510,10))
left_indent = list(range(200,810,10))


row = len(right_indent)
col = len(left_indent)

alpha_matrix = np.empty((row,col))

for i in range(len(right_indent)):
    for j in range(len(left_indent)):
        print(i,j)
        alpha_matrix[i,j], r_squared, alpha_upper, alpha_lower = spa.analyze_image(image, left_indent[j], right_indent[i], 20,10)
        
#%%
import seaborn as sns
from matplotlib.colors import LogNorm 
import pandas as pd


dataframe = pd.DataFrame(alpha_matrix)
dataframe.index = right_indent
dataframe.columns = left_indent
plt.figure(figsize=(10,6))

log_norm = LogNorm(vmin=10,vmax=40)
ax = sns.heatmap(dataframe, cbar_kws={'label': 'alpha (dB/cm)'},norm=log_norm)

plt.xlabel("Left indent")
plt.ylabel("Right indent")
plt.show()

#%% Moving average 

image = Image.open(path)

spa = SPA(False,3870)

image = spa.rotate_image(image,"flip")


m_bins = np.array(range(10,1010,10))






alphas = []
r_squared = []
upper_list = []
lower_list = []

for m in m_bins:
    alpha, r2, upper, lower =  spa.analyze_image(image, 400, 100, 20, m)
    alphas.append(alpha)
    upper_list.append(upper)
    lower_list.append(lower)
    r_squared.append(r2)

#%%
fig, ax1 = plt.subplots(figsize=(10,6))

plt.grid()

# Plot the first dataset on the left y-axis
ax1.plot(m_bins, alphas, color='b', label='$\\alpha$ values')
ax1.plot(m_bins,upper_list, "b--",label="confidence_interval")
ax1.plot(m_bins,lower_list, "b--")
ax1.set_xlabel('Window length value')
ax1.set_ylabel('$\\alpha$ (dB/cm)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Create a second axis (right y-axis) sharing the same x-axis
ax2 = ax1.twinx()

# Plot the second dataset on the right y-axis
ax2.plot(m_bins, r_squared, color='r', label='R\u00b2 values')
ax2.set_ylabel('R\u00b2', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Add a legend for both datasets
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines = lines1 + lines2
labels = labels1 + labels2
ax2.legend(lines, labels, loc='upper right')

# Title for the plot
#plt.title('Moving average convergence test')
#ax1.set_ylim(bottom=0)
#ax2.set_ylim(bottom=0)
# Show the plot
plt.show()


#%% 
from PIL import Image
import sys
sys.path.append("C:/Users/frede/OneDrive/Skrivebord/Civil/Speciale/PICLAB/Projects/Scattering Photo Analysis")
from SPA import SPA
import os

image_folder = "C:/Users/frede/OneDrive/Skrivebord/Civil/Speciale/"

image_encoding = ['.png', '.jpeg', '.jpg', '.bmp']

for file in os.listdir(image_folder):
    if any([x in file for x in image_encoding]):
        image_path = image_folder + file
        image = Image.open(image_path)


        spa = SPA(True,3870) #set flag to False to tunr off plotting

        image = spa.rotate_image(image,"flip")
        #plt.imshow(image)

        print(spa.analyze_image(image,400,100,20,10))
