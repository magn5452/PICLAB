################################################################
# Qversion, Toptica running - Emil Z. Ulsig, Magnus L. Madsen, ECE AU
# Last Updated March 6th 2023
################################################################


from Python_lib.Resource_Manager_Stub import Resource_Manager_Stub
from Python_lib.Setup_Factories import Setup_Stub_Factory, Setup_Toptica_Factory
from Python_lib.Thorlabs_Stub import Thorlabs_Stub
from Python_lib.Toptica_Stub import Toptica_Stub
from Python_lib.Toptica_CTL950 import *
from Python_lib.Thorlabs_PM100U import Thorlabs_PM100U
# from Python_lib.Yokogawa import Yokogawa
import tkinter as tk
from tkinter import ttk
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import h5py
import datetime
import pyvisa as visa


def power_W_to_dBm(power_W):
    return 10 * np.log10(power_W * 1000)


# sys.exit()
################################################################
# Scan settings

setup_factory = Setup_Toptica_Factory()  # Change to Setup_Stub_Factory for testing purposes

chip = ''
device = ''
add_info = 'normalization'
scan = ''

toptica_power_mW = 20  # Toptica output power [mW]
toptica_current_mA = 15  # Toptica current [mA]
toptica_wavelength_nm = 980  # Toptica wavelength [mm]
initial_wavelength_nm = toptica_wavelength_nm  # Toptica initial wavelength [nm]

toptica_wavelength_min_nm = 910  # [nm]
toptica_wavelength_max_nm = 980  # [nm]

step_size = 1  # [nm]

wavelength_array = np.arange(toptica_wavelength_min_nm, toptica_wavelength_max_nm + 0.01, step_size, dtype=float)

wav_nm = (toptica_wavelength_max_nm + toptica_wavelength_min_nm) / 2
wav_PD_nm = wav_nm  # [nm]

beginning_time = datetime.datetime.now()
filename = beginning_time.strftime("%Y-%m-%d_%H-%M-%S") + \
           chip + \
           device + \
           scan + \
           '_Run_' + \
           str(toptica_power_mW) + 'mW_' + \
           str(toptica_wavelength_nm) + 'nm_' + add_info

################################################################
# Initialize
detector_units = 'W'  # dBm or W, dBm may not work
# resource_manager = Resource_Manager_Stub()
resource_manager = setup_factory.create_resource_manager()
resource_list = resource_manager.list_resources()
print("Resources: " + str(resource_list))

# Input detectors
detector_list = []

for address in resource_manager.list_resources():
    try:
        print(address, '-->', resource_manager.open_resource(address).query('*IDN?').strip())
        detector = setup_factory.create_detector(resource_manager, address)
        detector.set_wavelength_nm(initial_wavelength_nm)
        detector.set_units(detector_units)
        detector_list.append(detector)

    except visa.VisaIOError:
        pass

detector_in_1 = detector_list[0]
detector_in_2 = detector_list[1]
detector_out = Thorlabs_Stub()

# Laser controller
toptica_laser = setup_factory.create_laser()
toptica_laser.set_power_stabilization_status(True)
toptica_laser.set_power_stabilization_parameters(0.3, 15, 0, 1)
toptica_laser.set_wavelength_nm(toptica_wavelength_nm)
# toptica_laser.set_current(toptica_current_mA)
toptica_laser.set_power_mW(toptica_power_mW)
toptica_laser.print_emission_status()


def end_acquisition():
    global acquisition_flag
    running_flag = False


def data_acquisition_window():
    popup = tk.Tk()
    popup.wm_title("Data acquisition")
    msg = "Aquisition running..."
    label = ttk.Label(popup, text=msg, font="Arial")
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="End acquisition", command=end_acquisition)
    B1.pack()
    w = 400  # width for the Tk root
    h = 100  # height for the Tk root
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (w / 2)
    y = hs - h - 50
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return popup, ws, hs


def set_step_wavelength(step):
    global tune_step_wavelength
    tune_step_wavelength = float(step)


def set_step_power(step):
    global tune_step_power
    tune_step_power = float(step)


def set_wavelength(laser, detector_list, wavelength):
    if (wavelength <= 980) and (wavelength >= 910):
        laser.set_wavelength_nm(wavelength)
        for detector in detector_list:
            detector.set_wavelength_nm(wavelength)
    else:
        print("Error: " + str(round(wavelength, 1)) + " is not within the range 910-980nm")


def update_label(label, laser):
    msg = "Wavelength = %0.2f nm" % (laser.get_detector_wavelength()) + " Power = %0.2f mW" % (laser.get_detector_power())
    label.config(text=msg)


def tune_laser_window_button(laser, detector_list, step, label):
    current_wavelength = laser.get_detector_wavelength()
    update_wavelength = current_wavelength + step
    set_wavelength(laser, detector_list, update_wavelength)
    update_label(label, laser)


