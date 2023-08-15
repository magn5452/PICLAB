################################################################
# Qversion, Toptica running - Emil Z. Ulsig, Magnus L. Madsen, ECE AU
# Last Updated March 6th 2023
################################################################
import GUI
from GUI import *
from Python_lib.Resource_Manager_Stub import Resource_Manager_Stub
from Python_lib.Setup_Factories import Setup_Stub_Factory,  Setup_EXFO_Factory
# from Python_lib.Yokogawa import Yokogawa
import tkinter as tk
from tkinter import ttk
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import h5py
import datetime
import pyvisa as visa

from Python_lib.Thorlabs_Stub import Thorlabs_Stub
from Python_lib.Toptica_CTL950 import Toptica_CTL950
from Python_lib.Toptica_Stub import Toptica_Stub

# sys.exit()
################################################################
# Scan settings

setup_factory = Setup_EXFO_Factory()  # Change to Setup_Stub_Factory for testing purposes

scan = ''
chip = ''
component = ''
add_info = 'EXFO_WDM_test'

## Set parameters
# EXFO
exfo_power_mW = 30  # EXFO output power [mW]
exfo_wavelength_nm = 1550  # EXFOwavelength [mm]
exfo_initial_wavelength_nm = exfo_wavelength_nm  # EXFO initial wavelength [nm]

exfo_wavelength_min_nm = 1540  # [nm]
exfo_wavelength_max_nm = 1630  # [nm]

step_size = 0.5  # [nm]
exfo_sweep_speed = 10 # [nm/s]

wavelength_array = np.arange(exfo_wavelength_min_nm, exfo_wavelength_max_nm + 0.01, step_size, dtype=float)

wav_nm = (exfo_wavelength_max_nm + exfo_wavelength_min_nm) / 2
wav_PD_nm = wav_nm  # [nm]



beginning_time = datetime.datetime.now()
filename = beginning_time.strftime("%Y-%m-%d_%H-%M-%S") + \
           chip + \
           component + \
           scan + \
           '_Run_' + \
           str(exfo_power_mW) + 'mW_' + \
           str(exfo_wavelength_nm) + 'nm_' + add_info

################################################################
# Initialize

detector_units = 'W'  # dBm or W, dBm may not work
# resource_manager = Resource_Manager_Stub()
resource_manager = setup_factory.create_resource_manager()
resource_list = resource_manager.list_resources()
print("Resources: " + str(resource_list))

################################################################
# Laser controller
exfo_laser = setup_factory.create_laser(resource_manager)
exfo_laser.set_power_unit_mW()
exfo_laser.automatic_power_control()
exfo_laser.set_sweep_speed(exfo_sweep_speed)
exfo_laser.set_wavelength_nm(exfo_wavelength_nm)
exfo_laser.set_power_mW(exfo_power_mW)
exfo_laser.laser_on()

toptica_laser = Toptica_Stub()
toptica_laser.set_power_stabilization_status(True)
toptica_laser.set_power_stabilization_parameters(0.3, 15, 0, 1)
toptica_laser.set_wavelength(940)
# toptica_laser.set_current(toptica_current_mA)
toptica_laser.set_power(70)
toptica_laser.print_emission_status()

################################################################
# Input detectors
thorlabs_PM101U_in_1 = 'USB0::0x1313::0x8076::M00905455::INSTR'
detector_in_1 = exfo_laser
detector_in_1.set_wavelength_nm(exfo_initial_wavelength_nm)
#detector_in_1.set_units(detector_units)
#detector_in_1.set_averaging(10)
# detector_in_1_.zero()

thorlabs_PM101U_in_2 = 'USB0::0x1313::0x8076::M00905455::INSTR'
#detector_in_2 = setup_factory.create_detector(resource_manager, thorlabs_PM101U_in_2)
detector_in_2 = Thorlabs_Stub()
detector_in_2.set_wavelength(exfo_initial_wavelength_nm)
detector_in_2.set_units(detector_units)
detector_in_2.set_averaging(10)
# detector_in_2.zero()


## Output detector
thorlabs_PM101U_out = 'USB0::0x1313::0x8076::M00905456::INSTR'
detector_out = setup_factory.create_detector(resource_manager, thorlabs_PM101U_out)
detector_out.set_wavelength_nm(exfo_initial_wavelength_nm)
detector_out.set_units(detector_units)
detector_out.set_averaging(10)
# detector_out.zero()

detector_list = [detector_in_1, detector_in_2, detector_out]

detector_plot = detector_list[GUI.detector_plot_index]

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

