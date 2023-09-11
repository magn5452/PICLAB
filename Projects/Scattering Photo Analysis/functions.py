import glob
import matplotlib.image as mpimg
import scipy
import os
import sys

from scipy.fftpack import fftfreq, fft, ifft
from scipy.signal import convolve2d
from scipy.signal import convolve
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit
import scipy.stats as sct


def find_left_right_index(window_num_pixel_width, window_num_pixel_height, image_array, left_indent, right_indent):
    left_gauss_p0 = [0, 255, 1115, 100]
    right_gauss_p0 = [0, 255, 1115, 100]
    plt.figure()
    poptleft, pcov = curve_fit(gaussian_function, range(window_num_pixel_height), image_array[:, 0, 2],
                               p0=left_gauss_p0, maxfev=10000)
    poptright, pcov = curve_fit(gaussian_function, range(window_num_pixel_height),
                                image_array[:, window_num_pixel_width - left_indent - right_indent - 1, 2],
                                p0=right_gauss_p0, maxfev=10000)
    plt.plot(range(window_num_pixel_height), gaussian_function(range(window_num_pixel_height), *poptleft),
             label='Gaussian fit')
    plt.plot(range(window_num_pixel_height), image_array[:, 0, 2], label='Data')
    plt.legend()
    plt.title('Left hand side blue values')
    plt.figure()
    plt.title('Right hand side blue values')
    plt.plot(range(window_num_pixel_height), gaussian_function(range(window_num_pixel_height), *poptright),
             label='Gaussian fit')
    plt.plot(range(window_num_pixel_height),
             image_array[:, window_num_pixel_width - left_indent - right_indent - 1, 2], label='Data')
    plt.legend()
    left_max_index = find_closest(image_array[:, 0, 2], poptleft[2])
    right_max_index = find_closest(image_array[:, window_num_pixel_width - left_indent - right_indent - 1, 2],
                                   poptright[2])
    return left_max_index, right_max_index


def find_waveguide_angle(image_array, left_index_guess, left_right_separation, number_of_points):
    kernel = np.ones([1, 50]) / (1 * 50)
    smoothed_image_array = convolve2d(image_array, kernel)
    plt.figure()
    plt.imshow(smoothed_image_array)
    x_index_array = []
    max_height_index_array = []
    for index in range(0, number_of_points):
        x_index = left_index_guess + index*left_right_separation
        x_index_array.append(x_index)
        max_array = np.flip(np.mean(smoothed_image_array[:, x_index: left_index_guess + x_index + 1], axis=1))
        max_height_index = np.argmax(max_array - np.mean(max_array))
        max_height_index_array.append(max_height_index)

    param, covparam = curve_fit(linear_function, x_index_array, max_height_index_array)
    angle = np.degrees(np.arctan(param[0]))

    return angle, param, x_index_array, max_height_index_array


def increase_contrast(image_array, contrast):
    return contrast_function(image_array, contrast)


def contrast_function(x, contrast):
    maximum_value = np.max(x)
    minimum_value = np.min(x)
    middle_value = (maximum_value - minimum_value) / 2
    if contrast != 0:
        a = -contrast / np.log(contrast)
        result = maximum_value / (1 + np.exp(-a * x / maximum_value))
    else:
        result = x
    return result


