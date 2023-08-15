import glob
import matplotlib.image as mpimg
import scipy
import os
import sys
from scipy.signal import convolve2d
from scipy.signal import convolve
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit


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


def find_left_right_index_max(image_array, left_right_separation):
    kernel = np.ones([10, 200]) / (10 * 200)

    smoothed_image_array = convolve2d(image_array, kernel)
    left_array = np.mean(smoothed_image_array[:, 0:50], axis=1)
    right_array = np.mean(smoothed_image_array[:, left_right_separation:left_right_separation + 50], axis=1)
    filtered_image = Image.fromarray(smoothed_image_array)
    plt.imshow(filtered_image)

    plt.figure()
    plt.title('Left hand side blue values')
    plt.plot(left_array)

    plt.figure()
    plt.title('Right hand side blue values')
    plt.plot(right_array)

    left_max_index = np.argmax(left_array)
    right_max_index = np.argmax(right_array)

    return left_max_index, right_max_index

def defect_detection(image_array):
    width_array = []
    height_array = []
    return

def insertion_detection(image):
    # Convert the image to a NumPy array
    image_array = np.array(image)
    image_array_shape = np.shape(image_array)

    scale_factor = 2 ** 6
    new_width = int(np.rint(image_array_shape[0] / scale_factor))  # New width in pixels
    new_height = int(np.rint(image_array_shape[1] / scale_factor))  # New height in pixels
    print(new_width)
    print(new_height)
    # Resize the image to the new dimensions
    resized_image = image.resize((new_height, new_width), Image.LANCZOS)
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

    intensity_array = np.sqrt(
        filtered_image_array[:, :, 0] ** 2 + filtered_image_array[:, :, 1] ** 2 + filtered_image_array[:, :, 2] ** 2)

    resized_max_index = np.unravel_index(np.argmax(intensity_array, axis=None), intensity_array.shape)
    print(resized_max_index)
    max_height_index = int(resized_max_index[0] * scale_factor)
    max_width_index = int(resized_max_index[1] * scale_factor)
    print(max_height_index, "_", max_width_index)
    plt.figure()
    plt.imshow(image)
    plt.plot([max_width_index], [max_height_index], '.')
    return max_height_index, max_width_index


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


def gaussian_function(x, H, A, mu, sigma):
    return H + A * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


def exponential_function(x, a, b):
    return a * np.exp(-b * x)


def find_closest(xs, x):
    """Return the index of the value closest to x in array xs."""
    diff = np.abs(xs - x)
    idx = diff.argmin()
    median_indices = np.where(diff == diff.min())[0]
    if len(median_indices) > 1:
        idx = int(np.median(median_indices))
    return idx
