# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:35:46 2023

@author: frede
"""
 
import numpy as np
import matplotlib.pyplot as plt
import skimage.graph
from skimage.io import imread, imshow
from skimage.morphology import disk
from skimage.color import rgb2gray
from skimage.transform import rotate
from skimage.filters import rank
from skimage import util

from functions import *
 
import scipy.ndimage as ndi
from scipy.fft import ifft2,fftshift, fft2, ifftshift
 

def mean_image_intensity(image,disk_size):
    mean_disk = disk(disk_size)
    mean_image = (rank.mean_percentile(image, footprint=mean_disk, p0=0.1, p1=0.9))
    return mean_image



def find_path(bw_image,start,end):
    costs = np.where(bw_image==1,1,10000)
    path, cost = skimage.graph.route_through_array(costs, start=start, end=end, fully_connected=True)
    return path, cost


def remove_background(image): #FFT image and set center pixel to 0 to remove background and IFFT back to real image
    image_f = fftshift(fft2(image))
    shape = image.shape
    x = int(shape[0]/2)
    y = int(shape[1]/2)
    image_f[x,y] = 0
    
    
    background_f =  fftshift(fft2(image)) - image_f
    
    background = abs(ifft2(ifftshift(background_f)))
    
    fft_img_mod = ifftshift(image_f)
    img_mod = abs(ifft2(fft_img_mod))
    return img_mod, background


def find_input_and_output(indent_list,image):
    input_indent_start = int(image.shape[1]*indent_list[0])
    input_indent_end = int(image.shape[1]*indent_list[1])
    
    output_indent_start = int(image.shape[1]*indent_list[2])
    output_indent_end = int(image.shape[1]*indent_list[3])

    input_index = image[:,input_indent_start:input_indent_end] > 0.05
    imshow(input_index)
    
    cy, cx = ndi.center_of_mass(input_index)

    input_point = (int(cx),int(cy))
    #print(input_point)
    
    output_index = image[:,output_indent_start:output_indent_end] > 0.05
    cy, cx = ndi.center_of_mass(output_index)
    cx = image.shape[1]-cx
    output_point = (int(cx),int(cy))
    
    return input_point, output_point


def main():
    path = "C:\\Users\\frede\\OneDrive\\Skrivebord\\Civil\\Speciale\\W31 1.4 air measurements\\2023-09-07_16_10_03_312_chip12_waveguide2.png"
    path2 = "C:\\Users\\frede\\OneDrive\\Skrivebord\\Civil\\Speciale\\W31 1.4 air measurements\\14-09-23\\loss\\2023-09-14_13_49_08_364_chip14_waveguide8.straight_40mA.png"
    
    
    
    image = util.img_as_float(imread(path))
    #image = (rotate(image,90,resize=True))
    
    plt.figure(figsize=(10,6))
    plt.title("Histogram of channels")
    plt.hist(image[:,:,2].ravel(), bins=256, histtype='step', color='blue')
    plt.hist(image[:,:,1].ravel(), bins=256, histtype='step', color='green')
    plt.hist(image[:,:,0].ravel(), bins=256, histtype='step', color='red')
    plt.yscale("log")
    
    
    plt.figure(figsize=(10,6))
    plt.title("Original Image")
    imshow(image)
    
    #grey_image = rgb2gray(image)
    grey_image = image[:,:,2]
    plt.figure(figsize=(10,6))
    plt.title("Grayscale Image")
    imshow(grey_image)
    
    indent_list = [0.1,0.2,0.95,1]
    in_point, out_point = find_input_and_output(indent_list, grey_image)
    
    plt.figure(figsize=(10,6))
    plt.title("Grayscale Image with input and output and max pixel values removed")
    plt.plot(*in_point,"ro")
    plt.plot(*out_point,"ro")
    
    peaks = grey_image != 1
    grey_image = grey_image*peaks 
    imshow(grey_image)
    
    plt.figure(figsize=(10,6))
    plt.title("Black and white image of waveguide")
    
    
    grey_image, background = remove_background(grey_image)
    
    bw_waveguide = grey_image > 0.01
    imshow(bw_waveguide)
    
    
    start = (in_point[1], in_point[0])
    end = (out_point[1], out_point[0])
    path, costs = find_path(bw_waveguide, start, end)
    
    
    x_path = []
    y_path = []
    for i in range(len(path)):
        #if i % 10 == 0:
        x_path.append(path[i][1])
        y_path.append(path[i][0])
    
    plt.figure(figsize=(10,6))
    plt.title("Image with path")
    plt.plot(*in_point,"ro")
    plt.plot(*out_point,"ro")
    plt.plot(x_path,y_path)
    imshow(grey_image)
    
    
    disk_size = 10
    mean_image = mean_image_intensity(grey_image, disk_size)
    
    
    plt.figure(figsize=(10,6))
    plt.title("Mean of Image")
    imshow(mean_image,cmap="twilight_shifted")
    
    intensity_values = mean_image[y_path,x_path]
    
    cummulated = np.cumsum(np.flip(intensity_values))
    background_intensity = background[y_path,x_path]
    
    #flip_cummulated = np.flip(cummulated)
    
    
    
    plt.figure(figsize=(10,6))
    plt.title("Mean of intensity values as a function of distance, with background")
    #plt.plot(intensity_values)
    plt.plot(cummulated)
    #plt.plot(background_intensity) 
    plt.xlabel('Point in path')
    plt.ylabel('Mean blue intensity')
    plt.legend(["Mean intensity", "Background"])
    plt.show()
    
    
    #db = [4.21, 6.61, 6.78, 6.63, 7.46, 7.11, 6.62, 5.39]
    #print(sum(db)/(len(db)))
    #power = [40,50,60,70,80,90,100,200]
    #plt.figure(figsize=(10,6))
    #plt.plot(power,db)
    #plt.axhline(sum(db)/(len(db)))
    #plt.legend(["Loss from 40-200mA", "Mean loss"])
    #plt.xlabel("Laser current (mA)")
    #plt.ylabel("dB/cm")
    
    cummulated = intensity_values
    
    spiral_diameter_um = 1102 #Measured in klayout
    
    mum_per_pixel = spiral_diameter_um/(out_point[1]-in_point[1])
    
    fit_x = range(len(cummulated))
    
    fit_x = np.array([x*mum_per_pixel for x in fit_x])
    
    initial_guess = np.array([25, -0.0009, 0])
    fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(exponential_function_offset, fit_x, cummulated, p0=initial_guess, full_output=True)
    fit = exponential_function_offset(fit_x, *fit_parameters)
    fit_guess = exponential_function_offset(fit_x, *initial_guess)
    residuals = fit - cummulated
    mean_squared_error = np.mean(residuals**2)
    confidence_bounds_sigma_f = exponential_function_offset_confidence_bounds_sigma(fit_x, fit_parameters[0], fit_parameters[1], fit_parameters[2], fit_parameters_cov_var_matrix)
    #prediction_bounds_sigma_f = exponential_function_prediction_bounds_sigma(fit_x, fit_parameters[0], fit_parameters[1], fit_parameters_cov_var_matrix, mean_squared_error)
    
    plt.figure(figsize=(10,6))
    plt.plot(fit_x, cummulated, 'b-', label="Raw data")
    plt.plot(fit_x, fit, 'r-', label="Fitted Curve")
    
    plt.plot(fit_x, fit_guess, 'g-', label="Initial guess")
    #plt.plot(fit_x, fit + 2 * confidence_bounds_sigma_f, 'r', linestyle='dashed', label="2 Sigma Confidence Bound")
    #plt.plot(fit_x, fit - 2 * confidence_bounds_sigma_f, 'r', linestyle='dashed')
    #plt.plot(fit_x, fit + 2 * prediction_bounds_sigma_f, 'r', linestyle='dotted', label="2 Sigma Prediction Bound")
    #plt.plot(fit_x, fit - 2 * prediction_bounds_sigma_f, 'r', linestyle='dotted')
    plt.legend()
    plt.xlabel('x Length [um]')
    
    plt.ylabel('Mean of blue intensity')
    
    print("Fit Parameters:", fit_parameters)
    print("Variance-Covariance Matrix Fit Parameters:", fit_parameters_cov_var_matrix)
    print(
        f'a={fit_parameters[0]} +- {np.sqrt(fit_parameters_cov_var_matrix[0, 0])}, b={fit_parameters[1]} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1])}')
    print(f"alpha = {fit_parameters[1] * 1e4} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4} 1/cm")
    print(
        f'alpha_dB = {10 * np.log10(np.exp(-fit_parameters[1] * 1e4))} ({- 10 * np.log10(np.exp(-fit_parameters[1] * 1e4 + np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4))} {- 10 * np.log10(np.exp(-fit_parameters[1] * 1e4 - np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4))}) dB/cm')
    print(f'Length over measurement = {fit_x[-1] - fit_x[0]} um')
    

if __name__ == "__main__":
    main()
