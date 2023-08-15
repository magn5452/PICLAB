import json
import tkinter as tk
from tkinter import ttk

import numpy as np

import pyvisa as visa
from matplotlib import pyplot as plt
import matplotlib as mpl

from GUI.functions import *
from Python_lib import *
import h5py
import datetime

from Python_lib.Agilent import Agilent
from Python_lib.Arroyo import Arroyo
from Python_lib.EXFO import EXFO
from Python_lib.Piezo_Controller_Visa import Piezo_Controller_Thorlabs
from Python_lib.Siglent import Siglent
from Python_lib.Thorlabs_PM100U import Thorlabs_PM100U
from Python_lib.Toptica_CTL950 import Toptica_CTL950
from Python_lib.Yokogawa import Yokogawa





class Sweep_Voltage_Plot_Window:
    def __init__(self, instrument_controller, gui_controller):
        self.folder = "Attenuation"
        self.scan = 'Voltage'  # Loss, DFG, SFG
        self.chip = 'Filter'  # STOA, STOB, ST1, ST2
        self.component = ''  # 1750nm_WG1, Loss_980,
        self.add_info = ''

        self.instrument_controller = instrument_controller
        self.gui_controller = gui_controller
        self.target_detector = None
        self.laser = None
        self.target_detector_index = 0
        self.detector_list = None
        self.waveform_generator = None

        self.fig = None

    def open(self):

        self.target_detector = self.instrument_controller.get_target_detector()
        self.target_detector_index = self.instrument_controller.get_target_detector()
        self.detector_list = self.instrument_controller.get_detector_list()
        self.laser = self.instrument_controller.get_target_laser()
        self.waveform_generator = self.instrument_controller.get_waveform_generator_list()[0]

        for detector in self.detector_list:
            detector.set_detector_wavelength(self.laser.get_wavelength())

        ws = 2000
        hs = 1500
        voltage_array = np.arange(self.instrument_controller.get_min_voltage(),
                                  self.instrument_controller.get_max_voltage() + self.instrument_controller.get_sweep_voltage(),
                                  self.instrument_controller.get_sweep_voltage(), dtype=float)

        LW, MS, MEW = 2.0, 5.0, 0.5

        rows, cols = (len(self.detector_list), len(voltage_array))

        power_W_array, power_dBm_array = np.empty([rows, cols]), np.empty([rows, cols])
        voltage_array_plot, power_W_plot_list, power_dBm_plot_list = [], [], []

        self.fig, ax = plt.subplots()
        points, = ax.plot(voltage_array[0], 1,
                          marker='o', linestyle='-', color='blue',
                          lw=LW, ms=MS, mec='k', mew=MEW)

        ax.set(xlabel='Voltage (V)', ylabel='Power (dBm)')
        ax.grid()
        ax.set_xlim([self.instrument_controller.get_min_voltage(), self.instrument_controller.get_max_voltage()])
        DPI = self.fig.get_dpi()
        self.fig.set_size_inches((ws - 80) / DPI, (hs - 200) / DPI, forward=True)
        self.fig.canvas.manager.window.wm_geometry('+80+0')

        for voltage_index in range(len(voltage_array)):
            voltage = round(voltage_array[voltage_index], 3)
            self.waveform_generator.set_voltage(voltage)
            plt.pause(0.1)
            # Data Acquisition
            for detector_index in range(0, len(self.detector_list)):
                detector = self.detector_list[detector_index]
                power_W = detector.get_detector_power()
                power_dBm = power_W_to_dBm(power_W)

                power_W_array[detector_index][voltage_index] = power_W
                power_dBm_array[detector_index][voltage_index] = power_dBm

                if detector_index == self.instrument_controller.get_target_detector_index():
                    power_W_plot_list.append(power_W)
                    power_dBm_plot_list.append(power_dBm)
                    voltage_array_plot.append(voltage)

            # Plot
            points.set_data(voltage_array_plot, power_dBm_plot_list)

            ax.set_ylim([min(power_dBm_plot_list) - 1, max(power_dBm_plot_list) + 1])

            self.gui_controller.update_menu()
            plt.pause(0.1)

        ################################################################
        # Save data
        beginning_time = datetime.datetime.now()
        filename = beginning_time.strftime("%Y-%m-%d_%H-%M-%S") + "_" + \
                   self.scan + "_" + \
                   self.chip + "_" + \
                   self.component + "_" + \
                   self.add_info + \
                   str(self.laser.get_name()) + "_" + \
                   str(self.laser.get_wavelength()) + "_" + \
                   str(self.instrument_controller.get_min_voltage()) + "_" + \
                   str(self.instrument_controller.get_max_voltage()) + "_" + \
                   str(self.instrument_controller.get_sweep_voltage())

        if self.gui_controller.save_bool:
            header = \
                "#\n# Date: %s\n#\n" % beginning_time.strftime("%Y-%m-%d_%H-%M-%S") + "_" \
                                                                                      "# Scan type: %s\n" % self.scan + \
                "# Chip: %s\n" % self.chip + \
                "# Component: %s\n" % self.component + \
                "# Additional info: %s\n#\n" % self.add_info + \
                "# Laser: %s\n" % self.laser.get_name()

            # Transmission alignment

            self.fig.savefig("Figures/" + filename + ".pdf", bbox_inches='tight')
            hf = h5py.File('Data/' + self.folder + '/' + filename + '.h5', 'w')
            hf.create_dataset('Header', data=header)
            hf.create_dataset('Voltage_V', data=voltage_array)
            for detector_index in range(0, len(self.detector_list)):
                print(self.detector_list[detector_index].get_name() + "_power_W")
                print(power_W_array)
                print(power_W_array[detector_index])
                hf.create_dataset(self.detector_list[detector_index].get_name() + "_power_W",
                                  data=power_W_array[detector_index])

            hf.close()

    def close(self):
        self.acquisition_flag = False
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None