def button_1_2(laser, detector_list, step, label):
    current_wavelength = laser.get_detector_wavelength()
    update_wavelength = current_wavelength + step
    set_wavelength(laser, detector_list, update_wavelength)
    update_label(label, laser)


def button3(entry, laser, detector_list, label):
    set_wavelength(laser, detector_list, get_float_from_string(entry.get(), laser.get_detector_wavelength()))
    update_label(label, laser)


def button4(entry, button_1, button_2):
    set_step_wavelength(get_float_from_string(entry.get(), tune_step_wavelength))
    button_1.configure(text="+" + str(tune_step_wavelength) + " nm")
    button_2.configure(text="-" + str(tune_step_wavelength) + " nm")


def button_5_6(laser, step, label):
    current_power = laser.get_detector_power()
    update_power = current_power + step
    laser.set_power_mW(update_power)
    update_label(label, laser)


def button7(entry, laser, label):
    laser.set_power_mW(get_float_from_string(entry.get(), laser.get_detector_power()))
    update_label(label, laser)


def button8(entry, button_5, button_6):
    set_step_power(get_float_from_string(entry.get(), tune_step_power))
    button_5.configure(text="+" + str(tune_step_power) + " mW")
    button_6.configure(text="-" + str(tune_step_power) + " mW")


def tune_laser_window(toptica_laser, detector_list):
    popup = tk.Tk()
    popup.wm_title("Tune Laser")
    window_width = 400  # width for the Tk root
    window_height = 230  # height for the Tk root
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = ws - window_width * 2
    y = hs - window_height - 50
    popup.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

    msg = "Wavelength = %0.2f nm" % (toptica_laser.get_detector_wavelength()) + " Power = %0.2f mW" % (toptica_laser.get_detector_power())
    label = ttk.Label(popup, text=msg, font="Arial")
    label.pack(side="top", fill="x", pady=10)

    global tune_step_wavelength
    tune_step_wavelength = 1.0
    button_1 = ttk.Button(popup)
    button_1["text"] = "+" + str(tune_step_wavelength) + " nm"
    button_1["command"] = lambda: button_1_2(toptica_laser, detector_list, tune_step_wavelength, label)
    button_1.pack(side='right', fill='y')

    button_2 = ttk.Button(popup)
    button_2["text"] = "-" + str(tune_step_wavelength) + " nm"
    button_2["command"] = lambda: button_1_2(toptica_laser, detector_list,
                                             -tune_step_wavelength, label)
    button_2.pack(side='left', fill='y')

    global tune_step_power
    tune_step_power = 1.0
    button_5 = ttk.Button(popup)
    button_5["text"] = "+" + str(tune_step_power) + " mW"
    button_5["command"] = lambda: button_5_6(toptica_laser, tune_step_power, label)
    button_5.pack(side='right', fill='y')

    button_6 = ttk.Button(popup)
    button_6["text"] = "-" + str(tune_step_power) + " mW"
    button_6["command"] = lambda: button_5_6(toptica_laser, -tune_step_power, label)
    button_6.pack(side='left', fill='y')

    entry_1 = ttk.Entry(popup)
    button_3 = ttk.Button(popup)
    button_3["text"] = "Go to [nm]"
    button_3["command"] = lambda: button3(entry_1, toptica_laser, detector_list, label)
    button_3.pack(fill='y')
    entry_1.pack()

    entry_2 = ttk.Entry(popup)
    button_4 = ttk.Button(popup)
    button_4["text"] = "Set step [nm]"
    button_4["command"] = lambda: button4(entry_2, button_1, button_2)
    button_4.pack(fill='y')
    entry_2.pack()

    entry_3 = ttk.Entry(popup)
    button_7 = ttk.Button(popup)
    button_7["text"] = "Go to [mW]"
    button_7["command"] = lambda: button7(entry_3, toptica_laser, label)
    button_7.pack(fill='y')
    entry_3.pack()

    entry_4 = ttk.Entry(popup)
    button_8 = ttk.Button(popup)
    button_8["text"] = "Set step [mW]"
    button_8["command"] = lambda: button8(entry_4, button_5, button_6)
    button_8.pack(fill='y')
    entry_4.pack()

    return popup


def get_float_from_string(str, original_step):
    if str == '':
        return original_step
    else:
        return float(str)


SMALL_SIZE, MEDIUM_SIZE, BIGGER_SIZE = 22, 24, 26
LW, MS, MEW = 2.0, 5.0, 0.5
mpl.rcParams['font.sans-serif'] = "Arial"
plt.rc('font', size=MEDIUM_SIZE)
plt.rc('axes', titlesize=MEDIUM_SIZE, labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE)
mpl.use("TkAgg")  # set the backend
yrange, xrange = 2, 45  # [dB] +/-, [s]

