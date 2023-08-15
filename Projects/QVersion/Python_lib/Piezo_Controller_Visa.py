import json
from ctypes import *

import numpy as np
from matplotlib import pyplot as plt

from Python_lib.MDT_COMMAND_LIB_TEST import *
from Python_lib.MDT_COMMAND_LIB import *


class Piezo_Controller_Visa:

    def __init__(self, resource_manager, settings_path, resource):
        self.settings_path = settings_path
        print(self.settings_path)
        self.resource_manager = resource_manager
        self.piezo_controller = resource_manager.open_resource(resource)

        self.x_resolution = None
        self.y_resolution = None
        self.z_resolution = None

        self.x_voltage = None
        self.y_voltage = None
        self.z_voltage = None

        self.min_x_voltage_set = None
        self.min_y_voltage_set = None
        self.min_z_voltage_set = None

        self.max_x_voltage_set = None
        self.max_y_voltage_set = None
        self.max_z_voltage_set = None

        self.is_alive()
        self.open()

    def scan(self):
        pass

    def is_alive(self):
        is_alive = self.piezo_controller.query('*IDN?')
        if is_alive != 0:
            print("Piezo controller is alive")

    def set_min_x_voltage(self, voltage):
        self.min_x_voltage_set = voltage
        self.piezo_controller.write("xmin=" + str(voltage))

    def set_max_x_voltage(self, voltage):
        self.max_x_voltage_set = voltage
        self.piezo_controller.write("xmax=" + str(voltage))

    def set_min_y_voltage(self, voltage):
        self.min_y_voltage_set = voltage
        self.piezo_controller.write("ymin=" + str(voltage))

    def set_max_y_voltage(self, voltage):
        self.max_y_voltage_set = voltage
        self.piezo_controller.write("ymax=" + str(voltage))

    def set_min_z_voltage(self, voltage):
        self.min_z_voltage_set = voltage
        self.piezo_controller.write("zmin=" + str(voltage))

    def set_max_z_voltage(self, voltage):
        self.max_z_voltage_set = voltage
        self.piezo_controller.write("zmax=" + str(voltage))

    def set_x_voltage(self, voltage):
        self.x_voltage = voltage
        self.piezo_controller.write("xvoltage=" + str(voltage))

    def set_y_voltage(self, voltage):
        self.y_voltage = voltage
        self.piezo_controller.write("yvoltage=" + str(voltage))

    def set_z_voltage(self, voltage):
        self.z_voltage = voltage
        self.piezo_controller.write("zvoltage=" + str(voltage))

    def set_x_resolution(self, resolution):
        self.x_resolution = resolution

    def set_y_resolution(self, resolution):
        self.y_resolution = resolution

    def set_z_resolution(self, resolution):
        self.z_resolution = resolution

    def get_min_x_voltage(self):
        return self.min_x_voltage_set

    def get_max_x_voltage(self):
        return self.max_x_voltage_set

    def get_min_y_voltage(self):
        return self.min_y_voltage_set

    def get_max_y_voltage(self):
        return self.max_y_voltage_set

    def get_min_z_voltage(self):
        return self.min_z_voltage_set

    def get_max_z_voltage(self):
        return self.max_z_voltage_set

    def get_float(self, command, print_bool=False):
        self.piezo_controller.write(command)
        anwser_string = self.piezo_controller.read()
        if print_bool:
            print(anwser_string)
        index = anwser_string.find("=")
        return float(anwser_string[index + 1:-1])

    def get_x_resolution(self):
        return self.x_resolution

    def get_y_resolution(self):
        return self.y_resolution

    def get_z_resolution(self):
        return self.z_resolution

    def get_x_voltage(self):
        return self.x_voltage

    def get_y_voltage(self):
        return self.y_voltage

    def get_z_voltage(self):
        return self.z_voltage

    def increment_x_voltage(self):
        self.set_x_voltage(self.x_voltage + self.x_resolution)

    def set_display_intensity(self, intensity):
        return self.piezo_controller.write("intensity=" + str(intensity))

    def get_display_intensity(self):
        return self.get_float("intensity?")

    def load_settings(self):
        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.set_x_voltage(settings_dict["x_voltage"])
            self.set_y_voltage(settings_dict["y_voltage"])
            self.set_z_voltage(settings_dict["z_voltage"])
            self.set_x_resolution(settings_dict["x_resolution"])
            self.set_y_resolution(settings_dict["y_resolution"])
            self.set_z_resolution(settings_dict["z_resolution"])

    def save_settings(self):
        dictionary = {
            "x_voltage": self.x_voltage,
            "y_voltage": self.y_voltage,
            "z_voltage": self.z_voltage,
            "x_resolution": self.x_resolution,
            "y_resolution": self.y_resolution,
            "z_resolution": self.z_resolution
        }
        print(self.settings_path)
        with open(self.settings_path, "w") as text_file:
            json.dump(dictionary, text_file)

    def open(self):
        self.load_settings()

    def close(self):
        self.save_settings()
        self.piezo_controller.close()