class Sweep_Piezo_Plot_Window:
    def __init__(self, instrument_controller, gui_controller):
        self.instrument_controller = instrument_controller
        self.input_piezo_controller = self.instrument_controller.input_piezo_controller
        self.output_piezo_controller = self.instrument_controller.output_piezo_controller
        self.target_detector = None
        self.laser = None
        self.target_detector_index = 0
        self.detector_list = None
        self.gui_controller = gui_controller
        self.original_x_voltage = None
        self.original_y_voltage = None
        self.original_z_voltage = None
        self.y_voltage_interval = 40
        self.z_voltage_interval = 40

    def open(self):
        self.input_piezo_controller = self.instrument_controller.input_piezo_controller
        self.original_x_voltage = self.input_piezo_controller.get_x_voltage()
        self.original_y_voltage = self.input_piezo_controller.get_y_voltage()
        self.original_z_voltage = self.input_piezo_controller.get_z_voltage()
        self.target_detector = self.instrument_controller.get_target_detector()
        self.target_detector_index = self.instrument_controller.get_target_detector_index()
        self.detector_list = self.instrument_controller.get_detector_list()
        self.laser = self.instrument_controller.get_target_laser()
        z_voltage_array = np.arange(self.original_z_voltage - self.z_voltage_interval / 2,
                                    self.original_z_voltage + self.z_voltage_interval / 2,
                                    self.input_piezo_controller.get_z_resolution())
        y_voltage_array = np.arange(self.original_y_voltage - self.y_voltage_interval / 2,
                                    self.original_y_voltage + self.y_voltage_interval / 2,
                                    self.input_piezo_controller.get_y_resolution())

        rows, cols = (len(z_voltage_array), len(y_voltage_array))
        power_W_array, power_dBm_array = np.empty([rows, cols]), np.empty([rows, cols])

        for idx_z_voltage, z_voltage in enumerate(z_voltage_array):
            self.input_piezo_controller.set_z_voltage(z_voltage)
            if (idx_z_voltage % 2) == 0:
                y_loop_array = reversed(list(enumerate(y_voltage_array)))
            else:
                y_loop_array = enumerate(y_voltage_array)
            for idx_y_voltage, y_voltage in y_loop_array:
                print(y_voltage)
                self.input_piezo_controller.set_y_voltage(y_voltage)
                plt.pause(0.2)
                power_W = self.target_detector.get_detector_power()
                power_dBm = power_W_to_dBm(power_W)
                power_W_array[idx_z_voltage, idx_y_voltage] = power_W
                power_dBm_array[idx_z_voltage, idx_y_voltage] = power_dBm

        self.input_piezo_controller.set_z_voltage(self.original_z_voltage)
        self.input_piezo_controller.set_y_voltage(self.original_y_voltage)
        self.plot_data(z_voltage_array, y_voltage_array, power_dBm_array)

    def plot_data(self, z_voltage_array, y_voltage_array, power_dBm_array):
        # generate 2 2d grids for the x & y bounds
        Z_voltage_array, Y_voltage_array = np.meshgrid(y_voltage_array, z_voltage_array)

        fig, ax = plt.subplots()

        c = ax.pcolormesh(Z_voltage_array, Y_voltage_array, power_dBm_array, cmap='RdBu')
        ax.set_title('Coupling Scan')

        fig.colorbar(c, ax=ax)

        plt.show()

    def optimize_y_and_z(self):
        self.input_piezo_controller = self.instrument_controller.input_piezo_controller
        self.target_detector = self.instrument_controller.get_target_detector()

        initial_point = np.array([self.input_piezo_controller.get_y_voltage(), self.input_piezo_controller.get_z_voltage()])
        learning_rate = 5
        iterations = 20
        abs_tol = 0.05
        rel_tol = 1e-6

        current_point = initial_point.copy()
        best_point = current_point.copy()
        best_value = self.compute_function_value(current_point)

        for i in range(iterations):
            learning_rate = learning_rate / (i+1)**(0.5)

            print(i)
            # Estimate the gradient at the current point
            gradient = self.estimate_gradient(current_point, learning_rate)
            # Update the current point using gradient ascent
            new_point = current_point + learning_rate * gradient


            # Apply limits to the new point
            new_point[0] = np.clip(new_point[0], 0, 120)
            new_point[1] = np.clip(new_point[1], 0, 120)

            new_value = self.compute_function_value(new_point)

            self.input_piezo_controller.set_y_voltage(new_point[0])
            self.input_piezo_controller.set_z_voltage(new_point[1])

            # Update the best point if the new point has a lower function value
            if new_value > best_value:
                best_point = new_point
                best_value = new_value

            print("New value: ", new_value, "Best value: " , best_value)

            # Check for convergence based on absolute and relative tolerances
            change = np.linalg.norm(new_point - current_point)
            if change < abs_tol:
                break

            current_point = new_point

        self.input_piezo_controller.set_y_voltage(best_point[0])
        self.input_piezo_controller.set_z_voltage(best_point[1])

    # Example gradient estimation function
    def estimate_gradient(self, point, step_size):
        gradient_x = (self.compute_function_value(point + np.array([step_size, 0])) - self.compute_function_value(
            point)) / step_size
        gradient_y = (self.compute_function_value(point + np.array([0, step_size])) - self.compute_function_value(
            point)) / step_size
        return np.array([gradient_x, gradient_y])

    def compute_function_value(self, point):
        self.input_piezo_controller.set_y_voltage(point[0])
        self.input_piezo_controller.set_z_voltage(point[1])
        plt.pause(0.2)
        return power_W_to_dBm(self.target_detector.get_detector_power())

    def close(self):
        pass


