# -*- coding: utf-8 -*-
"""
Created on Mon May  9 10:03:03 2022

@author: Peter Tønning, Kevin Bach Gravesen, Magnus Linnet Madsen
"""
import numpy
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit, least_squares
from scipy.signal import find_peaks

from functions import *
import scipy.signal

# Path the pictures are at
path = 'Pictures/'

# Load Image
picture_index = 135
pictures = print_files(path, 'bmp')
original_image = Image.open(path + pictures[picture_index])
original_image = original_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)  # flip image and manually rotate
original_image_array = np.asarray(original_image)

# Size of Image
window_num_pixel_height = np.shape(original_image_array)[0]  # 2048
window_num_pixel_width = np.shape(original_image_array)[1]  # 2448

# Distance Calibration
chip_length_mum = 3870 # mu m

# Chip Detection
#find_chip(original_image)

# Detect the pixel of input
input_width_index, input_height_index, output_width_index, output_height_index = insertion_detection(original_image.copy())
print("input_width_index: ", input_width_index, " input_height_index ", input_height_index, " output_width_index: ", output_width_index, "output_height_index: ", output_height_index)


# Change these to cut out the laser from the left and how far you want to go to the right
left_indent = input_width_index + 0
right_indent = output_width_index - 100
top_indent = input_height_index - 100
bottom_indent = input_height_index + 100
cropped_image = original_image.crop((left_indent, top_indent, right_indent, bottom_indent))
cropped_image_array = np.asarray(cropped_image)

distance_input_output_pixel = np.sqrt((input_height_index - output_height_index)**2 + (input_width_index - output_width_index)**2)

# Length Calibration
mum_pr_pixel = chip_length_mum / distance_input_output_pixel

# Find the waveguide
left_index_guess = 300
separation = 50
number_of_points = 15
angle, angle_params, x_max_index_array, y_max_index_array = find_waveguide_angle(cropped_image_array[:, :, 2], left_index_guess, separation, number_of_points)

# Rotate picture and plot it with the upper and lower limit
print("Angle: ", angle)
left_indent = left_indent
right_indent = right_indent
top_indent = top_indent
bottom_indent = bottom_indent
rotated_image = original_image.rotate(-angle, center=(left_indent, int(angle_params[1]) + top_indent)).crop((left_indent, top_indent, right_indent, bottom_indent))
rotated_image_array = np.asarray(rotated_image)

interval = 10
upper = int(angle_params[1] + interval/2)
lower = int(angle_params[1] - interval/2)
cropped_array = rotated_image_array[lower:upper, :, 2]
shape_cropped_array = np.shape(cropped_array)

x_mu_array = np.arange(np.shape(rotated_image_array)[1]) * mum_pr_pixel
y_mu_array = np.arange(np.shape(rotated_image_array)[0]) * mum_pr_pixel


plt.figure()
plt.imshow(get_intensity_array(cropped_image_array.copy()), cmap="jet", vmin=0, vmax=10, interpolation='spline16', extent=[x_mu_array[0], x_mu_array[-1], y_mu_array[0], y_mu_array[-1]])
plt.plot(x_mu_array[x_max_index_array], y_mu_array[y_max_index_array],'r.')
plt.plot([x_mu_array[0], x_mu_array[-1]], [angle_params[1]*mum_pr_pixel, (angle_params[0]*len(x_mu_array) + angle_params[1])*mum_pr_pixel],'r-')
#plt.plot(x_mu_array[right_max_width_index], y_mu_array[right_max_height_index], 'r.')
#plt.plot([x_mu_array[left_max_width_index], x_mu_array[right_max_width_index]], [y_mu_array[left_max_height_index], y_mu_array[right_max_height_index]], 'r-')
plt.title("Cropped")
plt.xlabel('x [um]')
plt.ylabel('y [um]')

# Plot rotated picture
plt.figure()
plt.imshow(get_intensity_array(rotated_image_array), cmap="jet", vmin=0, vmax=10, extent=[x_mu_array[0], x_mu_array[-1], y_mu_array[0], y_mu_array[-1]])
plt.title("Rotated Image")
plt.xlabel('x [um]')
plt.ylabel('y [um]')