power_in_1_list, power_in_2_list, power_out_list, power_dB_out_list, power_dBm_out_sweep_list, power_dBm_plot_sweep_list, power_dBm_max_plot_list, power_running_max_list, power_running_mean_list, time_list = [], [], [], [], [], [], [], [], [], []
T0 = datetime.datetime.now()
T = T0 - T0

power_in_1 = detector_in_1.get_detector_power()
power_in_1_list.append(power_in_1)

power_in_2 = detector_in_2.get_power()
power_in_2_list.append(power_in_2)

power_out = detector_out.get_detector_power()
power_out_list.append(power_out)

power_dB_out = power_to_dB(power_out, power_in_1) - split_ratio
power_dB_out_list.append(power_dB_out - split_ratio)

power_dBm_out = power_W_to_dBm(power_out)
power_dBm_out_sweep_list.append(power_dBm_out)

power_dBm_plot = power_dBm_out
power_dBm_plot_sweep_list.append(power_dBm_plot)

power_dBm_max_plot = power_dBm_out
power_dBm_max_plot_list.append(power_dBm_max_plot)
power_running_max_list.append(power_dBm_max_plot)

power_running_mean = power_dBm_out
power_running_mean_list.append(power_running_mean)

time_list.append(T.seconds + T.microseconds / 1e6)

y_c = int(power_dB_out) + (power_dB_out % 1 > 0)

# Windows

pi = increment_detector_window(detector_list)
pm, ws, hs = data_acquisition_window()
pt = tune_laser_window(exfo_laser, detector_list)

# Plot
fig, ax = plt.subplots(ncols=1, nrows=1)
points_plot, = ax.plot(time_list, power_dBm_out_sweep_list,
                       marker='o', linestyle='-', color='red',
                       lw=LW, ms=MS, mec='k', mew=MEW)
power_max_plot, = ax.plot(time_list, power_dBm_max_plot_list,
                          marker='', linestyle='-', color='blue',
                          lw=LW, ms=MS, mec='k', mew=MEW)

ax.set(xlabel='Time (s)', ylabel='Power (dBm)',
       title="Power detektor 1: " + str(np.round(power_W_to_dBm(power_in_1), 3)) + " [dBm], Power detektor 2: " + str(
           np.round(power_W_to_dBm(power_in_2), 3)) + " [dBm], Power detektor out: " + str(
           np.round(power_W_to_dBm(power_out), 3)) + " [dBm]")

ax.grid()
DPI = fig.get_dpi()

fig.set_size_inches((ws - 80) / DPI, (hs - 200) / DPI, forward=True)
fig.canvas.manager.window.wm_geometry('+80+0')

while GUI.acquisition_flag:
    pause_value = 0.01
    T = datetime.datetime.now() - T0
    T_up = T.seconds + T.microseconds / 1e6

    #print(exfo_laser.get_power())
    # Detector lists
    power_in_1 = detector_in_1.get_detector_power()
    power_dBm_in_1 = power_W_to_dBm(np.array(power_in_1))
    power_in_1_list.append(power_in_1)

    power_in_2 = detector_in_2.get_power()
    power_dBm_in_2 = power_W_to_dBm(np.array(power_in_2))
    power_in_2_list.append(power_in_2)

    power_out = detector_out.get_detector_power()
    power_out_list.append(power_out)

    power_dB_out = power_to_dB(power_out, power_in_1) - split_ratio
    power_dB_out_list.append(power_dB_out)

    power_dBm_out = power_W_to_dBm(np.array(power_out))
    power_dBm_out_sweep_list.append(power_dBm_out)

    # Update Plot
    time_list.append(T_up)
    detector_plot = detector_list[GUI.detector_plot_index]
    power_dBm_plot = power_W_to_dBm(detector_plot.get_power())
    power_dBm_plot_sweep_list.append(power_dBm_plot)
    points_plot.set_data(time_list, power_dBm_plot_sweep_list)

    # x_left_limit_index = int((T_up - xrange)/pause_value)
    x_left_limit_index = 0
    power_dBm_max_plot = max(power_dBm_plot_sweep_list[x_left_limit_index: -1])
    power_dBm_max_plot_list.append(power_dBm_max_plot)
    power_max_plot.set_data(time_list, power_dBm_max_plot_list)

    ax.set_xlim([T_up - xrange, T_up])
    if power_dBm_plot > (y_c + (yrange - 0.1)):
        y_c = int(power_dBm_plot)
    if power_dBm_plot < (y_c - (yrange - 0.1)):
        y_c = int(power_dBm_plot + 1)

    ax.set_ylim([y_c - yrange, y_c + yrange])
    title_string = ""
    for detector in detector_list:
        power_W = detector.get_power()
        title_string += "Power " + detector.get_name() + ": " + \
                        str(np.round(power_W_to_dBm(power_W), 3)) + " [dBm], " + \
                        str(np.round(power_W * 1000, 3)) + " [mW], "
    ax.set_title(title_string)
    plt.pause(pause_value)