class Tune_Piezo_Menu_Window:
    def __init__(self, instrument_controller, gui_controller):
        self.update_bool = None
        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.button_5 = None
        self.button_6 = None
        self.entry_1 = None
        self.gui_controller = gui_controller
        self.instrument_controller = instrument_controller
        self.detector_list = None
        self.window = None
        self.label = None
        self.info_label = None

    def open(self):
        if self.window is None:
            self.detector_list = self.instrument_controller.get_detector_list()
            self.update_bool = True
            self.window = tk.Tk()
            self.window.wm_title("Tune Piezo")
            window_width = 450  # width for the Tk root
            window_height = 350  # height for the Tk root
            ws = self.window.winfo_screenwidth()  # width of the screen
            hs = self.window.winfo_screenheight()  # height of the screen
            x = ws - window_width
            y = hs - window_height - 500
            self.window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

            msg = self.get_message()
            self.label = ttk.Label(self.window, text=msg, font="Arial")
            self.label.pack(side="top", fill="x", pady=10)

            self.button_6 = ttk.Button(self.window)
            self.button_6["text"] = "Optimize Y and Z"
            self.button_6["command"] = lambda: self.optimize_y_and_z_button()
            self.button_6.pack()

            self.button_5 = ttk.Button(self.window)
            self.button_5["text"] = "Run Piezo Scan"
            self.button_5["command"] = lambda: self.run_piezo_scan_button()
            self.button_5.pack()

            self.entry_1 = ttk.Entry(self.window)
            self.button_1 = ttk.Button(self.window)
            self.button_1["text"] = "Set X Voltage"
            self.button_1["command"] = lambda: self.set_x_voltage_button()
            self.button_1.pack()
            self.entry_1.pack()

            self.entry_2 = ttk.Entry(self.window)
            self.button_2 = ttk.Button(self.window)
            self.button_2["text"] = "Set Y Voltage"
            self.button_2["command"] = lambda: self.set_y_voltage_button()
            self.button_2.pack()
            self.entry_2.pack()

            self.entry_3 = ttk.Entry(self.window)
            self.button_3 = ttk.Button(self.window)
            self.button_3["text"] = "Set Z Voltage"
            self.button_3["command"] = lambda: self.set_z_voltage_button()
            self.button_3.pack()
            self.entry_3.pack()

            self.entry_4 = ttk.Entry(self.window)
            self.button_4 = ttk.Button(self.window)
            self.button_4["text"] = "Set X Resolution"
            self.button_4["command"] = lambda: self.set_x_resolution_button()
            self.button_4.pack()
            self.entry_4.pack()

            self.entry_5 = ttk.Entry(self.window)
            self.button_5 = ttk.Button(self.window)
            self.button_5["text"] = "Set Y Resolution"
            self.button_5["command"] = lambda: self.set_y_resolution_button()
            self.button_5.pack()
            self.entry_5.pack()

            self.entry_6 = ttk.Entry(self.window)
            self.button_6 = ttk.Button(self.window)
            self.button_6["text"] = "Set Z Resolution"
            self.button_6["command"] = lambda: self.set_z_resolution_button()
            self.button_6.pack()
            self.entry_6.pack()

    def update_button(self):
        self.update_window()

    def get_message(self):
        return self.get_controller_info() + "\n"

    def update_window(self):
        if self.update_bool:
            self.label.config(text=self.get_message())

    def close(self):
        self.update_bool = False
        if self.window is not None:
            self.window.destroy()
            self.window = None

    def get_controller_info(self):
        controller = self.instrument_controller.input_piezo_controller
        return "Voltage X: " + str(controller.get_x_voltage()) + ", " \
                                                                 "Y: " + str(controller.get_y_voltage()) + ", " \
                                                                                                           "Z: " + str(
            controller.get_z_voltage()) + ", ""\n" + \
            "Resolution X: " + str(controller.get_x_resolution()) + ", " \
                                                                    "Y: " + str(controller.get_y_resolution()) + ", " \
                                                                                                                 "Z: " + str(
                controller.get_z_resolution())

    def set_x_voltage_button(self):
        self.instrument_controller.input_piezo_controller.set_x_voltage(
            get_float_from_string(self.entry_1.get(), self.instrument_controller.input_piezo_controller.get_x_voltage()))
        self.update_window()

    def set_y_voltage_button(self):
        self.instrument_controller.input_piezo_controller.set_y_voltage(
            get_float_from_string(self.entry_2.get(), self.instrument_controller.input_piezo_controller.get_y_voltage()))
        self.update_window()

    def set_z_voltage_button(self):
        self.instrument_controller.input_piezo_controller.set_z_voltage(
            get_float_from_string(self.entry_3.get(), self.instrument_controller.input_piezo_controller.get_z_voltage()))
        self.update_window()

    def set_x_resolution_button(self):
        self.instrument_controller.input_piezo_controller.set_x_resolution(
            get_float_from_string(self.entry_4.get(), self.instrument_controller.input_piezo_controller.get_x_resolution()))
        self.update_window()

    def set_y_resolution_button(self):
        self.instrument_controller.input_piezo_controller.set_y_resolution(
            get_float_from_string(self.entry_5.get(), self.instrument_controller.input_piezo_controller.get_y_resolution()))
        self.update_window()

    def set_z_resolution_button(self):
        self.instrument_controller.input_piezo_controller.set_z_resolution(
            get_float_from_string(self.entry_6.get(), self.instrument_controller.input_piezo_controller.get_z_resolution()))
        self.update_window()

    def run_piezo_scan_button(self):
        self.gui_controller.open_sweep_piezo_window()

    def optimize_y_and_z_button(self):
        self.gui_controller.optimize_y_and_z()