upper_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * upper).astype("int")
lower_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * lower).astype("int")

background_delta = 40
background_lower = lower - background_delta
background_upper = upper + background_delta

background_upper_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * background_upper).astype("int")
background_lower_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * background_lower).astype("int")

plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[upper_index_array], 'r-')
plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[lower_index_array], 'r-')

plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[background_upper_index_array], 'r-')
plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[background_lower_index_array], 'r-')

# Find Saturated Points
unsaturation_percentage_limit = 1
saturated_bool_array = cropped_array != 255
saturated_mean_bool_array = np.mean(saturated_bool_array, axis=0)
peaks_index_array = find_peaks(1 - saturated_mean_bool_array, height=0.05, threshold=None, distance=20, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)[0]
max_array = np.max(cropped_array, axis=0)
saturation_index_list = np.where(max_array != 255)[0]
window_num_pixel_height = np.shape(rotated_image_array)[0]  # 2048
window_num_pixel_ewidth = np.shape(rotated_image_array)[1]  # 2448
length_convolve = 200
saturated_array = max_array != 255
saturated_array_pad = np.pad(saturated_array, (length_convolve, length_convolve), 'constant', constant_values=(0, 1))
saturated_array_pad_convolved = np.convolve(saturated_array_pad, np.ones(length_convolve), 'same') / length_convolve
saturated_array_convolved = saturated_array_pad_convolved[length_convolve:length_convolve + shape_cropped_array[1]]
saturated_list = np.where(saturated_array_convolved >= unsaturation_percentage_limit)

#left_saturation_crop = saturated_list[0][0] + 800
left_saturation_crop = 400
right_saturation_crop = 2000
#right_saturation_crop = saturated_list[0][-1]

# Plot Saturation
plt.figure()
plt.plot(x_mu_array, saturated_array, label="Is Saturated")
plt.plot(x_mu_array, saturated_array_convolved, label="Convolved is Saturated")
plt.plot(x_mu_array, saturated_mean_bool_array, "r-", label="Percentage Saturated")
plt.plot(x_mu_array[peaks_index_array], saturated_mean_bool_array[peaks_index_array], "r.")
plt.plot([x_mu_array[left_saturation_crop], x_mu_array[left_saturation_crop]], [0, 1], 'r')
plt.plot([x_mu_array[right_saturation_crop], x_mu_array[right_saturation_crop]], [0, 1], 'r')
plt.plot([x_mu_array[0], x_mu_array[-1]], [unsaturation_percentage_limit, unsaturation_percentage_limit], 'r')
plt.ylabel('Saturation Index')
plt.title("Saturation")
plt.xlabel('x [um]')
plt.legend()


# Find Background
average_background, confidence_background, prediction_background = find_mean_background(rotated_image_array[:,left_saturation_crop:right_saturation_crop,:], background_lower, background_upper)
print("Background: ", average_background, "+-", confidence_background)

average_background_list, confidence_background_list, prediction_background_list = find_background(rotated_image_array[:,left_saturation_crop:right_saturation_crop,:], background_lower, background_upper)
print("Background: ", average_background, "+-", confidence_background)

# Plot Data
x_length_crop_mu_array = x_mu_array[left_saturation_crop:right_saturation_crop] # 7229 um measured on the GDS, 2445 is the pixel width of the sensor (Both numbers inherent of the sensor and lens)
x = x_length_crop_mu_array

y = np.mean(rotated_image_array[lower:upper, left_saturation_crop:right_saturation_crop, 2], axis=0)
y_std = np.std(rotated_image_array[lower:upper, left_saturation_crop:right_saturation_crop, 2], axis=0)

plt.figure()
#plt.plot(x_length_crop_mu_array, np.max(rotated_image_array[lower:upper, :, 2], axis=0), 'k-', label="Max reading")