SMALL_SIZE, MEDIUM_SIZE, BIGGER_SIZE = 22, 24, 26
LW, MS, MEW = 2.0, 5.0, 0.5
mpl.rcParams['font.sans-serif'] = "Arial"
plt.rc('font', size=MEDIUM_SIZE)
plt.rc('axes', titlesize=MEDIUM_SIZE, labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE)
mpl.use("TkAgg")  # set the backend
yrange, xrange = 2, 45  # [dB] +/-, [s]

## Transmission alignment

split_ratio = 0.0  # [dB]

power_in_1_list, power_in_2_list, power_out_list, power_dB_out_list, power_dBm_out_list, power_max_list, power_running_max_list, power_running_mean_list, time_list = [], [], [], [], [], [], [], [], []
T0 = datetime.datetime.now()
T = T0 - T0


power_in_1 = detector_in_1.get_detector_power()
power_in_1_list.append(power_in_1)

power_in_2 = detector_in_2.get_detector_power()
power_in_2_list.append(power_in_2)

power_out = detector_out.get_power()
power_out_list.append(power_out)

power_dB_out = 10 * np.log10(power_out / power_in_1) - split_ratio
power_dB_out_list.append(power_dB_out - split_ratio)

power_dBm_out = power_W_to_dBm(power_out)
power_dBm_out_list.append(power_dBm_out)

power_max = power_dBm_out
power_max_list.append(power_max)
power_running_max_list.append(power_max)

power_running_mean = power_dBm_out
power_running_mean_list.append(power_running_mean)

time_list.append(T.seconds + T.microseconds / 1e6)

y_c = int(power_dB_out) + (power_dB_out % 1 > 0)

pm, ws, hs = data_acquisition_window()
pt = tune_laser_window(toptica_laser, detector_list)

fig, ax = plt.subplots(ncols=1, nrows=1)
points_plot, = ax.plot(time_list, power_dBm_out_list,
                       marker='o', linestyle='-', color='red',
                       lw=LW, ms=MS, mec='k', mew=MEW)
power_max_plot, = ax.plot(time_list, power_max_list,
                          marker='', linestyle='-', color='blue',
                          lw=LW, ms=MS, mec='k', mew=MEW)

# power_running_max_plot, = ax.plot(time_list, power_running_max_list,
#                          marker='', linestyle='-', color='magenta',
#                          lw=LW, ms=MS, mec='k', mew=MEW)

power_running_mean_plot, = ax.plot(time_list, power_running_mean_list,
                                   marker='', linestyle='-', color='green',
                                   lw=LW, ms=MS, mec='k', mew=MEW)
ax.set(xlabel='Time (s)', ylabel='Power (dBm)',
       title="Power detektor 1: " + str(np.round(10 * np.log10(power_in_1), 3)) + " [dBm], Power detektor 2: " + str(
           np.round(10 * np.log10(power_in_2), 3)) + " [dBm], Power detektor out: " + str(
           np.round(10 * np.log10(power_out), 3)) + " [dBm]")
ax.grid()
DPI = fig.get_dpi()

fig.set_size_inches((ws - 80) / DPI, (hs - 200) / DPI, forward=True)
fig.canvas.manager.window.wm_geometry('+80+0')

acquisition_flag = True  # Global flag
while acquisition_flag:
    pause_value = 0.01
    T = datetime.datetime.now() - T0
    T_up = T.seconds + T.microseconds / 1e6

    power_in_1 = detector_in_1.get_detector_power()
    power_dBm_in_1 = power_W_to_dBm(np.array(power_in_1))
    power_in_1_list.append(power_in_1)

    power_in_2 = detector_in_2.get_detector_power()
    power_dBm_in_2 = power_W_to_dBm(np.array(power_in_2))
    power_in_2_list.append(power_in_2)

    power_out = detector_out.get_power()
    power_out_list.append(power_out)

    power_dB_out = 10 * np.log10(power_out / power_in_1) - split_ratio
    power_dB_out_list.append(power_dB_out)

    power_dBm_out = power_W_to_dBm(np.array(power_out))
    power_dBm_out_list.append(power_dBm_out)

    time_list.append(T_up)
    points_plot.set_data(time_list, power_dBm_out_list)

    power_max = max(power_dBm_out_list)
    power_max_list.append(power_max)
    power_max_plot.set_data(time_list, power_max_list)

    # power_running_max_list.append(np.max(power_dBm_out_list[int(-1/pause_value):]))
    # power_running_max_plot.set_data(time_list,power_running_max_list)

    power_running_mean_list.append(np.mean(power_dBm_out_list[int(-1 / pause_value):]))
    power_running_mean_plot.set_data(time_list, power_running_mean_list)

    ax.set_xlim([T_up - xrange, T_up])
    if power_dBm_out > (y_c + (yrange - 0.1)):
        y_c = int(power_dBm_out)
    if power_dBm_out < (y_c - (yrange - 0.1)):
        y_c = int(power_dBm_out + 1)

    ax.set_ylim([y_c - yrange, y_c + yrange])
    ax.set_title(
        "Power detektor 1: " + str(np.round(power_dBm_in_1, 3)) + " [dBm], Power detektor 2: " + str(
            np.round(power_dBm_in_2, 3)) + " [dBm], Power detektor out: " + str(
            np.round(power_dBm_out, 3)) + " [dBm]")

    plt.pause(pause_value)