class GUI_Controller:

    def __init__(self):
        beginning_time = datetime.datetime.now()

        self.is_acquisition_on = False
        self.is_instruments_on = False
        self.current_routine = None
        self.save_bool = True
        self.sweep_mode = "Loss"  # "Loss", "Polarization", "SFG", "DFG", "SHG"

        self.instrument_controller = Instrument_Controller()
        self.menu_window = Menu_Window(self)
        self.tune_laser_window = Tune_Laser_Window(self.instrument_controller, self)
        self.menu_window.open()
        self.detector_window = Tune_Detector_Window(self.instrument_controller)
        self.acquisition_window = Acquisition_Window(self.instrument_controller, self)
        self.sweep_wavelength_menu_window = Sweep_Wavelength_Menu_Window(self.instrument_controller, self)
        self.sweep_voltage_menu_window = Sweep_Voltage_Menu_Window(self.instrument_controller, self)
        self.sweep_voltage_plot_window = Sweep_Voltage_Plot_Window(self.instrument_controller, self)
        self.tune_piezo_menu_window = Tune_Piezo_Menu_Window(self.instrument_controller, self)
        self.sweep_piezo_plot_window = Sweep_Piezo_Plot_Window(self.instrument_controller, self)
        self.close_bool = False
        tk.mainloop()

        ending_time = datetime.datetime.now()
        elapsed = ending_time - beginning_time
        elapsed_min = int(elapsed.seconds / 60)
        elapsed_sec = elapsed.seconds - elapsed_min * 60
        print("Elapsed time = {0:2d} minutes {1:2d} seconds".format(elapsed_min, elapsed_sec))

    def toggle_save_bool(self):
        self.save_bool = not self.save_bool
        print(self.save_bool)

    def get_save_bool(self):
        return self.save_bool

    def get_sweep_mode(self):
        return self.sweep_mode

    def next_sweep_mode(self):
        pass

    def close_instruments(self):
        if self.is_instruments_on:
            self.is_instruments_on = False
            self.tune_laser_window.close()
            self.detector_window.close()
            self.instrument_controller.close_instruments()

    def toggle_instruments(self):
        if self.is_instruments_on:
            self.close_instruments()
        else:
            self.open_instruments()

    def open_instruments(self):
        if not self.is_instruments_on:
            self.is_instruments_on = True
            self.instrument_controller.open_instruments()
            self.tune_laser_window.open()
            self.detector_window.open()

    def close_program(self):
        self.close_bool = True
        self.close_windows()
        if self.is_instruments_on:
            self.close_instruments()

    def close_windows(self):
        self.end_acquisition()
        self.acquisition_window.close()
        self.sweep_wavelength_plot_window.close()
        self.sweep_wavelength_menu_window.close()
        self.sweep_voltage_plot_window.close()
        self.sweep_voltage_menu_window.close()
        self.tune_piezo_menu_window.close()
        self.detector_window.close()
        self.menu_window.close()

    def start_acquisition(self):
        self.is_acquisition_on = True
        self.open_instruments()
        self.tune_laser_window.open()
        self.detector_window.open()
        self.acquisition_window.open()
        self.update_menu()

    def end_acquisition(self):
        self.is_acquisition_on = False
        self.detector_window.close()
        self.tune_laser_window.close()
        self.acquisition_window.close()

    def open_sweep_voltage_menu(self):
        self.open_instruments()
        self.menu_window.update_window()
        self.detector_window.open()
        self.tune_laser_window.open()
        self.sweep_voltage_menu_window.open()

    def open_sweep_wavelength_menu(self):
        self.open_instruments()
        self.menu_window.update_window()
        self.detector_window.open()
        self.tune_laser_window.open()
        self.sweep_wavelength_menu_window.open()

    def open_tune_piezo_menu(self):
        self.open_instruments()
        self.menu_window.update_window()
        self.detector_window.open()
        self.tune_laser_window.open()
        self.tune_piezo_menu_window.open()

    def open_sweep_piezo_window(self):
        self.sweep_piezo_plot_window.open()

    def run_sweep_voltage(self):
        self.open_instruments()
        self.menu_window.update_window()
        self.sweep_voltage_plot_window.open()

    def run_sweep_wavelength(self):
        self.open_instruments()
        self.menu_window.update_window()
        self.sweep_wavelength_plot_window.open()

    def get_is_instruments_on(self):
        return self.is_instruments_on

    def get_is_acquisition_on(self):
        return self.is_acquisition_on

    def update_menu(self):
        if not self.close_bool:
            self.menu_window.update_window()
            self.tune_laser_window.update_window()
            self.menu_window.update_window()
            self.detector_window.update_window()
            self.sweep_wavelength_menu_window.update_window()
            self.sweep_voltage_menu_window.update_window()

    def optimize_y_and_z(self):
        self.sweep_piezo_plot_window.optimize_y_and_z()