class Piezo_Controller_Thorlabs:

    def __init__(self, settings_path, serial_number):
        self.settings_path = settings_path
        mdtListDevices()
        self.handle = CommonFunc(serial_number)
        print("Handle:", self.handle)

        self.x_resolution = None
        self.y_resolution = None
        self.z_resolution = None

        self.x_voltage_set = None
        self.y_voltage_set = None
        self.z_voltage_set = None

        self.min_x_voltage_set = None
        self.min_y_voltage_set = None
        self.min_z_voltage_set = None

        self.max_x_voltage_set = None
        self.max_y_voltage_set = None
        self.max_z_voltage_set = None

        self.open()

    def get_handle(self):
        return self.handle

    def set_min_x_voltage(self, voltage):
        pass

    def set_max_x_voltage(self, voltage):
        pass

    def set_min_y_voltage(self, voltage):
        pass

    def set_max_y_voltage(self, voltage):
        pass

    def set_min_z_voltage(self, voltage):
        pass

    def set_max_z_voltage(self, voltage):
        pass

    def set_xyz_voltage(self, x_voltage, y_voltage, z_voltage):
        """ Set the output voltage for the X axis.
        Args:
            voltage: the input voltage range:(0 ~ limit voltage)
        Returns:
            0: Success; negative number: failed.
        """
        if x_voltage == self.x_voltage_set and y_voltage == self.y_voltage_set and z_voltage == self.z_voltage_set :
            return 1
        self.x_voltage_set = x_voltage
        self.y_voltage_set = y_voltage
        self.z_voltage_set = z_voltage

        succes = cmdSetXYZAxisVoltage(self.handle, self.x_voltage_set, self.y_voltage_set, self.z_voltage_set)
        return succes

    def set_x_voltage(self, voltage):
        """ Set the output voltage for the X axis.
        Args:
            voltage: the input voltage range:(0 ~ limit voltage)
        Returns:
            0: Success; negative number: failed.
        """
        if voltage == self.x_voltage_set:
            return 1
        self.x_voltage_set = voltage
        succes = cmdSetXAxisVoltage(self.handle, self.x_voltage_set)
        return succes

    def set_y_voltage(self, voltage):
        """ Set the output voltage for the Y axis.
        Args:
            voltage: the input voltage range:(0 ~ limit voltage)
        Returns:
            0: Success; negative number: failed.
        """
        if voltage == self.y_voltage_set:
            return 1
        self.y_voltage_set = voltage
        succes = cmdSetYAxisVoltage(self.handle, self.y_voltage_set)
        return succes

    def set_z_voltage(self, voltage):
        """ Set the output voltage for the X axis.
        Args:
            voltage: the input voltage range:(0 ~ limit voltage)
        Returns:
            0: Success; negative number: failed.
        """
        if voltage == self.z_voltage_set:
            return 1
        self.z_voltage_set = voltage
        succes = cmdSetZAxisVoltage(self.handle, self.z_voltage_set)
        return succes

    def get_min_x_voltage(self):
        """ Get the minimum output voltage limit for X axis.
        Args:
        Returns:
            voltage: the minimum voltage of the X-axis
            succes: 0: Success; negative number: failed.
        """
        vol = c_double(0)
        succes = cmdGetXAxisMinVoltage(self.handle, vol)
        voltage = vol.value
        return voltage, succes

    def get_max_x_voltage(self):
        """ Get the maximum output voltage limit for X axis.
        Args:
        Returns:
            voltage: the maxmimum voltage of the X:axis
            succes: 0: Success; negative number: failed.
        """
        vol = c_double(0)
        succes = cmdGetXAxisMinVoltage(self.handle, vol)
        voltage = vol.value
        return voltage, succes

    def get_min_y_voltage(self):
        """ Get the maximum output voltage limit for X axis.
        Args:
        Returns:
            voltage: the minium  voltage of the X:axis
            succes: 0: Success; negative number: failed.
        """
        vol = c_double(0)
        succes = cmdGetXAxisMinVoltage(self.handle, vol)
        voltage = vol.value
        return voltage, succes

    def get_max_y_voltage(self):
        pass

    def get_min_z_voltage(self):
        pass

    def get_max_z_voltage(self):
        pass

    def get_x_resolution(self):
        pass

    def get_y_resolution(self):
        pass

    def get_z_resolution(self):
        pass

    def get_x_voltage(self):
        """ Get the X axis output voltage.
        Returns:
            voltage: the x axis voltage
        """
        plt.pause(0.01)
        vol = c_double(0)
        succes = cmdGetXAxisVoltage(self.handle, vol)
        voltage = vol.value
        return voltage

    def get_y_voltage(self):
        """ Get the X axis output voltage.
        Returns:
            voltage: the x axis voltage
        """
        plt.pause(0.01)
        vol = c_double(0)
        succes = cmdGetYAxisVoltage(self.handle, vol)
        voltage = vol.value
        return voltage

    def get_z_voltage(self):
        """ Get the X axis output voltage.
        Returns:
            voltage: the x axis voltage
        """
        plt.pause(0.01)
        vol = c_double(0)
        succes = cmdGetZAxisVoltage(self.handle, vol)
        voltage = vol.value
        return voltage

    def get_x_voltage_set(self):
        return self.x_voltage_set

    def get_y_voltage_set(self):
        return self.y_voltage_set

    def get_z_voltage_set(self):
        return self.z_voltage_set

    def set_x_resolution(self, resolution):
        self.x_resolution = resolution

    def set_y_resolution(self, resolution):
        self.y_resolution = resolution

    def set_z_resolution(self, resolution):
        self.z_resolution = resolution

    def get_x_resolution(self):
        return self.x_resolution

    def get_y_resolution(self):
        return self.y_resolution

    def get_z_resolution(self):
        return self.z_resolution

    def load_settings(self):
        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.set_x_voltage(settings_dict["x_voltage"])
            self.set_y_voltage(settings_dict["y_voltage"])
            self.set_z_voltage(settings_dict["z_voltage"])
            self.set_x_resolution(settings_dict["x_resolution"])
            self.set_y_resolution(settings_dict["y_resolution"])
            self.set_z_resolution(settings_dict["z_resolution"])

    def save_settings(self):
        dictionary = {
            "x_voltage": self.x_voltage_set,
            "y_voltage": self.y_voltage_set,
            "z_voltage": self.z_voltage_set,
            "x_resolution": self.x_resolution,
            "y_resolution": self.y_resolution,
            "z_resolution": self.z_resolution
        }
        print(self.settings_path)
        with open(self.settings_path, "w") as text_file:
            json.dump(dictionary, text_file)

    def open(self):
        self.load_settings()

    def close(self):
        self.save_settings()
        mdtClose(self.handle)