pm.destroy()
pt.destroy()
plt.close(fig)

################################################################
# Run sweep

power_W_in_1_list, power_W_out_list, power_dBm_out_list, x = [], [], [], []

power_W_in_1 = detector_in_1.get_detector_power()
power_W_in_1_list.append(power_W_in_1)

power_W_out = detector_out.get_power()
power_W_out_list.append(power_W_out)
power_dBm_out = power_W_to_dBm(power_W_out)

power_dB = 10 * np.log10(power_W_out / power_W_in_1)
power_dB_split = 10 * np.log10(np.array(power_W_out_list) / np.array(power_W_in_1_list)) - split_ratio

power_dBm_out_list.append(power_dBm_out)

x.append(wavelength_array[0])

figL, ax = plt.subplots()
points, = ax.plot(x, power_dBm_out_list,
                  marker='o', linestyle='-', color='blue',
                  lw=LW, ms=MS, mec='k', mew=MEW)

ax.set(xlabel='Wavelength (nm)', ylabel='Power (dBm)')
ax.grid()
ax.set_xlim([toptica_wavelength_min_nm, toptica_wavelength_max_nm])
DPI = figL.get_dpi()
figL.set_size_inches((ws - 80) / DPI, (hs - 200) / DPI, forward=True)
figL.canvas.manager.window.wm_geometry('+80+0')

for kk in range(len(wavelength_array)):
    detector_in_1.set_wavelength_nm(round(wavelength_array[kk], 1))
    detector_in_2.set_wavelength_nm(round(wavelength_array[kk], 1))
    detector_out.set_wavelength(round(wavelength_array[kk], 1))
    toptica_laser.set_wavelength_nm(round(wavelength_array[kk], 1))
    plt.pause(0.1)
    power_W_in_1 = detector_in_1.get_detector_power()
    power_W_in_1_list.append(power_W_in_1)

    power_W_out = detector_out.get_power()
    power_W_out_list.append(power_W_out)

    power_dB = 10 * np.log10(power_W_out / power_W_in_1) - split_ratio
    power_dB_split = 10 * np.log10(np.array(power_W_out_list) / np.array(power_W_in_1_list)) - split_ratio

    P_dBm_up = 10 * np.log10(power_W_out * 1e3)
    power_dBm_out_list = 10 * np.log10(np.array(power_W_out_list) * 1e3)

    x.append(wavelength_array[kk])
    points.set_data(x, power_dBm_out_list)

    ax.set_ylim([min(power_dBm_out_list), max(power_dBm_out_list)])

    plt.pause(0.1)

plt.close()

################################################################
# Save data

header = \
    "#\n# Date: %s\n#\n" % beginning_time.strftime("%Y-%m-%d_%H-%M-%S") + \
    "# Scan type: %s\n" % scan + \
    "# Chip: %s\n" % chip + \
    "# Device: %s\n" % device + \
    "# Additional info: %s\n#\n" % add_info + \
    "# Alignment wavelength: %s nm\n#\n" % toptica_wavelength_nm + \
    "# Input detector: %s\n" % detector_in_1.info[0:-1] + \
    "# Output detector: %s\n" % detector_out.info[0:-1] + \
    "# Laser: Toptica\n"

# Transmission alignment


fig.savefig("Figures/" + filename + "_L.pdf", bbox_inches='tight')
hf = h5py.File('Data/' + filename + '_L.h5', 'w')
hf.create_dataset('Header', data=header)
hf.create_dataset('Time', data=time_list)
hf.create_dataset('P_in_W', data=power_in_1_list)
hf.create_dataset('P_out_W', data=power_out_list)
hf.close()

################################################################
# Finalize equipment

toptica_laser.close()
detector_in_1.close()
detector_in_2.close()
detector_out.close()

################################################################
# End

ending_time = datetime.datetime.now()
elapsed = ending_time - beginning_time
elapsed_min = int(elapsed.seconds / 60)
elapsed_sec = elapsed.seconds - elapsed_min * 60

print("Elapsed time = {0:2d} minutes {1:2d} seconds".format(elapsed_min, elapsed_sec))

################################################################
