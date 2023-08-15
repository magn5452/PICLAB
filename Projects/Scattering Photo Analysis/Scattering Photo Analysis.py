# -*- coding: utf-8 -*-
"""
Created on Mon May  9 10:03:03 2022

@author: Peter Tønning, Kevin Bach Gravesen, Magnus Linnet Madsen
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit
from functions import *

# Path the pictures are at
path = 'Pictures/'

# Load Image
picture_index = 3
pictures = print_files(path, 'png')
original_image = Image.open(path + pictures[picture_index])
original_image = original_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)  # flip image
original_image_array = np.asarray(original_image)

# Size of Image
window_num_pixel_height = np.shape(original_image_array)[0]  # 2048
window_num_pixel_width = np.shape(original_image_array)[1]  # 2448

# Distance Calibration
calibration_num_pixel_height = 1030
calibration_num_pixel_width = 2047
calibration_mum_height = 2476
calibration_mum_width = 4866

# Detect the pixel of insertion
insertion_height_index, insertion_width_index = insertion_detection(original_image)

# Change these to cut out the laser from the left and how far you want to go to the right
left_indent = insertion_width_index + 550
right_indent = window_num_pixel_width
top_indent = insertion_height_index - 70
bottom_indent = insertion_height_index + 70
cropped_image = original_image.crop((left_indent, top_indent, right_indent, bottom_indent))
cropped_image_array = np.asarray(cropped_image)

# Plot Cropped Image
plt.figure()
plt.imshow(cropped_image_array)
plt.title(' after crop')

# Find the waveguide
left_right_separation = 200
left_max_index, right_max_index = find_left_right_index_max(cropped_image_array[:,:,2], left_right_separation)


# Rotate picture and plot it with the upper and lower limit
slope = (right_max_index - left_max_index) / (left_right_separation)
angle = np.degrees(np.arctan(slope))
rotated_image = cropped_image.rotate(angle)
rotated_image_array = np.asarray(rotated_image)
plt.figure()
plt.imshow(cropped_image_array)
plt.title(pictures[picture_index] + ' before rotation')

# Plot rotated picture
plt.figure()
plt.imshow(rotated_image_array)
upper = left_max_index + 10
lower = left_max_index - 10
cropped_array = rotated_image_array[lower:upper, :, 2]
plt.plot(range(len(rotated_image_array[0, :, 2])), np.ones(len(rotated_image_array[0, :, 2])) * upper, 'r-')
plt.plot(range(len(rotated_image_array[0, :, 2])), np.ones(len(rotated_image_array[0, :, 2])) * lower, 'r-')
plt.title(pictures[picture_index] + " after rotation")




# Remove Saturated Points
max_array = np.max(cropped_array, axis=0)
saturation_index_list = np.where(max_array != 255)[0]

# Fit Exponential Curve
length_pixel = saturation_index_list
length_um_array = np.asarray(length_pixel) * (calibration_mum_width / calibration_num_pixel_width)  # 7229 um measured on the GDS, 2445 is the pixel width of the sensor (Both numbers inherent of the sensor and lens)
decay = np.mean(rotated_image_array[lower:upper, saturation_index_list, 2], axis=0)
popt, pcov = curve_fit(exponential_function, length_um_array, decay, p0=[25, 0.0006], maxfev=1000)

# Plot Data and Fit
plt.figure()
plt.plot(length_um_array, np.max(rotated_image_array[lower:upper, saturation_index_list, 2], axis=0), 'k-', label="Max reading")
plt.plot(length_um_array, decay, label="Raw data")
plt.plot(length_um_array, exponential_function(length_um_array, *popt), 'r-', label="Fitted Curve")
plt.legend()
plt.xlabel('Length [um]')
plt.ylabel('Mean of blue intensity')
plt.title(pictures[picture_index])


print(picture_index)
print(pictures[picture_index])
print(f'a={popt[0]}, b={popt[1]}')
print(f"alpha = {-popt[1] * 1e4} 1/cm")
print(f'alpha_dB = {-10 * np.log10(np.exp(-popt[1] * 1e4))} dB/cm')
print(f'Length over measurement = {length_um_array[-1]} um')

plt.show()