class Instrument_Controller:
    def __init__(self):
        self.input_piezo_controller_connect_bool = None
        self.output_piezo_controller_connect_bool = None
        self.settings_path = "Settings/instrument_controller_settings.txt"
        self.resource_manager = visa.ResourceManager()
        self.detector_list = []
        self.laser_list = []
        self.waveform_generator_list = []
        self.optical_spectrum_analyzer_list = []
        self.wavelength_min = None
        self.wavelength_max = None

        self.initial_wavelength_nm = None
        self.target_laser_index = None
        self.target_detector_index = None
        self.wavelength_step = None

        self.voltage_step = None
        self.voltage_min = None
        self.voltage_max = None

        self.siglent_connect_bool = None
        self.arroyo_connect_bool = None
        self.toptica_connect_bool = None
        self.agilent_connect_bool = None
        self.yokogawa_connect_bool = None
        self.exfo_connect_bool = None
        self.input_piezo_controller = None
        self.output_piezo_controller = None

        self.instrument_connected_bool = False

        self.load_settings()

    def load_settings(self):
        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.initial_wavelength_nm = settings_dict["initial_wavelength_nm"]
            self.target_laser_index = settings_dict["target_laser_index"]
            self.target_detector_index = settings_dict["target_detector_index"]
            self.wavelength_step = settings_dict["wavelength_step"]  # nm

            self.voltage_step = settings_dict["voltage_step"]  # V
            self.voltage_min = settings_dict["min_voltage"]  # V
            self.voltage_max = settings_dict["max_voltage"]  # V

            self.input_piezo_controller_connect_bool = settings_dict["input_piezo_controller_connect_bool"]
            self.output_piezo_controller_connect_bool = settings_dict["output_piezo_controller_connect_bool"]
            self.siglent_connect_bool = settings_dict["siglent_connect_bool"]
            self.arroyo_connect_bool = settings_dict["arroyo_connect_bool"]
            self.toptica_connect_bool = settings_dict["toptica_connect_bool"]
            self.agilent_connect_bool = settings_dict["agilent_connect_bool"]
            self.yokogawa_connect_bool = settings_dict["yokogawa_connect_bool"]
            self.exfo_connect_bool = settings_dict["exfo_connect_bool"]

    def get_max_voltage(self):
        return self.voltage_max

    def get_min_voltage(self):
        return self.voltage_min

    def get_sweep_voltage(self):
        return self.voltage_step

    def set_min_voltage(self, voltage):
        if 0 <= voltage <= 5 and voltage < self.get_max_voltage():
            self.voltage_min = voltage
        else:
            print("Voltage " + str(voltage) + " is not a valid minimum voltage")

    def set_max_voltage(self, voltage):
        if 0 <= voltage <= 5 and self.get_min_voltage() < voltage:
            self.voltage_max = voltage
        else:
            print("Voltage " + str(voltage) + " is not a valid maximum voltage")

    def set_sweep_voltage(self, voltage):
        self.voltage_step = voltage

    def get_min_wavelength(self):
        if self.wavelength_min is None:
            return self.get_target_laser().get_min_wavelength()
        else:
            return self.wavelength_min

    def get_max_wavelength(self):
        if self.wavelength_max is None:
            return self.get_target_laser().get_max_wavelength()
        else:
            return self.wavelength_max

    def get_sweep_wavelength(self):
        return self.wavelength_step

    def set_min_wavelength(self, wavelength):
        if self.get_target_laser().get_min_wavelength() <= wavelength <= self.get_target_laser().get_max_wavelength() and wavelength < self.get_max_wavelength():
            self.wavelength_min = wavelength
        else:
            print("Wavelength " + str(wavelength) + " is not a valid minimum wavelength for the " + str(
                self.get_target_laser().get_name()))

    def set_max_wavelength(self, wavelength):
        if self.get_target_laser().get_min_wavelength() <= wavelength <= self.get_target_laser().get_max_wavelength() and self.get_min_wavelength() < wavelength:
            self.wavelength_max = wavelength
        else:
            print("Wavelength " + str(wavelength) + " is not a valid maximum wavelength for the " + str(
                self.get_target_laser().get_name()))

    def set_sweep_wavelength(self, wavelength):
        self.wavelength_step = wavelength

    def open_instruments(self):
        if not self.instrument_connected_bool:

            self.connect_instruments_visa()

            if self.toptica_connect_bool:
                settings_path = "Settings/toptica_settings.txt"
                try:
                    toptica_laser = Toptica_CTL950(settings_path)
                    self.laser_list.append(toptica_laser)
                except:
                    print("Could not connect to Toptica Laser")

            if self.input_piezo_controller_connect_bool:
                self.input_piezo_controller = Piezo_Controller_Thorlabs(serial_number=['1908086985-08', 'MDT693B'])
            if self.output_piezo_controller_connect_bool:
                self.output_piezo_controller = Piezo_Controller_Thorlabs(serial_number=['2207070466-03', 'MDT693B'])
            self.instrument_connected_bool = True

            plt.pause(2)

    def connect_instruments_visa(self):
        resource_list = self.resource_manager.list_resources()
        print("List of resources: " + str(resource_list))
        for resource in resource_list:

            if resource == "USB0::0x1313::0x8076::M00905457::INSTR":
                settings_path = "Settings/thorlabs_57_settings.txt"
                detector = Thorlabs_PM100U(self.resource_manager, resource, settings_path)
                self.detector_list.append(detector)

            if resource == "USB0::0x1313::0x8076::M00905456::INSTR":
                settings_path = "Settings/thorlabs_56_settings.txt"
                detector = Thorlabs_PM100U(self.resource_manager, resource, settings_path)
                self.detector_list.append(detector)

            if resource == "USB0::0x1313::0x8076::M00905455::INSTR":
                settings_path = "Settings/thorlabs_55_settings.txt"
                detector = Thorlabs_PM100U(self.resource_manager, resource, settings_path)
                self.detector_list.append(detector)

            if resource == "ASRL3::INSTR" and self.arroyo_connect_bool:
                try:
                    settings_path = "Settings/arroyo_settings.txt"
                    arroyo_laser = Arroyo(self.resource_manager, settings_path, resource)
                    self.laser_list.append(arroyo_laser)
                except visa.errors.VisaIOError:
                    print("Could not connect to Arroyo Laser. Did you turn it on?")

            if resource == "GPIB0::7::INSTR" and self.yokogawa_connect_bool:
                yokogawa = Yokogawa(self.resource_manager, resource)
                yokogawa.set_sensitivity('MID')
                yokogawa.set_wavelength_center(self.initial_wavelength_nm)
                yokogawa.set_span_wav(15)  # [nm]
                yokogawa.set_RBW(0.05)
                self.optical_spectrum_analyzer_list.append(yokogawa)

            if resource == "GPIB1::10::INSTR" and self.exfo_connect_bool:
                settings_path = "Settings/exfo_settings.txt"
                exfo_laser = EXFO(self.resource_manager, settings_path, resource)
                exfo_laser.laser_on()
                self.laser_list.append(exfo_laser)
                self.detector_list.append(exfo_laser)

            if resource == "GPIB0::18::INSTR" and self.agilent_connect_bool:
                agilent = Agilent(self.resource_manager, GPIB_interface=18)
                self.laser_list.append(agilent)

            if resource == "USB0::0xF4EC::0x1101::SDG6XBAQ3R0181::INSTR" and self.siglent_connect_bool:
                settings_path = "Settings/siglent_settings.txt"
                siglent = Siglent(self.resource_manager, settings_path, resource)
                self.waveform_generator_list.append(siglent)

    def get_laser_list(self):
        return self.laser_list

    def get_detector_list(self):
        return self.detector_list

    def get_waveform_generator_list(self):
        return self.waveform_generator_list

    def set_target_laser_index(self, index):
        self.target_laser_index = np.mod(index, len(self.laser_list))
        self.wavelength_min = None
        self.wavelength_max = None

    def set_target_detector_index(self, index):
        self.target_detector_index = np.mod(index, len(self.detector_list))

    def next_laser(self):
        self.set_target_laser_index(self.target_laser_index + 1)

    def previous_laser(self):
        self.set_target_laser_index(self.target_laser_index - 1)

    def next_detector(self):
        print("next_detector")
        print(self.target_detector_index)
        self.set_target_detector_index(self.target_detector_index + 1)
        print(self.target_detector_index)

    def previous_detector(self):
        self.set_target_detector_index(self.target_detector_index - 1)

    def update_detector_wavelength(self, wavelength):
        for detector in self.detector_list:
            detector.set_detector_wavelength(wavelength)

    def get_target_laser(self):
        return self.laser_list[self.get_laser_detector_index()]

    def get_target_detector(self):
        return self.detector_list[self.get_target_detector_index()]

    def get_target_detector_index(self):
        return np.mod(self.target_detector_index, len(self.detector_list))

    def get_laser_detector_index(self):
        return np.mod(self.target_laser_index, len(self.laser_list))

    def save_settings(self):
        dictionary = {"initial_wavelength_nm": float(self.initial_wavelength_nm),
                      "target_laser_index": int(self.target_laser_index),
                      "target_detector_index": int(self.target_detector_index),
                      "wavelength_step": float(self.wavelength_step),
                      "voltage_step": float(self.voltage_step),
                      "min_voltage": float(self.voltage_min),
                      "max_voltage": float(self.voltage_max),
                      "siglent_connect_bool": self.siglent_connect_bool,
                      "toptica_connect_bool": self.toptica_connect_bool,
                      "agilent_connect_bool": self.agilent_connect_bool,
                      "yokogawa_connect_bool": self.yokogawa_connect_bool,
                      "exfo_connect_bool": self.exfo_connect_bool,
                      "arroyo_connect_bool": self.arroyo_connect_bool,
                      "piezo_controller_connect_bool": self.piezo_controller_connect_bool,
                      "piezo_controller_connect_bool": self.piezo_controller_connect_bool}

        with open(self.settings_path, "w") as text_file:
            json.dump(dictionary, text_file)

    def close_instruments(self):
        self.save_settings()
        for laser in self.laser_list:
            laser.close()
        self.laser_list = []
        for detector in self.detector_list:
            detector.close()
        self.detector_list = []
        for osa in self.optical_spectrum_analyzer_list:
            osa.close()
        self.optical_spectrum_analyzer_list = []
        # for waveform_generator in self.waveform_generator_list:
        # waveform_generator.close()
        self.waveform_generator_list = []
        self.piezo_controller.close()
        self.instrument_connected_bool = False
        plt.pause(2)