def find_chip(image):
    image_array = np.array(image)
    image_array_shape = np.shape(image_array)

    image_width = image_array_shape[0]
    image_height = image_array_shape[1]

    scale_factor = 2 ** 4

    resized_height = int(np.rint(image_height / scale_factor))  # New width in pixels
    resized_width = int(np.rint(image_width / scale_factor))  # New height in pixels

    resized_image = image.resize((resized_height, resized_width), Image.LANCZOS)
    resized_array = np.array(resized_image)
    intensity_array = get_intensity_array(resized_array)

    # Define a simple convolution kernel
    kernel_size = 8
    kernel = np.ones([kernel_size, kernel_size]) / kernel_size ** 2
    filtered_intensity_array = convolve2d(intensity_array[:, :], kernel, mode='same', boundary='wrap')

    contrast_image_array = increase_contrast(filtered_intensity_array, 0)

    plt.figure()
    plt.imshow(contrast_image_array, cmap="plasma")
    plt.title("Intensity")

    plt.figure()
    plt.imshow(image_array, cmap="plasma")
    plt.title("Intensity")

    plt.figure()
    plt.imshow(intensity_array, cmap="plasma")
    plt.title("Intensity")

    plt.figure()
    plt.imshow(filtered_intensity_array, cmap="plasma")
    plt.title("Filtered Intensity")

    peaks_list = []
    for index in range(74, 75):
        plt.figure()
        plt.plot(filtered_intensity_array[:, 75])
        smart = np.convolve(np.abs(np.gradient(filtered_intensity_array[:, 75])),
                            np.ones(int(kernel_size * 1.5)) / int(kernel_size * 1.5))
        peaks = scipy.signal.find_peaks(smart, height=[0.1], threshold=None, distance=40, prominence=None, width=None,
                                        wlen=None, rel_height=0.5, plateau_size=None)[0]
        plt.plot(smart)
        plt.plot(peaks, smart[peaks])

    plt.figure()
    plt.plot(filtered_intensity_array[75, :])
    smart = np.convolve(np.abs(np.gradient(filtered_intensity_array[75, :])),
                        np.ones(int(kernel_size * 1.5)) / int(kernel_size * 1.5))
    plt.plot(smart)
    peaks = \
        scipy.signal.find_peaks(smart, height=[0.1], threshold=None, distance=80, prominence=None, width=None,
                                wlen=None,
                                rel_height=0.5, plateau_size=None)[0]
    plt.plot(peaks, smart[peaks])


def insertion_detection(image):
    # Convert the image to a NumPy array
    image_array = np.array(image)
    image_array_shape = np.shape(image_array)

    scale_factor = 2 ** 3
    new_height = int(np.rint(image_array_shape[0] / scale_factor))  # New width in pixels
    new_width = int(np.rint(image_array_shape[1] / scale_factor))  # New height in pixels
    print(new_height)
    print(new_width)
    # Resize the image to the new dimensions
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    resized_image_array = np.array(resized_image)

    # Define a simple convolution kernel
    kernel_size = 4
    kernel = np.ones([kernel_size, kernel_size]) / kernel_size ** 2

    # Apply convolution separately for each color channel
    filtered_channels = []
    for channel in range(3):  # RGB channels
        filtered_channel = convolve2d(resized_image_array[:, :, channel], kernel, mode='same', boundary='wrap')
        filtered_channels.append(filtered_channel)

    # Combine the filtered channels back into an RGB image
    filtered_image_array = np.stack(filtered_channels, axis=2)

    intensity_filtered_image_array = get_intensity_array(filtered_image_array)

    plt.figure()
    plt.imshow(intensity_filtered_image_array, cmap="jet", vmin=0, vmax=255)

    resized_input_index = np.unravel_index(np.argmax(intensity_filtered_image_array, axis=None),
                                           intensity_filtered_image_array.shape)

    input_height_index = int(resized_input_index[0] * scale_factor)
    input_width_index = int(resized_input_index[1] * scale_factor)

    height_tolerance_output = 100
    left_index_limit = int(new_width) - 20
    right_index_limit = int(new_width) - 1
    lower_index_limit = int((input_height_index - height_tolerance_output) / scale_factor)
    upper_index_limit = int((input_height_index + height_tolerance_output) / scale_factor)
    height_tolerance_output = 100
    plt.plot([0, new_width], [upper_index_limit, upper_index_limit], 'r-')
    plt.plot([0, new_width], [lower_index_limit, lower_index_limit], 'r-')
    plt.plot([left_index_limit, left_index_limit], [lower_index_limit, upper_index_limit], 'r-')
    plt.plot([right_index_limit, right_index_limit], [lower_index_limit, upper_index_limit], 'r-')
    plt.plot([0, 0], [0, kernel_size], 'b-')
    plt.plot([kernel_size, kernel_size], [0, kernel_size], 'b-')
    plt.plot([0, kernel_size], [0, 0], 'b-')
    plt.plot([0, kernel_size], [kernel_size, kernel_size], 'b-')
    output_array = intensity_filtered_image_array[lower_index_limit: upper_index_limit,
                   left_index_limit: right_index_limit]
    resized_output_index = np.unravel_index(np.argmax(output_array, axis=None), output_array.shape)

    output_height_index = int((resized_output_index[0] + lower_index_limit) * scale_factor)
    output_width_index = int((resized_output_index[1] + left_index_limit) * scale_factor)

    plt.plot(resized_input_index[1], resized_input_index[0], 'r.')
    plt.plot(resized_output_index[1] + left_index_limit, resized_output_index[0] + lower_index_limit, 'r.')
    return input_width_index, input_height_index, output_width_index, output_height_index


