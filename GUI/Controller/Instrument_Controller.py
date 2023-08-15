import json
import threading

import pyvisa as visa
from matplotlib import pyplot as plt

from Python_lib.Agilent import Agilent
from Python_lib.Arroyo import Arroyo
from Python_lib.EXFO import EXFO
from Python_lib.Piezo_Controller_Visa import Piezo_Controller_Thorlabs
from Python_lib.Siglent import Siglent
from Python_lib.Thorlabs_PM100U import Thorlabs_PM100U
from Python_lib.Toptica_CTL950 import Toptica_CTL950
from Python_lib.Yokogawa import Yokogawa
from GUI.Functions.functions import *


class Instrument_Controller:
    def __init__(self):
        self.power_step = None
        self.power_max = None
        self.power_min = None
        self.toptica_laser = None
        self.exfo_laser = None

        self.settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/instrument_controller_settings.txt"
        self.resource_manager = visa.ResourceManager()
        self.detector_list = []
        self.laser_list = []
        self.piezo_list = []
        self.waveform_generator_list = []
        self.optical_spectrum_analyzer_list = []
        self.wavelength_min = None
        self.wavelength_max = None

        self.initial_wavelength_nm = None
        self.target_laser_index = None
        self.target_detector_index = None
        self.target_piezo_index = 0
        self.wavelength_step = None

        self.voltage_step = None
        self.voltage_min = None
        self.voltage_max = None

        self.input_piezo_controller = None
        self.output_piezo_controller = None

        self.siglent_connect_bool = None
        self.arroyo_connect_bool = None
        self.toptica_connect_bool = None
        self.agilent_connect_bool = None
        self.yokogawa_connect_bool = None
        self.exfo_connect_bool = None
        self.input_piezo_controller_connect_bool = None
        self.output_piezo_controller_connect_bool = None

        self.siglent_connected_bool = None
        self.arroyo_connected_bool = None
        self.toptica_connected_bool = None
        self.agilent_connected_bool = None
        self.yokogawa_connected_bool = None
        self.exfo_connected_bool = None
        self.input_piezo_controller_connected_bool = None
        self.output_piezo_controller_connected_bool = None



        self.instrument_connected_bool = False

        self.load_settings()

    def load_settings(self):
        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.initial_wavelength_nm = settings_dict["initial_wavelength_nm"]
            self.target_laser_index = settings_dict["target_laser_index"]
            self.target_detector_index = settings_dict["target_detector_index"]
            self.wavelength_step = settings_dict["wavelength_step"]  # nm
            self.power_step = settings_dict["power_step"]  # mW

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

    def get_min_power(self):
        if self.power_min is None:
            return self.get_target_laser().get_min_power()
        else:
            return self.power_min

    def get_max_power(self):
        if self.power_max is None:
            return self.get_target_laser().get_max_power()
        else:
            return self.power_max

    def get_sweep_power(self):
        return self.power_step

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

    def set_min_power(self, power):
        if self.get_target_laser().get_min_power() <= power <= self.get_target_laser().get_max_power() and power < self.get_max_power():
            self.wavelength_min = power
        else:
            print("power " + str(power) + " is not a valid minimum power for the " + str(
                self.get_target_laser().get_name()))

    def set_max_power(self, power):
        if self.get_target_laser().get_min_power() <= power <= self.get_target_laser().get_max_power() and self.get_min_power() < power:
            self.power_max = power
        else:
            print("power " + str(power) + " is not a valid maximum power for the " + str(
                self.get_target_laser().get_name()))

    def set_sweep_power(self, power):
        self.power_step = power

    def open_instruments(self):
        if not self.instrument_connected_bool:

            thread_list = []
            resource_list = self.resource_manager.list_resources()
            print("List of resources: " + str(resource_list))
            for resource in resource_list:

                if resource == "USB0::0x1313::0x8076::M00905457::INSTR":
                    #self.open_thorlabs_57(resource)
                    detector_57_start_thread = threading.Thread(target=self.open_thorlabs_57, args=[resource])
                    detector_57_start_thread.start()
                    thread_list.append(detector_57_start_thread)

                if resource == "USB0::0x1313::0x8076::M00905456::INSTR":
                    #self.open_thorlabs_56(resource)
                    detector_56_start_thread = threading.Thread(target=self.open_thorlabs_56, args=[resource])
                    detector_56_start_thread.start()
                    thread_list.append(detector_56_start_thread)

                if resource == "USB0::0x1313::0x8076::M00905455::INSTR":
                    #self.open_thorlabs_55(resource)
                    detector_55_start_thread = threading.Thread(target=self.open_thorlabs_55, args=[resource])
                    detector_55_start_thread.start()
                    thread_list.append(detector_55_start_thread)

                if resource == "ASRL3::INSTR" and self.arroyo_connect_bool:
                    #self.open_arroyo(resource)
                    arroyo_start_thread = threading.Thread(target=self.open_arroyo, args=[resource])
                    arroyo_start_thread.start()
                    thread_list.append(arroyo_start_thread)

                if resource == "GPIB1::7::INSTR" and self.yokogawa_connect_bool:
                    #self.open_yokogawa(resource)
                    yokogawa_start_thread = threading.Thread(target=self.open_yokogawa, args=[resource])
                    yokogawa_start_thread.start()
                    thread_list.append(yokogawa_start_thread)

                if resource == "GPIB1::10::INSTR" and self.exfo_connect_bool:
                    self.open_exfo(resource)
                    #exfo_start_thread = threading.Thread(target=self.open_exfo, args=[resource])
                    #exfo_start_thread.start()
                    #thread_list.append(exfo_start_thread)

                if resource == "GPIB0::18::INSTR" and self.agilent_connect_bool:
                    #self.open_agilent(resource)
                    agilent_start_thread = threading.Thread(target=self.open_agilent, args=[resource])
                    agilent_start_thread.start()
                    thread_list.append(agilent_start_thread)

                if resource == "USB0::0xF4EC::0x1101::SDG6XBAQ3R0181::INSTR" and self.siglent_connect_bool:
                    #self.open_siglent(resource)
                    siglent_start_thread = threading.Thread(target=self.open_siglent, args=[resource])
                    siglent_start_thread.start()
                    thread_list.append(siglent_start_thread)

            if self.toptica_connect_bool:
                self.open_toptica()
                #toptica_start_thread = threading.Thread(target=self.open_toptica)
                #toptica_start_thread.start()
                #thread_list.append(toptica_start_thread)

            if self.input_piezo_controller_connect_bool:
                #self.open_input_piezo()
                input_piezo_start_thread = threading.Thread(target=self.open_input_piezo)
                input_piezo_start_thread.start()
                thread_list.append(input_piezo_start_thread)

            if self.output_piezo_controller_connect_bool:
                #self.open_output_piezo()
                output_piezo_start_thread = threading.Thread(target=self.open_output_piezo)
                output_piezo_start_thread.start()
                thread_list.append(output_piezo_start_thread)

            self.instrument_connected_bool = True

            for thread in thread_list:
                thread.join()

    def open_output_piezo(self):
        settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/output_piezo_controller_settings.txt"
        try:
            self.output_piezo_controller = Piezo_Controller_Thorlabs(settings_path, '2207070466-03')
            if self.output_piezo_controller.get_handle() >= 0:
                self.piezo_list.append((self.output_piezo_controller))
        except:
            print("Could not connect to input piezo")

    def open_input_piezo(self):
        settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/input_piezo_controller_settings.txt"
        try:
            self.input_piezo_controller = Piezo_Controller_Thorlabs(settings_path, '1908086985-08')
            if self.input_piezo_controller.get_handle() >= 0:
                self.piezo_list.append((self.input_piezo_controller))
        except:
            print("Could not connect to input piezo")

    def open_toptica(self):
        settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/toptica_settings.txt"
        try:
            self.toptica_laser = Toptica_CTL950(settings_path)
            self.laser_list.append(self.toptica_laser)
        except:
            print("Could not connect to Toptica Laser")


    def open_siglent(self, resource):
        settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/siglent_settings.txt"
        siglent = Siglent(self.resource_manager, settings_path, resource)
        self.waveform_generator_list.append(siglent)

    def open_agilent(self):
        agilent = Agilent(self.resource_manager, GPIB_interface=18)
        self.laser_list.append(agilent)

    def open_exfo(self, resource):
        settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/exfo_settings.txt"
        self.exfo_laser = EXFO(self.resource_manager, settings_path, resource)
        self.exfo_laser.laser_on()
        self.laser_list.append(self.exfo_laser)

    def open_yokogawa(self, resource):
        settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/yokogawa_settings.txt"
        yokogawa = Yokogawa(self.resource_manager, resource, settings_path)
        self.optical_spectrum_analyzer_list.append(yokogawa)
        self.detector_list.append(yokogawa)

    def open_arroyo(self, resource):
        try:
            settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/arroyo_settings.txt"
            arroyo_laser = Arroyo(self.resource_manager, settings_path, resource)
            self.laser_list.append(arroyo_laser)
        except visa.errors.VisaIOError:
            print("Could not connect to Arroyo Laser. Did you turn it on?")

    def open_thorlabs_55(self, resource):
        try:
            settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/thorlabs_55_settings.txt"
            detector = Thorlabs_PM100U(self.resource_manager, resource, settings_path)
            self.detector_list.append(detector)
        except:
            print("Could not connect to Thorlabs 55")

    def open_thorlabs_56(self, resource):
        try:
            settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/thorlabs_56_settings.txt"
            detector = Thorlabs_PM100U(self.resource_manager, resource, settings_path)
            self.detector_list.append(detector)
        except:
            print("Could not connect to Thorlabs 56")

    def open_thorlabs_57(self, resource):
        try:
            settings_path = "C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Settings/thorlabs_57_settings.txt"
            detector = Thorlabs_PM100U(self.resource_manager, resource, settings_path)
            self.detector_list.append(detector)
        except:
            print("Could not connect to Thorlabs 57")

    def get_laser_list(self):
        return self.laser_list

    def get_toptica_laser(self):
        return self.toptica_laser

    def get_exfo_laser(self):
        return self.exfo_laser

    def get_detector_list(self):
        return self.detector_list

    def get_piezo_list(self):
        return self.piezo_list

    def get_waveform_generator_list(self):
        return self.waveform_generator_list

    def set_target_laser_index(self, index):
        self.target_laser_index = np.mod(index, len(self.laser_list))
        self.wavelength_min = None
        self.wavelength_max = None

    def set_target_detector_index(self, index):
        self.target_detector_index = np.mod(index, len(self.detector_list))

    def set_target_piezo_index(self, index):
        self.target_piezo_index = np.mod(index, len(self.piezo_list))

    def next_laser(self):
        self.set_target_laser_index(self.target_laser_index + 1)

    def previous_laser(self):
        self.set_target_laser_index(self.target_laser_index - 1)

    def next_detector(self):
        print("next_detector")
        self.set_target_detector_index(self.target_detector_index + 1)

    def next_piezo(self):
        print("next_piezo")
        self.set_target_piezo_index(self.target_piezo_index + 1)

    def previous_detector(self):
        self.set_target_detector_index(self.target_detector_index - 1)

    def update_detector_wavelength(self, wavelength):
        for detector in self.detector_list:
            detector.set_detector_wavelength(wavelength)

    def get_target_laser(self):
        return self.laser_list[self.get_target_laser_index()]

    def get_target_detector(self):
        return self.detector_list[self.get_target_detector_index()]

    def get_target_piezo(self):
        return self.piezo_list[self.get_target_piezo_index()]

    def get_target_detector_index(self):
        return np.mod(self.target_detector_index, len(self.detector_list))

    def get_target_laser_index(self):
        return np.mod(self.target_laser_index, len(self.laser_list))

    def get_target_piezo_index(self):
        return np.mod(self.target_piezo_index, len(self.piezo_list))

    def save_settings(self):
        dictionary = {"initial_wavelength_nm": float(self.initial_wavelength_nm),
                      "target_laser_index": int(self.target_laser_index),
                      "target_detector_index": int(self.target_detector_index),
                      "wavelength_step": float(self.wavelength_step),
                      "voltage_step": float(self.voltage_step),
                      "power_step": float(self.power_step),
                      "min_voltage": float(self.voltage_min),
                      "max_voltage": float(self.voltage_max),
                      "siglent_connect_bool": self.siglent_connect_bool,
                      "toptica_connect_bool": self.toptica_connect_bool,
                      "agilent_connect_bool": self.agilent_connect_bool,
                      "yokogawa_connect_bool": self.yokogawa_connect_bool,
                      "exfo_connect_bool": self.exfo_connect_bool,
                      "arroyo_connect_bool": self.arroyo_connect_bool,
                      "input_piezo_controller_connect_bool": self.input_piezo_controller_connect_bool,
                      "output_piezo_controller_connect_bool": self.output_piezo_controller_connect_bool}

        with open(self.settings_path, "w") as text_file:
            json.dump(dictionary, text_file)

    def close_instruments(self):
        self.instrument_connected_bool = False
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
        for piezo in self.piezo_list:
            piezo.close()
        plt.pause(1)