plt.plot(x, y, 'b-', label="Raw data")
#plt.plot(x, average_background * np.ones(np.shape(x_length_crop_mu_array)), 'm-', label="Background")
#plt.plot(x, (average_background + 2 * confidence_background) * np.ones(np.shape(x)), 'm', linestyle='dashed', label="2 Sigma Confindece Bound")
#plt.plot(x, (average_background - 2 * confidence_background) * np.ones(np.shape(x)), 'm', linestyle='dashed')
#plt.plot(x, (average_background + 2 * prediction_background) * np.ones(np.shape(x)), 'm', linestyle='dotted', label="2 Sigma Prediction Bound")
#plt.plot(x, (average_background - 2 * prediction_background) * np.ones(np.shape(x)), 'm', linestyle='dotted')
plt.plot(x, average_background_list, 'y-', label="Background")
#plt.plot(x, average_background_list + 2 * confidence_background_list, 'y', linestyle='dashed', label="2 Sigma Confindece Bound")
#plt.plot(x, average_background_list - 2 * confidence_background_list, 'y', linestyle='dashed')
#plt.plot(x, average_background_list + 2 * prediction_background_list, 'y', linestyle='dotted', label="2 Sigma Prediction Bound")
#plt.plot(x, average_background_list - 2 * prediction_background_list, 'y', linestyle='dotted')
plt.legend()
plt.xlabel('x Length [um]')
plt.ylim([0, np.max(y)])
plt.ylabel('Mean of blue intensity')
plt.title(pictures[picture_index])

# Fit Exponential Curve

remove_number = 1

remove_index_array = np.array([])
for peak_index in peaks_index_array:
    remove_index = np.arange(peak_index - remove_number, np.min([peak_index + remove_number + 1, np.size(x_length_crop_mu_array)]), 1)
    remove_index_array = np.concatenate((np.array(remove_index_array), remove_index))

remove_index_array = np.unique(remove_index_array.astype(int))

fit_x = np.delete(x_length_crop_mu_array, [])
fit_y = np.delete(y - average_background_list, [])


initial_guess = [25, 0.0006]
fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(exponential_function, fit_x, fit_y, p0=initial_guess, full_output=True)
fit = exponential_function(fit_x, fit_parameters[0], fit_parameters[1])
residuals = fit - fit_y
mean_squared_error = np.mean(residuals**2)
confidence_bounds_sigma_f = exponential_function_confidence_bounds_sigma(fit_x, fit_parameters[0], fit_parameters[1], fit_parameters_cov_var_matrix)
prediction_bounds_sigma_f = exponential_function_prediction_bounds_sigma(fit_x, fit_parameters[0], fit_parameters[1], fit_parameters_cov_var_matrix, mean_squared_error)

plt.figure()
plt.plot(fit_x, fit_y, 'b-', label="Raw data")
plt.plot(fit_x, fit, 'r-', label="Fitted Curve")
plt.plot(fit_x, fit + 2 * confidence_bounds_sigma_f, 'r', linestyle='dashed', label="2 Sigma Confidence Bound")
plt.plot(fit_x, fit - 2 * confidence_bounds_sigma_f, 'r', linestyle='dashed')
plt.plot(fit_x, fit + 2 * prediction_bounds_sigma_f, 'r', linestyle='dotted', label="2 Sigma Prediction Bound")
plt.plot(fit_x, fit - 2 * prediction_bounds_sigma_f, 'r', linestyle='dotted')

plt.legend()
plt.xlabel('x Length [um]')
plt.ylim([0, np.max(fit_y)])
plt.ylabel('Mean of blue intensity')
plt.title(pictures[picture_index])

print("Picture", pictures[picture_index])
print("Fit Parameters:", fit_parameters)
print("Variance-Covariance Matrix Fit Parameters:", fit_parameters_cov_var_matrix)
print(
    f'a={fit_parameters[0]} +- {np.sqrt(fit_parameters_cov_var_matrix[0, 0])}, b={fit_parameters[1]} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1])}')
print(f"alpha = {fit_parameters[1] * 1e4} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4} 1/cm")
print(
    f'alpha_dB = {- 10 * np.log10(np.exp(-fit_parameters[1] * 1e4))} ({- 10 * np.log10(np.exp(-fit_parameters[1] * 1e4 + np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4))} {- 10 * np.log10(np.exp(-fit_parameters[1] * 1e4 - np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4))}) dB/cm')
print(f'Length over measurement = {fit_x[-1] - fit_x[0]} um')

plt.show()