# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:35:46 2023

@author: frede
"""
 
import numpy as np
import matplotlib.pyplot as plt
import skimage.graph
from skimage.io import imread, imshow
from skimage.morphology import disk, rectangle
from skimage.color import rgb2gray
from skimage.transform import rotate
from skimage.filters import rank
from skimage import util

from functions import *
 
import scipy.ndimage as ndi
from scipy.fft import ifft2,fftshift, fft2, ifftshift
 

def mean_image_intensity(image,disk_size,q1=0,q3=1):
    mean_disk = disk(disk_size)

    mean_image = (rank.mean_percentile(image, footprint=mean_disk,p0=q1,p1=q3))
    return mean_image

def mean_image_intensity_rectangular(image,row,col,q1=0,q3=1):
    mean_rectangle = rectangle(row,col)
    mean_image = (rank.mean_percentile(image, footprint=mean_rectangle,p0=q1,p1=q3))
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

    input_index = image[:,input_indent_start:input_indent_end] > 0.2
    imshow(input_index)
    
    cy, cx = ndi.center_of_mass(input_index)
    
    cx = cx + input_indent_start
    
    
    input_point = (int(cx),int(cy))
    #print(input_point)
    
    output_index = image[:,output_indent_start:output_indent_end] > 0.2
    cy, cx = ndi.center_of_mass(output_index)
    cx = image.shape[1]-cx
    
    output_point = (int(cx),int(cy))
    
    return input_point, output_point

def um_per_pixel(point1, point2, distance):     
    # calculating Euclidean distance
    dist_pixels = np.linalg.norm(point1 - point2)
    return distance / dist_pixels

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def remove_outliers_IQR(intensity):
    temp_intensity = intensity
    new_x = [range(len(temp_intensity))]
    
    Q1 = np.percentile(temp_intensity, 25, method='midpoint')
    Q3 = np.percentile(temp_intensity, 75, method='midpoint')
    IQR = Q3 - Q1

    upper=Q3+1.5*IQR
    lower=Q1-1.5*IQR
    
    print(upper)
    print(lower)

    upper_array = np.where(temp_intensity>=upper)[0]
    lower_array = np.where(temp_intensity<=lower)[0]

    remove_array = np.concatenate((upper_array,lower_array))

    new_intensity = np.delete(temp_intensity,remove_array)
    new_x = np.delete(new_x,remove_array)
    return new_x, new_intensity

path = "C:/Users/frede/Downloads/2023-10-03_ST2_Toptica_980nm_70mW_Width_1600nm_TE.bmp"
path2 = "C:\\Users\\frede\\OneDrive\\Skrivebord\\Civil\\Speciale\\W31 1.4 air measurements\\14-09-23\\loss\\2023-09-14_13_04_52_198_chip14_waveguide3_straight_40mA_TE_polarized.png"



image = util.img_as_float(imread(path))
image = (rotate(image,180,resize=True))

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



point1 = np.array((in_point[1],0))
point2 = np.array((out_point[1],grey_image.shape[1]))



distance_um = 3800 #Measured in klayout  
mum_per_pixel = um_per_pixel(point1, point2, distance_um)

#peaks = grey_image != 1
#grey_image = grey_image*peaks 
imshow(grey_image)

plt.figure(figsize=(10,6))
plt.title("Black and white image of waveguide")


grey_image, background = remove_background(grey_image)


bw_waveguide = grey_image > 0.1
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


disk_size = 20
row = 20
col = 3
q1= 0.00
q3 = 1

#mean_image = mean_image_intensity(grey_image, disk_size)
mean_image = mean_image_intensity_rectangular(grey_image, row, col,q1,q3)

mean_test = mean_image_intensity_rectangular(grey_image, row, col)

test_x, new_intensity = remove_outliers_IQR(mean_image[y_path,x_path])


plt.figure(figsize=(10,6))
plt.title("Mean of Image")
imshow(mean_image,cmap="twilight_shifted")

intensity_values = mean_image[y_path,x_path]
intensity_test = mean_test[y_path,x_path]

background_intensity = background[y_path,x_path]


#mov_intensity_values = moving_average(new_intensity, 100)

plt.figure(figsize=(10,6))
plt.title("Mean of intensity values as a function of distance, with background")
plt.plot(intensity_values)
#plt.plot(intensity_test)
plt.plot(test_x,new_intensity)
plt.plot(background_intensity) 
plt.xlabel('Point in path')
plt.ylabel('Mean blue intensity')
plt.legend(["Mean intensity", "Statistical outliers removed","Background"])
plt.show()


#intensity_values = new_intensity




#point1 = np.array((0,0))
#point2 = np.array((0,grey_image.shape[1]))



fit_x = range(len(intensity_values))

fit_x = np.array([x*mum_per_pixel for x in fit_x])


initial_guess = np.array([25, -0.0009])
fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(exponential_function, fit_x, intensity_values, p0=initial_guess, full_output=True)
fit = exponential_function(fit_x, *fit_parameters)
fit_guess = exponential_function(fit_x, *initial_guess)
residuals = fit - intensity_values
mean_squared_error = np.mean(residuals**2)

var_a = fit_parameters_cov_var_matrix[0,0]
var_b = fit_parameters_cov_var_matrix[1,1]

upper_a = fit_parameters[0]+1.440*np.sqrt(var_a)
lower_a = fit_parameters[0]-1.440*np.sqrt(var_a)

upper_b = fit_parameters[1]+1.440*np.sqrt(var_b)
lower_b = fit_parameters[1]-1.440*np.sqrt(var_b)

fit_upper = exponential_function(fit_x,*[upper_a,upper_b])
fit_lower = exponential_function(fit_x,*[lower_a,lower_b])


upper_array = np.where(intensity_values>=fit_upper)[0]
lower_array = np.where(intensity_values<=fit_lower)[0]

remove_array = np.concatenate((upper_array,lower_array))

#intensity_values = np.delete(intensity_values,remove_array)
#fit_x_new = np.delete(fit_x,remove_array)


#fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(exponential_function, fit_x_new, intensity_values, p0=initial_guess, full_output=True)
#fit_new = exponential_function(fit_x_new, *fit_parameters)
#confidence_bounds_sigma_f = exponential_function_confidence_bounds_sigma(fit_x, fit_parameters[0], fit_parameters[1], fit_parameters_cov_var_matrix)
#prediction_bounds_sigma_f = exponential_function_prediction_bounds_sigma(fit_x, fit_parameters[0], fit_parameters[1], fit_parameters_cov_var_matrix, mean_squared_error)

plt.figure(figsize=(10,6))
plt.plot(fit_x, intensity_values, 'b-', label="Raw data")
plt.plot(fit_x, fit, 'r-', label="Fitted Curve")
#plt.plot(fit_x_new, fit_new, 'g-', label="New Fitted Curve")

#plt.plot(fit_x, fit_guess, 'g-', label="Initial guess")
#plt.plot(fit_x, fit + 2 * confidence_bounds_sigma_f, 'r', linestyle='dashed', label="2 Sigma Confidence Bound")
#plt.plot(fit_x, fit - 2 * confidence_bounds_sigma_f, 'r', linestyle='dashed')
plt.plot(fit_x, fit_upper, 'r', linestyle='dashed', label="2 Sigma Confidence Bound")
plt.plot(fit_x, fit_lower, 'r', linestyle='dashed')
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
    f'alpha_dB = {10 * np.log10(np.exp(fit_parameters[1] * 1e4))} +- {10 * np.log10(np.exp(np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4))}) dB/cm')
print(f'Length over measurement = {fit_x[-1] - fit_x[0]} um')

from sklearn.metrics import r2_score

coefficient_of_determination = r2_score(intensity_values, fit)    

print(f"R^2: {coefficient_of_determination}")
    


#%%

def analyse_image(grey_image, row, col, x_path, y_path, mum_per_pixel):
    q1= 0
    q3 = 0.95
    mean_image = mean_image_intensity_rectangular(grey_image, row, col,q1,q3)

    fit_x, intensity = remove_outliers_IQR(mean_image[y_path,x_path])



    fit_x = np.array([x*mum_per_pixel for x in fit_x])


    initial_guess = np.array([25, -0.0009])
    fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(exponential_function, fit_x, intensity, p0=initial_guess, full_output=True)
    fit = exponential_function(fit_x, *fit_parameters)
    fit_guess = exponential_function(fit_x, *initial_guess)


    var_a = fit_parameters_cov_var_matrix[0,0]
    var_b = fit_parameters_cov_var_matrix[1,1]

    upper_a = fit_parameters[0]+1.440*np.sqrt(var_a)
    lower_a = fit_parameters[0]-1.440*np.sqrt(var_a)

    upper_b = fit_parameters[1]+1.440*np.sqrt(var_b)
    lower_b = fit_parameters[1]-1.440*np.sqrt(var_b)

    fit_upper = exponential_function(fit_x,*[upper_a,upper_b])
    fit_lower = exponential_function(fit_x,*[lower_a,lower_b])



    upper_array = np.where(intensity>=fit_upper)[0]
    lower_array = np.where(intensity<=fit_lower)[0]

    remove_array = np.concatenate((upper_array,lower_array))

    #intensity_values = np.delete(intensity_values,remove_array)
    #fit_x_new = np.delete(fit_x,remove_array)


    #fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(exponential_function, fit_x_new, intensity_values, p0=initial_guess, full_output=True)
    #fit_new = exponential_function(fit_x_new, *fit_parameters)
    #confidence_bounds_sigma_f = exponential_function_confidence_bounds_sigma(fit_x, fit_parameters[0], fit_parameters[1], fit_parameters_cov_var_matrix)
    #prediction_bounds_sigma_f = exponential_function_prediction_bounds_sigma(fit_x, fit_parameters[0], fit_parameters[1], fit_parameters_cov_var_matrix, mean_squared_error)


    print("Fit Parameters:", fit_parameters)
    print("Variance-Covariance Matrix Fit Parameters:", fit_parameters_cov_var_matrix)
    print(
        f'a={fit_parameters[0]} +- {np.sqrt(fit_parameters_cov_var_matrix[0, 0])}, b={fit_parameters[1]} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1])}')
    print(f"alpha = {fit_parameters[1] * 1e4} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4} 1/cm")
    print(
        f'alpha_dB = {10 * np.log10(np.exp(fit_parameters[1] * 1e4))} +- {10 * np.log10(np.exp(np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4))}) dB/cm')
    print(f'Length over measurement = {fit_x[-1] - fit_x[0]} um')
    
    
    return 10 * np.log10(np.exp(fit_parameters[1] * 1e4))
    
alphas = []
for rows in range(1,101):
    alpha = analyse_image(grey_image, rows, 3, x_path, y_path, mum_per_pixel)
    alphas.append(alpha)
    
x = range(1,101)

#%%
plt.figure(figsize=(10,6))
plt.plot(x,alphas)
plt.xlabel("Rectangle mean rows")
plt.ylabel("Alpha value in dB")
plt.show()


print(alphas.index(min(alphas[1:])))

#%%

alphas_cols = []
for cols in range(1,100):
    alpha = analyse_image(grey_image, 10, cols, x_path, y_path, mum_per_pixel)
    alphas_cols.append(alpha)
    



#%%
x = range(1,100)
plt.figure(figsize=(10,6))
plt.plot(x,alphas_cols)
plt.xlabel("Rectangle mean cols")
plt.ylabel("Alpha value in dB")
plt.show()