def print_files(path, extension):
    print(path)
    filepaths = glob.glob(path + '//*.' + extension)
    print(filepaths)
    filenames = [None] * len(filepaths)
    for n in range(len(filepaths)):
        filenames[n] = filepaths[n][len(path):]
    for (i, item) in enumerate(filenames, start=0):
        print(i, ': ' + item)
    return filenames


def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
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


def frequency_filter(time, signal_time):
    dt = time[1] - time[0]  # Sample Time
    frequency = fftfreq(signal_time.size, d=dt)
    signal_frequency = fft(signal_time)
    cut_f_signal = signal_frequency.copy()
    cut_f_signal[(np.abs(frequency) > 0.02)] = 0  # cut signal above 3Hz

    filtered_signal_time = np.real_if_close(ifft(cut_f_signal))
    return filtered_signal_time


def gaussian_function(x, H, A, mu, sigma):
    return H + A * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


def exponential_function(x, a, b):
    return a * np.exp(-b * x)


def linear_function(x, a, b):
    return a * x + b


def linear_function_confidence_bounds_sigma(x, a, b, var_cov_matrix):
    var_a = var_cov_matrix[0, 0]
    var_b = var_cov_matrix[1, 1]
    cov_ab = var_cov_matrix[1, 0]
    dfda = x
    dfdb = 1
    return np.sqrt(var_a * dfda ** 2 + var_b * dfdb ** 2 + 2 * cov_ab * dfda * dfdb)


def fig_reg_exponential_function(x, a, b):
    return a * np.exp(-b * x)


def cost_exponential_function(params, x, y):
    return params[0] * np.exp(-params[1] * x) - y


def exponential_function_confidence_bounds_sigma(x, a, b, var_cov_matrix):
    var_a = var_cov_matrix[0, 0]
    var_b = var_cov_matrix[1, 1]
    cov_ab = var_cov_matrix[1, 0]
    f = exponential_function(x, a, b)
    dfda = (f / a)
    dfdb = (-x * f)
    return np.sqrt(var_a * dfda ** 2 + var_b * dfdb ** 2 + 2 * cov_ab * dfda * dfdb)


def exponential_function_prediction_bounds_sigma(x, a, b, var_cov_matrix, mean_squared_error):
    var_a = var_cov_matrix[0, 0]
    var_b = var_cov_matrix[1, 1]
    cov_ab = var_cov_matrix[1, 0]
    f = exponential_function(x, a, b)
    dfda = (f / a)
    dfdb = (-x * f)
    return np.sqrt(mean_squared_error ** 2 + var_a * dfda ** 2 + var_b * dfdb ** 2 + 2 * cov_ab * dfda * dfdb)


def find_closest(xs, x):
    """Return the index of the value closest to x in array xs."""
    diff = np.abs(xs - x)
    idx = diff.argmin()
    median_indices = np.where(diff == diff.min())[0]
    if len(median_indices) > 1:
        idx = int(np.median(median_indices))
    return idx


def find_mean_background(image_array, lower, upper):
    image_array_shape = np.shape(image_array)
    a = np.arange(0, lower)
    b = np.arange(upper, image_array_shape[0])
    slice_height_index_array = np.concatenate((a, b))
    background_array = image_array[slice_height_index_array, :, 2]
    background_array_shape = np.shape(background_array)
    number_of_points = background_array_shape[0] * background_array_shape[1]
    average_background = np.mean(background_array)
    prediction_background = np.std(background_array)
    confidence_background = prediction_background / np.sqrt(number_of_points)
    return average_background, confidence_background, prediction_background


def find_background(image_array, lower, upper):
    image_array_shape = np.shape(image_array)
    a = np.arange(0, lower)
    b = np.arange(upper, image_array_shape[0])
    slice_height_index_array = np.concatenate((a, b))
    background_array = image_array[slice_height_index_array, :, 2]
    background_array_shape = np.shape(background_array)
    number_of_points = background_array_shape[0]
    average_background = np.mean(background_array, 0)
    prediction_background = np.std(background_array, 0)
    confidence_background = prediction_background / np.sqrt(number_of_points)
    return average_background, confidence_background, prediction_background


def get_intensity_array(image_array):
    return np.clip(np.sqrt(image_array[:, :, 0] ** 2 + image_array[:, :, 1] ** 2 + image_array[:, :, 2] ** 2) / np.sqrt(
        3 * 255 ** 2) * 255, 0, 255)