class Menu_Window:
    def __init__(self, GUI_controller):
        self.y = None
        self.x = None
        self.screen_height = None
        self.screen_width = None
        self.gui_controller = GUI_controller
        self.observer_list = None
        self.window = None
        self.label = None
        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.button_5 = None
        self.button_6 = None
        self.button_7 = None
        self.width = 450
        self.height = 180

        self.close_bool = None

    def open(self):
        self.close_bool = False
        self.window = tk.Tk()
        self.window.wm_title("Main Menu")
        msg = self.get_message()
        self.label = ttk.Label(self.window, text=msg, font="Arial")
        self.label.pack(side="top", fill="x", pady=10)

        self.button_4 = ttk.Button(self.window)
        self.button_4["text"] = self.get_start_acquisition_label()
        self.button_4["command"] = lambda: self.toggle_acquisition()
        self.button_4.pack()

        self.button_5 = ttk.Button(self.window)
        self.button_5["text"] = "Open Sweep Wavelength Menu"
        self.button_5["command"] = lambda: self.run_sweep_wavelength()
        self.button_5.pack()

        self.button_6 = ttk.Button(self.window)
        self.button_6["text"] = "Open Sweep Voltage Menu"
        self.button_6["command"] = lambda: self.run_sweep_voltage()
        self.button_6.pack()

        self.button_7 = ttk.Button(self.window)
        self.button_7["text"] = "Piezo Sweep Menu"
        self.button_7["command"] = lambda: self.run_piezo_sweep()
        self.button_7.pack()

        self.button_1 = ttk.Button(self.window)
        self.button_1["text"] = self.get_toggle_instruments_label()
        self.button_1["command"] = lambda: self.toggle_instruments()
        self.button_1.pack()

        self.button_2 = ttk.Button(self.window)
        self.button_2["text"] = "Close Program"
        self.button_2["command"] = lambda: self.close_program()
        self.button_2.pack()

        self.set_geometry()

    def run_sweep_voltage(self):
        self.gui_controller.open_sweep_voltage_menu()

    def run_sweep_wavelength(self):
        self.gui_controller.open_sweep_wavelength_menu()

    def run_piezo_sweep(self):
        self.gui_controller.open_tune_piezo_menu()

    def toggle_acquisition(self):
        if self.gui_controller.get_is_acquisition_on():
            self.gui_controller.end_acquisition()
        else:
            self.gui_controller.start_acquisition()
        self.gui_controller.update_menu()

    def get_start_acquisition_label(self):
        is_acquisition_on = self.gui_controller.get_is_acquisition_on()
        if is_acquisition_on:
            return "End Acquisition"
        else:
            return "Start Acquisition"

    def get_toggle_instruments_label(self):
        is_instruments_on = self.gui_controller.get_is_instruments_on()
        if is_instruments_on:
            return "Close Instruments"
        else:
            return "Connect to Instruments"

    def set_geometry(self):
        self.screen_width = self.window.winfo_screenwidth()  # width of the screen
        self.screen_height = self.window.winfo_screenheight()  # height of the screen
        self.x = self.screen_width - self.width
        self.y = 0
        self.window.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))

    def toggle_instruments(self):
        self.gui_controller.toggle_instruments()
        self.update_window()

    def close_program(self):
        self.gui_controller.close_program()

    def get_message(self):
        return "Program running... "

    def update_window(self):
        if not self.close_bool:
            self.label.config(text=self.get_message())
            self.button_1.configure(text=self.get_toggle_instruments_label())
            self.button_4.configure(text=self.get_start_acquisition_label())

    def close(self):
        self.close_bool = True
        if self.window is not None:
            self.window.destroy()
            self.window = None


