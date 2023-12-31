# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 09:08:25 2023

@author: Peter Tønning, Kevin Bach Gravesen, Magnus Linnet Madsen, Frederik P
"""

import numpy
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit, least_squares
from scipy.signal import find_peaks, savgol_filter
from time import time
import sys
sys.path.append("C:/Users/frede/OneDrive/Skrivebord/Civil/Speciale/PICLAB/Projects/Scattering Photo Analysis")
from functions import *
from scipy import signal
from scipy.fft import ifft2,fftshift, fft2, ifftshift



class SPA:
    
    def __init__(self, show_plots, chiplength, manual=False):
        self.show_plots = show_plots
        self.chiplength = chiplength  # 7229 um measured on the GDS, 2445 is the pixel width of the sensor (Both numbers inherent of the sensor and lens)
        self.manual = manual # When true remember to call manual_input_output and set_um_per_pixel before analyze_image

        
    def set_um_per_pixel(self, point1, point2):
        # calculating Euclidean distance
        points = [np.array(point1),np.array(point2)]
        dist_pixels = np.linalg.norm(points[0] - points[1]) 
        
        self.mum_per_pixel = self.chiplength / dist_pixels
    
    def rotate_image(self, image, input_side="left"):
        
        if input_side == "left":
            image = image.rotate(90,expand=True)
    
        elif input_side == "right":
            image = image.rotate(-90,expand=True)
            
        elif input_side == "flip":
             image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        
        else:
            raise Exception("Specify input side 'left', 'right', 'flip'")
        
        return image
    
    
    def SMA(self,data,m=10):
        i = 0
        ma = []
        
        while i < len(data) - m + 1:
            
            window_average = np.sum(data[i:i+m])/m
            ma.append(window_average)
            i += 1
        return ma
    
    def moving_sum(self,data,M):
        return np.convolve(data,np.ones(M,dtype=float),"valid")/M
    
    def CMA(self,data):
        i = 1
        ma = []
        
        cum_sum = np.cumsum(data)
        
        while i < len(data):
            
            window_average = cum_sum[i-1] / i
            ma.append(window_average)
            i += 1
        return ma
    
    
    def EMA(self,data,smoothing=0.01):
        i = 1
        ma = []
        
        ma.append(data[0])
        
        while i < len(data):
            
            window_average = smoothing*data[i] + (1-smoothing) * ma[-1]
            ma.append(window_average)
            i += 1
        return ma
        
    def remove_outliers_IQR(self,x , data,blocks,num_neighbors):
        data_blocks = np.array_split(data,blocks)
        x_blocks = np.array_split(x,blocks)
        
        
        for i in range(len(data_blocks)):
            Q1 = np.percentile(data_blocks[i], 25, method='midpoint')
            Q3 = np.percentile(data_blocks[i], 75, method='midpoint')
            IQR = Q3 - Q1

            upper=Q3+1.5*IQR
            lower=Q1-1.5*IQR
            

            upper_array = np.where(data_blocks[i]>=upper)[0]
            lower_array = np.where(data_blocks[i]<=lower)[0]
            
            
            remove_array = np.concatenate((upper_array,lower_array))
            new_remove_array = []

            for index in remove_array:
                neighbor_indexes = np.arange(index-num_neighbors,index+num_neighbors+1,1)
                neighbor_indexes = [x for x in neighbor_indexes if x > 0 and x < len(data_blocks[i])]
                new_remove_array += neighbor_indexes
            
            new_remove_array = list(set(new_remove_array))
            data_blocks[i] = np.delete(data_blocks[i],new_remove_array)
            x_blocks[i] = np.delete(x_blocks[i],new_remove_array)
        
        
        
        return np.concatenate(x_blocks), np.concatenate(data_blocks)
        
    def threshold_background(self,x ,data,blocks,background):
        data_blocks = np.array_split(data,blocks)
        x_blocks = np.array_split(x,blocks)
        
        
        index = len(data_blocks)
        for i in range(len(data_blocks)):
            data_mean = np.mean(data_blocks[i])
            if data_mean < background:
                index = i
                break
        
        return np.concatenate(x_blocks[:index]), np.concatenate(data_blocks[:index])
        
    def plot_histogram(self, image):
        plt.figure(figsize=(10,6))
        plt.title("Histogram of RGB channels")
        plt.hist(image[:,:,2].ravel(), bins=256, histtype='step', color='blue')
        plt.hist(image[:,:,1].ravel(), bins=256, histtype='step', color='green')
        plt.hist(image[:,:,0].ravel(), bins=256, histtype='step', color='red')
        plt.yscale("log")
        
    
    def manual_input_and_output(self,input_point, output_point):
        self.input_width_index = input_point[0]
        self.input_height_index = input_point[1]
        
        self.output_width_index = output_point[0]
        self.output_height_index = output_point[1]
    
    
    def remove_background(self, image): #FFT image and set center pixel to 0 to remove background and IFFT back to real image
        image_f = fftshift(fft2(image))
        shape = image.shape
        x = int(shape[1]/2)
        y = int(shape[0]/2)

        image_f[y,x] = 0

        
        background_f =  fftshift(fft2(image)) - image_f
        
        background = abs(ifft2(ifftshift(background_f)))
        
        fft_img_mod = ifftshift(image_f)
        img_mod = abs(ifft2(fft_img_mod))
        return img_mod, background
    

    
    def calculate_confidence_interval(self,fit_parameters,fit_parameters_cov_var_matrix, x ,confidence_interval):
        var_a = fit_parameters_cov_var_matrix[0,0]
        var_b = fit_parameters_cov_var_matrix[1,1]
        var_c = fit_parameters_cov_var_matrix[2,2]


        upper_a = fit_parameters[0]+confidence_interval*np.sqrt(var_a)
        lower_a = fit_parameters[0]-confidence_interval*np.sqrt(var_a)

        upper_b = fit_parameters[1]+confidence_interval*np.sqrt(var_b)
        lower_b = fit_parameters[1]-confidence_interval*np.sqrt(var_b)
        
        upper_c = fit_parameters[2]+confidence_interval*np.sqrt(var_c)
        lower_c = fit_parameters[2]-confidence_interval*np.sqrt(var_c)


        fit_upper = exponential_function_offset(x,*[upper_a,upper_b,upper_c])
        fit_lower = exponential_function_offset(x,*[lower_a,lower_b,upper_c])
        
        return fit_upper,fit_lower, upper_b, lower_b 
    
    def crop_and_rotate(self,image,input_indent,output_indent,interval):
        
        image_array = np.asarray(image)
        
        if self.manual == True:
            input_width_index = self.input_width_index
            input_height_index = self.input_height_index
            output_width_index = self.output_width_index
            output_height_index = self.output_height_index
        else:
            input_width_index, input_height_index, output_width_index, output_height_index = insertion_detection(image.copy(),self.show_plots)
            

            input_point = (input_width_index,input_height_index)
            output_point = (output_width_index,output_height_index)
            self.set_um_per_pixel(input_point,output_point)
        
        window_num_pixel_height = np.shape(image_array)[1]  # 2048
        window_num_pixel_width = np.shape(image_array)[0]  # 2448
         
        # Change these to cut out the laser from the left and how far you want to go to the right
        left_indent = input_width_index + input_indent
        right_indent = output_width_index - output_indent
        top_indent = input_height_index - (window_num_pixel_height/20)
        
        
        if top_indent < 0:
            top_indent = 0
                
        bottom_indent = input_height_index + (window_num_pixel_height/20)
        
        if bottom_indent > window_num_pixel_height:
            bottom_indent = window_num_pixel_height
        
        
        
        
        cropped_image = image.crop((left_indent, top_indent, right_indent, bottom_indent))
        cropped_image_array = np.asarray(cropped_image)
 
       
        # Find the waveguide
        left_index_guess = 175
        
        number_of_points = 15
        
        #separation = 70
        separation = int((right_indent-left_indent-left_index_guess)/number_of_points)
        
        angle, angle_params, x_max_index_array, y_max_index_array = find_waveguide_angle(cropped_image_array[:, :, 2], left_index_guess, separation, number_of_points,self.show_plots)
 
        # Rotate picture and plot it with the upper and lower limit

        left_indent = left_indent
        right_indent = right_indent
        top_indent = top_indent
        bottom_indent = bottom_indent
        rotated_image = image.rotate(-angle, center=(left_indent, int(angle_params[1]) + top_indent)).crop((left_indent, top_indent, right_indent, bottom_indent))
 
        rotated_image_array = np.asarray(rotated_image)
        
        
        upper = int(angle_params[1] + interval/2)
        lower = int(angle_params[1] - interval/2)
        #cropped_array = rotated_image_array[lower:upper, :, 2]
 
        #shape_cropped_array = np.shape(cropped_array)
 
        x_mu_array = np.arange(np.shape(rotated_image_array)[1]) * self.mum_per_pixel
        y_mu_array = np.arange(np.shape(rotated_image_array)[0]) * self.mum_per_pixel
 
        upper_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * upper).astype("int")
        lower_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * lower).astype("int")   
 
        if self.show_plots:
            plt.figure(figsize=(10,6))
            #plt.ylim([1000,2000])
            #plt.xticks([])
            #plt.yticks([])
            #plt.title("Original Image with cropped section")
            plt.plot((left_indent,left_indent),(top_indent,bottom_indent),"r")
            plt.plot((left_indent,right_indent),(bottom_indent,bottom_indent),"r")
            plt.plot((left_indent,right_indent),(top_indent,top_indent),"r")
            plt.plot((right_indent,right_indent),(top_indent,bottom_indent),"r")
            plt.imshow(image)
            
            
        
            #plt.imshow(get_intensity_array(cropped_image_array.copy()), cmap="jet", vmin=0, vmax=10, interpolation='spline16', extent=[right_indent, left_indent, bottom_indent, top_indent])
            
            plt.figure()
            plt.imshow(get_intensity_array(cropped_image_array.copy()), cmap="jet", vmin=0, vmax=10, interpolation='spline16', extent=[x_mu_array[0], x_mu_array[-1], y_mu_array[0], y_mu_array[-1]])
            plt.plot(x_mu_array[x_max_index_array], y_mu_array[y_max_index_array],'r.')
            plt.plot([x_mu_array[0], x_mu_array[-1]], [angle_params[1]*self.mum_per_pixel, (angle_params[0]*len(x_mu_array) + angle_params[1])*self.mum_per_pixel],'r-')
            #plt.title("Cropped")
            plt.xlabel('x [um]')
            plt.ylabel('y [um]')
     
            # Plot rotated picture
            plt.figure()
            plt.imshow(get_intensity_array(rotated_image_array), cmap="jet", vmin=0, vmax=10, extent=[x_mu_array[0], x_mu_array[-1], y_mu_array[0], y_mu_array[-1]])
            #plt.title("Rotated Image")
            plt.xticks([])
            plt.yticks([])
            #plt.xlabel('x [um]')
            #plt.ylabel('y [um]')
            #plt.colorbar(fraction=0.016, pad=0.01)
            plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[upper_index_array], 'r-')
            plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[lower_index_array], 'r-')
 

    
        return rotated_image_array, x_mu_array, y_mu_array, upper, lower
    
    
    def analyze_image(self, image,input_indent,output_indent,interval,num_neighbors, threshold_factor=1.5):
        
        rotated_image_array, x_mu_array, y_mu_array, upper, lower = self.crop_and_rotate(image,input_indent,output_indent,interval)
        
        cropped_image_height = np.shape(rotated_image_array)[0]
        
        x = x_mu_array 
        

        image_data_raw = np.sum(rotated_image_array,2)
        
        cropped_image = image_data_raw[cropped_image_height - upper: cropped_image_height - lower, :]
        
        mean_image = np.mean(cropped_image)
        #cropped_image[cropped_image < mean_image*threshold_factor] = 0
        
        y_raw = np.sum(cropped_image, axis=0)
        
        smoothing = 10
        x_iqr,y_iqr = self.remove_outliers_IQR(x, y_raw, smoothing,num_neighbors) 
        
        y_exp = self.EMA(y_iqr,0.01)
        x_exp = x_iqr[:len(y_exp)]
        
        y_savgol = savgol_filter(y_iqr,501,1,mode="nearest")
        
        fit_x = np.delete(x_iqr, [])
        fit_y = np.delete(y_savgol, [])
        
        initial_guess = [25, 0.0006,np.mean(fit_y[-10:])]
        fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier, = curve_fit(exponential_function_offset, fit_x, fit_y, p0=initial_guess, full_output=True) # sigma=weights, absolute_sigma=True
        fit = exponential_function_offset(fit_x, fit_parameters[0], fit_parameters[1],fit_parameters[2])
        
        fit_upper,fit_lower, alpha_upper, alpha_lower = self.calculate_confidence_interval(fit_parameters, fit_parameters_cov_var_matrix, fit_x, 1.960)
        
        residuals = fit_y - exponential_function_offset(fit_x, *fit_parameters)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((fit_y-np.mean(fit_y))**2)
        r_squared = 1 - (ss_res/ss_tot)
        
        alpha_dB = 10 * np.log10(np.exp(fit_parameters[1] * 1e4))

        alpha_upper = 10 * np.log10(np.exp((alpha_upper) * 1e4))
        alpha_lower = 10 * np.log10(np.exp((alpha_lower) * 1e4))
        
        if self.show_plots:

            
            #image_data, background = self.remove_background(image_data_raw)
            #y = np.mean(image_data[cropped_image_height - upper: cropped_image_height - lower, left_saturation_crop:right_saturation_crop], axis=0)
            
            plt.figure(figsize=(10,6))
            plt.plot(x, y_raw, 'b-', label="Raw data")
            plt.legend()
            plt.xlabel('x Length [um]')
            #plt.ylim([0, np.max(y_raw)])
            plt.ylabel('Sum of pixel intensities')
            plt.show()
            
            plt.figure(figsize=(10,6))
            plt.plot(fit_x, fit_y, 'b-', label="Savitzky–Golay smoothed and outlier removed data")
            plt.plot(fit_x, fit, 'r-', label=f"Fit with: {alpha_dB:.3f} dB/cm +- {alpha_dB-alpha_lower:.3f}, R\u00b2: {r_squared:.3f}")
            plt.plot(fit_x, fit_upper, 'r', linestyle='dashed', label="95% Confidence Bound")
            plt.plot(fit_x, fit_lower, 'r', linestyle='dashed')
            plt.legend()
            plt.xlabel('x Length [um]')
            plt.ylabel('Sum of pixel intensities')
            plt.show()
            
            
            plt.figure(figsize=(10,6))
            plt.plot(x, y_raw, 'b-', label="Raw data")
            plt.plot(x_iqr,y_iqr,"y-",label="IQR outlier removal")
            #plt.plot(x_mov,y_mov,"r-",label=f"Moving average, window length: {sum_width}")
            #plt.plot(x_exp,y_exp, "g-",label="Exponential Moving Average")
            #plt.axhline(background*higher,label="Background", color="y")
            plt.plot(x_iqr,y_savgol,label="Savgol filter",color="r")
            plt.xlabel('x Length [um]')
            plt.ylabel('Sum of pixel intensities')
            plt.legend()
            plt.show()
            #plt.savefig()
            
            
            #window = signal.windows.tukey(len(y_raw),0.1)
            #y_win = y_raw*window
            #y_fft = abs(fftshift(fft(y_win)))
            #freq = fftshift(fftfreq(len(y_win)))
            #middle = int((len(y_fft)-1)/2)
            #plt.figure(figsize=(10,6))
            #y_fft[middle:middle+2] = 0
            #plt.plot(y_fft[middle:], 'b-', label="FFT of data")
            #plt.yscale("log")
            #plt.xlabel('Frequency [Hz]')
            #plt.ylabel('Amplitude')
            #plt.legend()
            #plt.show()
            
            #self.plot_histogram(rotated_image_array)
        
            print("Fit Parameters:", fit_parameters)
            print("Variance-Covariance Matrix Fit Parameters:", fit_parameters_cov_var_matrix)
            print(
                f'a={fit_parameters[0]} +- {np.sqrt(fit_parameters_cov_var_matrix[0, 0])}, b={fit_parameters[1]} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1])}')
            print(f"alpha = {fit_parameters[1] * 1e4} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4} 1/cm")
            print(
                f'alpha_dB = {10 * np.log10(np.exp(fit_parameters[1] * 1e4))} +- {10 * np.log10(np.exp(np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4))}) dB/cm')
            print(f'Length over measurement = {fit_x[-1] - fit_x[0]} um')
            print(f"R\u00b2 : {r_squared}")
        
       
        return alpha_dB, r_squared, alpha_upper, alpha_lower, fit_x, fit_y
