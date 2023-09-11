from scipy.optimize import curve_fit
from scipy.signal import find_peaks

from functions import *
import scipy.signal

# Path the pictures are at
path = 'Pictures/'

# Load Image
picture_index = 27
pictures = print_files(path, 'bmp')
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

# Chip Detection
find_chip(original_image)

plt.show()