class Tune_Laser_Window:
    def __init__(self, instrument_controller, gui_controller):
        self.gui_controller = gui_controller
        self.instrument_controller = instrument_controller
        self.tune_step_wavelength = 1.0
        self.tune_step_power = 1.0
        self.window = None

        self.laser_list = None
        self.detector_list = None

        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.button_5 = None
        self.button_6 = None
        self.button_7 = None
        self.button_8 = None
        self.button_9 = None
        self.button_10 = None
        self.entry_1 = None
        self.entry_2 = None
        self.entry_3 = None
        self.entry_4 = None

        self.label = None
        self.info_label = None
        self.close_bool = None

    def open(self):
        if self.window is None:
            self.close_bool = False
            self.laser_list = self.instrument_controller.get_laser_list()
            self.detector_list = self.instrument_controller.get_detector_list()

            self.window = tk.Tk()
            self.window.wm_title("Tune Laser")
            window_width = 450  # width for the Tk root
            window_height = 450  # height for the Tk root
            ws = self.window.winfo_screenwidth()  # width of the screen
            hs = self.window.winfo_screenheight()  # height of the screen
            x = ws - window_width * 1
            y = hs - window_height - 30
            self.window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

            msg = self.get_message()
            self.label = ttk.Label(self.window, text=msg, font="Arial")
            self.label.pack(side="top", fill="x", pady=10)

            info_string = self.get_info()
            self.info_label = ttk.Label(self.window, text=info_string, font="Arial")
            self.info_label.pack(side="top", fill="x", pady=10)
            self.info_label.pack(side="bottom", fill="x", pady=10)

            self.button_1 = ttk.Button(self.window)
            self.button_1["text"] = "+" + str(self.tune_step_wavelength) + " nm"
            self.button_1["command"] = lambda: self.button1()
            self.button_1.pack(side='right', fill='y')

            self.button_2 = ttk.Button(self.window)
            self.button_2["text"] = "-" + str(self.tune_step_wavelength) + " nm"
            self.button_2["command"] = lambda: self.button2()
            self.button_2.pack(side='left', fill='y')

            self.button_5 = ttk.Button(self.window)
            self.button_5["text"] = "+" + str(self.tune_step_power) + " mW"
            self.button_5["command"] = lambda: self.button5()
            self.button_5.pack(side='right', fill='y')

            self.button_6 = ttk.Button(self.window)
            self.button_6["text"] = "-" + str(self.tune_step_power) + " mW"
            self.button_6["command"] = lambda: self.button6()
            self.button_6.pack(side='left', fill='y')

            self.entry_1 = ttk.Entry(self.window)
            self.button_3 = ttk.Button(self.window)
            self.button_3["text"] = "Go to [nm]"
            self.button_3["command"] = lambda: self.button3()
            self.button_3.pack(fill='y')
            self.entry_1.pack()

            self.entry_2 = ttk.Entry(self.window)
            self.button_4 = ttk.Button(self.window)
            self.button_4["text"] = "Set step [nm]"
            self.button_4["command"] = lambda: self.button4()
            self.button_4.pack(fill='y')
            self.entry_2.pack()

            self.entry_3 = ttk.Entry(self.window)
            self.button_7 = ttk.Button(self.window)
            self.button_7["text"] = "Go to [mW]"
            self.button_7["command"] = lambda: self.button7()
            self.button_7.pack(fill='y')
            self.entry_3.pack()

            self.entry_4 = ttk.Entry(self.window)
            self.button_8 = ttk.Button(self.window)
            self.button_8["text"] = "Set step [mW]"
            self.button_8["command"] = lambda: self.button8()
            self.button_8.pack(fill='y')
            self.entry_4.pack()

            self.button_9 = ttk.Button(self.window)
            self.button_9["text"] = "Next laser"
            self.button_9["command"] = lambda: self.next_laser()
            self.button_9.pack(fill='y')

            self.button_9 = ttk.Button(self.window)
            self.button_9["text"] = "On/Off"
            self.button_9["command"] = lambda: self.on_off_button()
            self.button_9.pack(fill='y')

    def on_off_button(self):
        self.instrument_controller.get_target_laser().toggle_laser()
        self.update_window()

    def get_info(self):
        info_string = "Laser Information:\n\n"
        for laser in self.laser_list:
            info_string += self.get_info_string(laser) + "\n"
        return info_string

    def get_info_string(self, laser):
        info_string = ""
        info_string += laser.get_name() + ": %0.2f nm" % (
            laser.get_wavelength()) + ", %0.2f mW" % (
                           laser.get_power()) + "\n"
        if laser.get_name() == "Arroyo laser":
            info_string += ", %0.2f mA" % (laser.get_current()) + ", %0.2f C" % (
                laser.get_temperature()) + ", %0.2f V" % (laser.get_voltage())
        return info_string

    def get_message(self):
        laser = self.instrument_controller.get_target_laser()
        return self.get_info_string(laser)

    def set_wavelength(self, wavelength):
        laser = self.instrument_controller.get_target_laser()
        laser.set_wavelength(wavelength)
        for detector in self.detector_list:
            detector.set_detector_wavelength(wavelength)

    def button1(self):
        laser = self.instrument_controller.get_target_laser()
        current_wavelength = laser.get_wavelength()
        update_wavelength = current_wavelength + self.tune_step_wavelength
        self.set_wavelength(update_wavelength)
        self.gui_controller.update_menu()

    def button2(self):
        laser = self.instrument_controller.get_target_laser()
        current_wavelength = laser.get_wavelength()
        update_wavelength = current_wavelength - self.tune_step_wavelength
        self.set_wavelength(update_wavelength)
        self.gui_controller.update_menu()

    def button3(self):
        laser = self.instrument_controller.get_target_laser()
        self.set_wavelength(get_float_from_string(self.entry_1.get(), laser.get_wavelength()))
        self.gui_controller.update_menu()

    def button5(self):
        laser = self.instrument_controller.get_target_laser()
        current_power = laser.get_power()
        update_power = current_power + self.tune_step_power
        laser.set_power(update_power)
        self.gui_controller.update_menu()

    def button6(self):
        laser = self.instrument_controller.get_target_laser()
        current_power = laser.get_power()
        update_power = current_power - self.tune_step_power
        laser.set_power(update_power)
        self.gui_controller.update_menu()

    def button7(self):
        laser = self.instrument_controller.get_target_laser()
        laser.set_power(get_float_from_string(self.entry_3.get(), laser.get_power()))
        self.gui_controller.update_menu()

    def set_step_power(self, step):
        self.tune_step_power = float(step)

    def set_step_wavelength(self, step):
        self.tune_step_wavelength = float(step)

    def button4(self):
        self.set_step_wavelength(get_float_from_string(self.entry_2.get(), self.tune_step_wavelength))
        self.gui_controller.update_menu()

    def button8(self):
        self.set_step_power(get_float_from_string(self.entry_4.get(), self.tune_step_power))
        self.gui_controller.update_menu()

    def update_window(self):
        if not self.close_bool:
            self.button_1.configure(text="+" + str(self.tune_step_wavelength) + " nm")
            self.button_2.configure(text="-" + str(self.tune_step_wavelength) + " nm")
            self.button_5.configure(text="+" + str(self.tune_step_power) + " mW")
            self.button_6.configure(text="-" + str(self.tune_step_power) + " mW")
            msg = self.get_message()
            info_string = self.get_info()
            self.label.config(text=msg)
            self.info_label.config(text=info_string)

    def next_laser(self):
        self.instrument_controller.next_laser()
        self.gui_controller.update_menu()

    def close(self):
        self.close_bool = True
        if self.window is not None:
            self.window.destroy()
            self.window = None


