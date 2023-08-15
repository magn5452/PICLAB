import json
from tkinter import *

from matplotlib import pyplot as plt
# these two imports are important
import threading

from GUI.Acquisition_Window import Acquisition_Window
from GUI.Instrument_Controller import Instrument_Controller
from GUI.Optimize_Piezo import Optimize_Piezo, Optimizer_Gradient_Descent
from GUI.Sweep_Voltage_Window import Sweep_Voltage_Menu_Window
from GUI.Sweep_Wavelength_Window import Sweep_Wavelength_Menu_Window
from GUI.Sweep_Wavelength_Plot import Sweep_Wavelength_Plot_Window
from GUI.Tune_Detector_Window import Tune_Detector_Window
from GUI.Tune_Laser_Window import Tune_Laser_Window
from GUI.Tune_Piezo_Window import Tune_Piezo_Window
from GUI.Sweep_Voltage_Plot import Sweep_Voltage_Plot_Window


class GUI_Controller:

    def __init__(self):

        self.is_voltage_sweep_on = None
        self.is_wavelength_sweep_on = None
        self.voltage_sweep_save_path = None
        self.wavelength_sweep_save_path = None
        self.settings_path = "Settings/gui_controller_settings.txt"
        self.sweep_wavelength_mode = "Loss"
        self.save_bool = True
        self.piezo_optimization_thread = None
        self.main_loop_bool = True
        self.sweep_wavelength_thread = None
        self.acquisition_thread = None

        self.is_optimize_piezo_on = False
        self.is_instruments_on = False
        self.is_acquisition_on = False

        self.sweep_pause_time = 1

        self.load_settings()

        self.instrument_controller = Instrument_Controller()

        self.acquisition_window = Acquisition_Window(self.instrument_controller, self)
        self.tune_laser_window = Tune_Laser_Window(self.instrument_controller)
        self.tune_detector_window = Tune_Detector_Window(self.instrument_controller)
        self.tune_piezo_window = Tune_Piezo_Window(self.instrument_controller, self)
        self.sweep_wavelength_menu_window = Sweep_Wavelength_Menu_Window(self.instrument_controller, self)
        self.sweep_wavelength_plot_window = Sweep_Wavelength_Plot_Window(self.instrument_controller, self)
        self.sweep_voltage_menu_window = Sweep_Voltage_Menu_Window(self.instrument_controller, self)
        self.sweep_voltage_plot_window = Sweep_Voltage_Plot_Window(self.instrument_controller, self)
        settings = 'C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/optimize_piezo_settings'
        self.optimizer = Optimizer_Gradient_Descent(settings)
        self.optimize_piezo = Optimize_Piezo(self.instrument_controller, self.optimizer, settings)

        # initialise a window.
        self.main_window = Tk()
        self.main_window.wm_title("PIC LAB")
        self.main_window.config(background='white')
        self.main_window.geometry("1000x700")
        # self.main_window.attributes("-fullscreen", True)
        self.main_window.protocol("WM_DELETE_WINDOW", self.close_application)

        self.menubar = Menu(self.main_window)

        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.do_nothing)
        self.file_menu.add_command(label="Save Figure", command=self.do_nothing)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.close_application)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.instrument_menu = Menu(self.menubar, tearoff=0)
        self.instrument_menu.add_command(label="Connect/Disconnect", command=self.toggle_instruments)
        self.instrument_menu.add_command(label="Toggle Acquisition", command=self.toggle_acquisition)
        self.instrument_menu.add_command(label="Piezo Optimization", command=self.optimize_y_and_z)
        self.instrument_menu.add_command(label="Phase Matching Follow", command=self.phase_matching_follow)
        self.instrument_menu.add_command(label="Sweep Power", command=self.sweep_power)
        self.menubar.add_cascade(label="Instruments", menu=self.instrument_menu)

        self.control_frame = Frame(self.main_window, bg="white")
        self.control_frame.pack(side=LEFT, expand=True, fill="y")

        self.tune_laser_frame = self.tune_laser_window.open(self.control_frame)
        self.tune_laser_frame.pack(side=TOP, fill="both")

        self.tune_detector_frame = self.tune_detector_window.open(self.control_frame)
        self.tune_detector_frame.pack(side=TOP, fill="both")

        self.tune_piezo_frame = self.tune_piezo_window.open(self.control_frame)
        self.tune_piezo_frame.pack(side=TOP, fill="both")

        self.sweep_frame = Frame(self.main_window, bg="white")
        self.sweep_frame.pack(side=RIGHT, expand=True, fill="y")

        self.sweep_wavelength_frame = self.sweep_wavelength_menu_window.open(self.sweep_frame)
        self.sweep_wavelength_frame.pack(side=TOP, fill="both")

        self.figure_frame = Frame(self.main_window, bg="white")
        self.figure_frame.pack(side=RIGHT, expand=True, fill="both")

        self.acquisition_frame = Frame(self.figure_frame, bg="white")
        self.acquisition_frame.pack(side=TOP, expand=True, fill="both")

        self.sweep_wavelength_plot_frame = Frame(self.figure_frame, bg="white")
        self.sweep_wavelength_plot_frame.pack(side=TOP, expand=True, fill="both")

        self.main_window.config(menu=self.menubar)

        self.open_instruments()
        self.toggle_acquisition()
        self.main_iteration()
        self.main_window.mainloop()

    def get_sweep_wavelength_mode(self):
        return self.sweep_wavelength_mode

    def get_save_bool(self):
        return self.save_bool

    def close_application(self):
        self.save_settings()

        if self.acquisition_window is not None:
            self.acquisition_window.close()
        self.close_instruments()
        print("Closing Application")
        self.main_window.quit()

    def do_nothing(self):
        pass

    def toggle_instruments(self):
        if self.is_instruments_on:
            self.close_instruments()
        else:
            self.open_instruments()

    def close_instruments(self):
        if self.is_instruments_on:
            self.is_instruments_on = False
            self.instrument_controller.close_instruments()

    def open_instruments(self):
        if not self.is_instruments_on:
            self.is_instruments_on = True
            self.instrument_controller.open_instruments()

    def set_voltage_sweep_save_path(self, path):
        self.voltage_sweep_save_path = path

    def get_voltage_sweep_save_path(self):
        return self.voltage_sweep_save_path

    def set_sweep_pause_time(self, time):
        self.sweep_pause_time = time

    def get_sweep_pause_time(self):
        return self.sweep_pause_time

    def get_wavelength_sweep_save_path(self):
        return self.wavelength_sweep_save_path

    def set_wavelength_sweep_save_path(self, path):
        self.wavelength_sweep_save_path = path

    def get_wavelength_sweep_save_path(self):
        return self.wavelength_sweep_save_path

    def next_sweep_wavelength_mode(self):
        if self.sweep_wavelength_mode == "Loss":
            self.sweep_wavelength_mode = "DFG"
        elif self.sweep_wavelength_mode == "DFG":
            self.sweep_wavelength_mode = "Follow"
        elif self.sweep_wavelength_mode == "Follow":
            self.sweep_wavelength_mode = "SFG"
        elif self.sweep_wavelength_mode == "SFG":
            self.sweep_wavelength_mode = "None"
        elif self.sweep_wavelength_mode == "None":
            self.sweep_wavelength_mode = "Voltage"
        elif self.sweep_wavelength_mode == "Voltage":
            self.sweep_wavelength_mode = "Power"
        elif self.sweep_wavelength_mode == "Power":
            self.sweep_wavelength_mode = "Loss"
        else:
            print("Wrong Mode")

    def main_iteration(self):
        self.main_window.update()
        self.tune_laser_window.update_window()
        self.tune_detector_window.update_window()
        self.tune_piezo_window.update_window()
        self.sweep_wavelength_menu_window.update_window()
        self.sweep_voltage_menu_window.update_window()
        self.main_window.after(100, self.main_iteration)

    def toggle_acquisition(self):
        if not self.is_acquisition_on:
            self.is_acquisition_on = True
            self.acquisition_window.set_pause_flag(False)
            self.open_instruments()

            self.acquisition_window.setup_figure(self.acquisition_frame)
            self.acquisition_thread = threading.Thread(target=self.acquisition_window.update)
            self.acquisition_thread.start()
        else:
            self.is_acquisition_on = False
            self.acquisition_window.set_pause_flag(True)

    def toggle_save_bool(self):
        self.save_bool = not self.save_bool

    def run_sweep_wavelength(self):
        if not self.is_wavelength_sweep_on:
            self.is_wavelength_sweep_on = True
            self.open_instruments()
            self.sweep_wavelength_plot_window.setup_figure(self.sweep_wavelength_plot_frame)
            self.sweep_wavelength_thread = threading.Thread(target=self.sweep_wavelength_plot_window.update)
            self.sweep_wavelength_thread.start()

    def run_sweep_voltage(self):
        if not self.is_voltage_sweep_on:
            self.is_voltage_sweep_on = True
            self.open_instruments()
            self.sweep_voltage_plot_window.setup_figure(self.sweep_voltage_plot_frame)
            self.sweep_voltage_thread = threading.Thread(target=self.sweep_voltage_plot_window.update)
            self.sweep_voltage_thread.start()

    def run_sweep_osa(self):
        pass

    def load_settings(self):
        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.wavelength_sweep_save_path = settings_dict["wavelength_sweep_save_path"]
            self.voltage_sweep_save_path = settings_dict["voltage_sweep_save_path"]
            self.save_bool = settings_dict["save_bool"]
            self.sweep_wavelength_mode = settings_dict["sweep_wavelength_mode"]

    def save_settings(self):
        dictionary = {"wavelength_sweep_save_path": self.wavelength_sweep_save_path,
                      "voltage_sweep_save_path": self.voltage_sweep_save_path,
                      "save_bool": self.save_bool,
                      "sweep_wavelength_mode": self.sweep_wavelength_mode}

        with open(self.settings_path, "w") as text_file:
            json.dump(dictionary, text_file)

    def optimize_y_and_z(self):
        self.open_instruments()
        self.piezo_optimization_thread = threading.Thread(target=self.optimize_piezo.optimize)
        self.piezo_optimization_thread.start()

    def phase_matching_follow(self):
        if not self.is_wavelength_sweep_on:
            self.is_wavelength_sweep_on = True
            self.open_instruments()
            self.sweep_wavelength_plot_window.setup_figure(self.sweep_wavelength_plot_frame)
            self.sweep_wavelength_thread = threading.Thread(
                target=self.sweep_wavelength_plot_window.follow_phase_matching)
            self.sweep_wavelength_thread.start()

    def sweep_power(self):
        if not self.is_wavelength_sweep_on:
            self.is_wavelength_sweep_on = True
            self.open_instruments()
            self.sweep_wavelength_plot_window.setup_figure(self.sweep_wavelength_plot_frame)
            self.sweep_wavelength_thread = threading.Thread(target=self.sweep_wavelength_plot_window.sweep_power)
            self.sweep_wavelength_thread.start()


GUI_Controller()
