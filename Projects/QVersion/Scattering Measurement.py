# -*- coding: utf-8 -*-
"""
Created on Mon May  9 10:03:03 2022

@author: Peter Tønning, Kevin Bach Gravesen
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import glob
import matplotlib.image as mpimg
from PIL import Image
from scipy.optimize import curve_fit

plt.close('all')

def PrintFiles(path,extension):
    print(path)
    filepaths=glob.glob(path+'//*.'+extension)
    print(filepaths)
    filenames=[None]*len(filepaths)
    for n in range(len(filepaths)):
        filenames[n]=filepaths[n][len(path):]
    for (i,item) in enumerate(filenames,start=0):
        print(i, ': '+item)
    return filenames


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def smooth_data_convolve_my_average(arr, span):
    re = np.convolve(arr, np.ones(span * 2 + 1) / (span * 2 + 1), mode="same")

    # The "my_average" part: shrinks the averaging window on the side that
    # reaches beyond the data, keeps the other side the same size as given
    # by "span"
    re[0] = np.average(arr[:span])
    for i in range(1, span + 1):
        re[i] = np.average(arr[:i + span])
        re[-i] = np.average(arr[-i - span:])
    return re

def gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


def func(x, a, b):
    return a * np.exp(-b * (x))

def funcc(x, a, b, c):
    ybackground = 0
    return a * np.exp(-b * (x)) + c*0 + ybackground

def find_closest(xs, x):
    """Return the index of the value closest to x in array xs."""
    diff = np.abs(xs - x)
    idx = diff.argmin()
    median_indices = np.where(diff == diff.min())[0]
    if len(median_indices) > 1:
        idx = int(np.median(median_indices))
    return idx

## Path the pictures are at
#current_file_path = sys.argv[0].replace('\\','/').split("propagation_loss")[0]
#path = '../'+ current_file_path + '/Pictures/'
path = 'Pictures/'
print('Files:')

## The picture to analyse (indexed at 0)
pic_index=3

Pictures=PrintFiles(path,'png')
org_img_image = Image.open(path + Pictures[pic_index])
org_img = np.asarray(org_img_image)
height = np.shape(org_img)[0]
width = np.shape(org_img)[1]
print(height,width)

## Camera Specification
window_num_pixel_height = 2048
window_num_pixel_width = 2448

## Distance Calibration
calibration_num_pixel_height = 1030
calibration_num_pixel_width = 2047
calibration_mum_height = 2476
calibration_mum_width = 4866

## Change these to cut out the laser from the left and how far you want to go to the right
left_indent = 250
right_indent = width - 2100
top_indent = 0
bottom_indent = height - top_indent

cut_img_image = org_img_image.crop((left_indent, top_indent, width-right_indent, bottom_indent))
cut_img = np.asarray(cut_img_image)
# plt.imshow(cut_img)

## Make guassian fits to find the maximum at the left and right side,
## to find the angle which the image needs to be rotated by.
left_gauss_p0 = [0,255,1115,100]
right_gauss_p0 = [0,255,1115,100]
poptleft, pcov = curve_fit(gauss, range(height), cut_img[:,0,2], p0=left_gauss_p0, maxfev=10000)
poptright, pcov = curve_fit(gauss, range(height), cut_img[:,width-left_indent-right_indent-1,2], p0=right_gauss_p0, maxfev=10000)
plt.plot(range(height),gauss(range(height), *poptleft), label='Gaussian fit')
plt.plot(range(height),cut_img[:,0,2], label='Data')
plt.legend()
plt.title('Left hand side blue values')
plt.figure()
plt.title('Right hand side blue values')
plt.plot(range(height),gauss(range(height), *poptright), label='Gaussian fit')
plt.plot(range(height),cut_img[:,width-left_indent-right_indent-1,2], label='Data')
plt.legend()
left_max_index = find_closest(cut_img[:,0,2], poptleft[2])
right_max_index = find_closest(cut_img[:,width-left_indent-right_indent-1,2], poptright[2])

## If you want to override the gaussian fits
left_max_index = 590 # Override
right_max_index = 1580 # Override

print(f'left max index = {left_max_index}')
print(f'right max index = {right_max_index}')
slope = (right_max_index-left_max_index)/(width)
#angle = np.degrees(np.arctan(slope))
angle = 0

## Rotate picture and plot it with the upper and lower limit
print(f'angle = {angle}')
img_rotated_image = cut_img_image.rotate(angle)
img_rotated = np.asarray(img_rotated_image)
plt.figure()
plt.imshow(cut_img)
plt.title(Pictures[pic_index] + ' before rotation')


plt.figure()
plt.imshow(img_rotated/np.max(img_rotated)*255)
upper=left_max_index+10
lower=left_max_index-10
plt.plot(range(len(img_rotated[0,:,2])),np.ones(len(img_rotated[0,:,2]))*upper,'r-')
plt.plot(range(len(img_rotated[0,:,2])),np.ones(len(img_rotated[0,:,2]))*lower,'r-')
plt.title(Pictures[pic_index] + " after rotation")

plt.figure()

# length_pixel=range(len(img_rotated[0,left_indent:(width-right_indent),2]))
length_pixel=range(len(img_rotated[0,:,2]))
length_um=np.asarray(length_pixel)*(calibration_mum_width/calibration_num_pixel_width) #7229 um measured on the GDS, 2445 is the pixel width of the sensor (Both numbers inherent of the sensor and lens)
Decay=np.sum(img_rotated[lower:upper,:,2],axis=0)
DecaySmooth=smooth_data_convolve_my_average(Decay,50)
plt.plot(length_um,Decay, label="Raw data")
plt.plot(length_um,DecaySmooth, label="Smothed data")
popt, pcov = curve_fit(funcc, length_um, DecaySmooth, p0=[5000,0.00000001, 200],maxfev=10000)
# popt, pcov = curve_fit(func, length_um, DecaySmooth, p0=[5000,0.00000001],maxfev=10000)

print(pic_index)
print(Pictures[pic_index])
print(f'a={popt[0]}, b={popt[1]}')
print(f"alpha = {-popt[1]*1e4} 1/cm")
print(f'alpha_dB = {-10*np.log10(np.exp(-popt[1]*1e4))} dB/cm')
print(f'Length over measurement = {length_um[-1]} um')
plt.plot(length_um, funcc(length_um, *popt), 'r-', label="Fitted Curve")
# plt.plot(length_um, func(length_um, *popt), 'r-', label="Fitted Curve")
plt.plot(length_um, np.mean(img_rotated[lower:upper,:,2],axis=0), 'k-', label="Max reading")

plt.legend()
plt.xlabel('Length [um]')
plt.ylabel('Sum of blue intensity')
plt.title(Pictures[pic_index])
plt.show()