class Acquisition_Window:
    def __init__(self, instrument_controller, gui_controller):
        self.gui_controller = gui_controller
        self.instrument_controller = instrument_controller
        self.ws = 2000
        self.hs = 1500
        self.acquisition_flag = None
        self.fig = None

    def open(self):
        self.acquisition_flag = True
        detector = self.instrument_controller.get_target_detector()
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

        power_list, power_dBm_list, power_dBm_max_list, time_list = [], [], [], []
        T0 = datetime.datetime.now()
        T = T0 - T0

        power = detector.get_detector_power()
        power_list.append(power)

        power_dBm = power_W_to_dBm(power)
        power_dBm_list.append(power_dBm)

        power_dBm_max = power_dBm
        power_dBm_max_list.append(power_dBm_max)

        time_list.append(T.seconds + T.microseconds / 1e6)

        y_c = int(power_dBm) + (power_dBm % 1 > 0)

        # Plot
        self.fig, ax = plt.subplots(ncols=1, nrows=1)
        ax.set(xlabel='Time (s)', ylabel='Power (dBm)')
        points_plot, = ax.plot(time_list, power_dBm_list, marker='o', linestyle='-', color='red', lw=LW, ms=MS, mec='k',
                               mew=MEW)
        power_max_plot, = ax.plot(time_list, power_dBm_max_list, marker='', linestyle='-', color='blue', lw=LW, ms=MS,
                                  mec='k', mew=MEW)

        ax.grid()
        DPI = self.fig.get_dpi()

        self.fig.set_size_inches((self.ws - 80) / DPI, (self.hs - 200) / DPI, forward=True)
        self.fig.canvas.manager.window.wm_geometry('+80+0')

        while self.acquisition_flag:
            pause_value = 0.01
            T = datetime.datetime.now() - T0
            T_up = T.seconds + T.microseconds / 1e6

            # Update Plot
            time_list.append(T_up)
            detector = self.instrument_controller.get_target_detector()
            power_dBm = power_W_to_dBm(detector.get_detector_power())
            power_dBm_list.append(power_dBm)
            points_plot.set_data(time_list, power_dBm_list)

            x_left_limit_index = 0
            power_dBm_max = max(power_dBm_list[x_left_limit_index: -1])
            power_dBm_max_list.append(power_dBm_max)
            power_max_plot.set_data(time_list, power_dBm_max_list)

            ax.set_xlim([T_up - xrange, T_up])
            if power_dBm > (y_c + (yrange - 0.1)):
                y_c = int(power_dBm)
            if power_dBm < (y_c - (yrange - 0.1)):
                y_c = int(power_dBm + 1)

            ax.set_ylim([y_c - yrange, y_c + yrange])

            self.gui_controller.update_menu()
            plt.pause(pause_value)

    def close(self):
        self.acquisition_flag = False
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None


class Tune_Detector_Window:
    def __init__(self, instrument_controller):
        self.update_bool = None
        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.entry_1 = None
        self.instrument_controller = instrument_controller
        self.detector_list = None
        self.window = None
        self.label = None
        self.info_label = None

    def open(self):
        if self.window is None:
            self.detector_list = self.instrument_controller.get_detector_list()
            self.update_bool = True
            self.window = tk.Tk()
            self.window.wm_title("Tune Detector")
            window_width = 450  # width for the Tk root
            window_height = 300  # height for the Tk root
            ws = self.window.winfo_screenwidth()  # width of the screen
            hs = self.window.winfo_screenheight()  # height of the screen
            x = ws - window_width
            y = hs - window_height - 500
            self.window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

            msg = self.get_message()
            self.label = ttk.Label(self.window, text=msg, font="Arial")
            self.label.pack(side="top", fill="x", pady=10)

            # self.button_2 = ttk.Button(self.window)
            # self.button_2["text"] = "Previous Detector"
            # self.button_2["command"] = lambda: self.previous_detector_button()
            # self.button_2.pack()

            # self.button_3 = ttk.Button(self.window)
            # self.button_3["text"] = "Update Label"
            # self.button_3["command"] = lambda: self.update_button()
            # self.button_3.pack()

            self.entry_1 = ttk.Entry(self.window)
            self.button_4 = ttk.Button(self.window)
            self.button_4["text"] = "Set Wavelength"
            self.button_4["command"] = lambda: self.set_wavelength_button()
            self.button_4.pack()
            self.entry_1.pack()

            self.entry_2 = ttk.Entry(self.window)
            self.button_5 = ttk.Button(self.window)
            self.button_5["text"] = "Set Averaging"
            self.button_5["command"] = lambda: self.set_averaging_button()
            self.button_5.pack()
            self.entry_2.pack()

            self.button_1 = ttk.Button(self.window)
            self.button_1["text"] = "Next Detector"
            self.button_1["command"] = lambda: self.next_detector_button()
            self.button_1.pack()

            info = self.get_info()
            self.info_label = ttk.Label(self.window, text=info, font="Arial")
            self.info_label.pack(side="top", fill="x", pady=10)

    def update_button(self):
        self.update_window()

    def next_detector_button(self):
        print("next")
        self.instrument_controller.next_detector()
        self.update_window()

    def set_wavelength_button(self):
        self.instrument_controller.get_target_detector().set_detector_wavelength(
            get_float_from_string(self.entry_1.get(),
                                  self.instrument_controller.get_target_detector().get_detector_wavelength()))
        self.update_window()

    def set_averaging_button(self):
        self.instrument_controller.get_target_detector().set_averaging(get_float_from_string(self.entry_2.get(),
                                                                                             self.instrument_controller.get_target_detector().get_averaging()))
        self.update_window()

    def previous_detector_button(self):
        self.instrument_controller.previous_detector()
        self.update_window()

    def get_message(self):
        detector = self.instrument_controller.get_target_detector()
        return self.get_detector_info(detector) + "\n"

    def get_info(self):
        info_string = "Detector Information:\n\n"
        for detector in self.detector_list:
            info_string += self.get_detector_info(detector) + "\n"
        return info_string

    def get_detector_info(self, detector):
        power_W = detector.get_detector_power()
        info_string = detector.get_name() + ": " + str(np.round(power_W * 1000, 6)) + " mW, " + str(
            np.round(power_W_to_dBm(power_W), 1)) + " dBm, " + str(detector.get_detector_wavelength()) + " nm, " + str(
            detector.get_averaging())
        return info_string

    def update_window(self):
        if self.update_bool:
            self.label.config(text=self.get_message())
            self.info_label.config(text=self.get_info())

    def close(self):
        self.update_bool = False
        if self.window is not None:
            self.window.destroy()
            self.window = None