pi.destroy()
pt.destroy()
plt.close(fig)

################################################################

if GUI.sweep_flag:
    # Run sweep

    power_W_in_1_sweep_list, power_W_in_2_sweep_list, power_W_out_sweep_list, power_dBm_plot_sweep_list = [], [], [], []

    power_W_in_1 = detector_in_1.get_detector_power()
    power_W_in_1_sweep_list.append(power_W_in_1)

    power_W_in_2 = detector_in_2.get_power()
    power_W_in_2_sweep_list.append(power_W_in_2)

    power_W_out = detector_out.get_detector_power()
    power_W_out_sweep_list.append(power_W_out)

    figL, ax = plt.subplots()
    points, = ax.plot(wavelength_array[0], 1,
                      marker='o', linestyle='-', color='blue',
                      lw=LW, ms=MS, mec='k', mew=MEW)

    ax.set(xlabel='Wavelength (nm)', ylabel='Power (dBm)')
    ax.grid()
    ax.set_xlim([exfo_wavelength_min_nm, exfo_wavelength_max_nm])
    DPI = figL.get_dpi()
    figL.set_size_inches((ws - 80) / DPI, (hs - 200) / DPI, forward=True)
    figL.canvas.manager.window.wm_geometry('+80+0')

    for wavelength_index in range(len(wavelength_array)):
        if GUI.sweep_flag:
            wavelength = round(wavelength_array[wavelength_index], 1)
            for detector in detector_list:
                detector.set_wavelength(wavelength)
            exfo_laser.set_wavelength_nm(wavelength)

            plt.pause(0.1)

            # Data Acquisition
            power_W_in_1 = detector_in_1.get_detector_power()
            power_W_in_1_sweep_list.append(power_W_in_1)

            power_W_in_2 = detector_in_2.get_power()
            power_W_in_2_sweep_list.append(power_W_in_2)

            power_W_out = detector_out.get_detector_power()
            power_W_out_sweep_list.append(power_W_out)

            # Plot
            power_dBm_plot_sweep_list.append(power_W_to_dBm(detector_list[GUI.detector_plot_index].get_power()))
            wavelength_array_plot = wavelength_array[0:wavelength_index]
            points.set_data(wavelength_array_plot, power_dBm_plot_sweep_list[0:wavelength_index])

            ax.set_ylim([min(power_dBm_plot_sweep_list), max(power_dBm_plot_sweep_list)])

            plt.pause(0.1)
        else:
            break

    plt.close()


    ''' #Procedure for continous sweep
        def continous_wavelengt_sweep(self, wl): #Change in wavelength [pm]
            #Set wavelength to wv_min
            self.set_wavelength(min(wl))
            #Set tuning speed
            self.set_sweep_speed(10)
            #Calling active cavity control will make the laser sweep to the next set wavelength
            self.active_cavity_control_on()
    
            self.set_wavelength(max(wl))
    
            self.active_cavity_control_off()
    
            self.active_cavity_control_off()
            return
    '''


    ################################################################
    # Save data
    if GUI.save_bool:
        header = \
            "#\n# Date: %s\n#\n" % beginning_time.strftime("%Y-%m-%d_%H-%M-%S") + \
            "# Scan type: %s\n" % scan + \
            "# Chip: %s\n" % chip + \
            "# Component: %s\n" % component + \
            "# Additional info: %s\n#\n" % add_info + \
            "# Alignment wavelength: %s nm\n#\n" % exfo_wavelength_nm + \
            "# Power laser: %s mW\n#\n" % exfo_power_mW + \
            "# Input detector: %s\n" % detector_in_1.info[0:-1] + \
            "# Output detector: %s\n" % detector_out.info[0:-1] + \
            "# Laser: %s\n" % exfo_laser.get_name()

        # Transmission alignment

        fig.savefig("Figures/" + filename + "_L.pdf", bbox_inches='tight')
        hf = h5py.File('Data/' + filename + '_L.h5', 'w')
        hf.create_dataset('Header', data=header)
        hf.create_dataset('Wavelength_nm', data=wavelength_array)
        hf.create_dataset('power_W_in_1_sweep_list', data=power_W_in_1_sweep_list)
        hf.create_dataset('power_W_in_2_sweep_list', data=power_W_in_2_sweep_list)
        hf.create_dataset('power_W_out_sweep_list', data=power_W_out_sweep_list)
        hf.close()

pm.destroy()

################################################################
# Finalize equipment

exfo_laser.close()
#detector_in_1.close()
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
