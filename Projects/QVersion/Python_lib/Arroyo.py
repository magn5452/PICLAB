import json

import numpy as np
from matplotlib import pyplot as plt
from pyvisa import constants
from scipy.optimize import fsolve

from Functions.functions import poly21, poly22, poly222


class Arroyo:  # developer: Magnus Linnet Madsen
    # For more information on how to connect to the Arroyo ComboPack look into:
    # https://www.arroyoinstruments.com/product/685-0-5-combopak-500ma-10v-laser-3a-3-5v-tec/
    # https://www.arroyoinstruments.com/wp-content/uploads/2021/01/ArroyoComputerInterfacingManual.pdf

    # You need to install the USB driver from the webpage to connect via proper connect via visa.

    def __init__(self, resource_manager, settings_path, location_visa):
        'Connect to Arroyo 4302 current source on serial port 5'

        self.settings_path = settings_path

        self.arroyo = resource_manager.open_resource(location_visa)

        self.wavelength_model = lambda current, temperature: self.model_calibration(current, temperature)
        self.temperature_set = 22
        self.current_set = 195.0
        self.wavelength_set = self.wavelength_model(self.current_set, self.temperature_set)

        # Set serial comm parameters
        self.arroyo.baud_rate = 38400
        self.arroyo.timeout = 500
        self.arroyo.write_termination = '\n'
        self.arroyo.send_end = True
        self.arroyo.data_bits = 8
        self.arroyo.stop_bits = constants.StopBits['one']
        self.arroyo.parity = constants.Parity['none']

        self.arroyo.write("TEC:LIMit:ITE " + str(2.3))
        self.arroyo.write("TEC:LIMit:V " + str(2.9))
        self.arroyo.write("TEC:MODE:T")
        self.arroyo.write("TEC:T " + str(self.temperature_set))

        self.set_maximum_voltage(2)
        self.set_maximum_current(200)
        self.arroyo.write("LASer:LIMit:THIgh " + str(45))
        self.arroyo.write("LASer:LIMit:TLOw " + str(10))
        self.arroyo.write("LASer:I " + str(self.current_set))

        self.turn_on_laser()

        print_bool = False
        self.ask("TEC:MODE?", print_bool)
        self.ask("TEC:T?", print_bool)
        self.ask("TEC:OUT?", print_bool)

        self.ask("LAS:MODE?", print_bool)
        self.ask("LAS:I?", print_bool)
        self.ask("LAS:LDV?", print_bool)
        self.ask("LAS:OUT?", print_bool)

        self.is_alive()

        self.load_settings()

    def is_alive(self):
        is_alive = self.arroyo.query('*IDN?')
        if is_alive != 0:
            print("Arroyo is alive")

    def ask(self, command, print_bool=False):
        response = self.arroyo.query(command)
        if print_bool:
            print("Command: " + command + ", Response: " + response)
        return response

    def reset(self):
        """Reset"""
        self.arroyo.query('*RST')
        self.arroyo.query('*CLS')

    def toggle_laser(self):
        print("toggle")
        if self.ask("LAS:OUT?", True):
            self.turn_off_laser()
        else:
            print("Turn on")
            self.turn_on_laser()

    def turn_on_laser(self):
        self.turn_on_TEC()
        self.arroyo.write("LAS:OUT " + str(1))

    def turn_off_laser(self):
        self.turn_off_TEC()
        self.arroyo.write("LAS:OUT " + str(0))

    def turn_on_TEC(self):
        self.arroyo.write("TEC:OUT " + str(1))

    def float(self, val):
        try:
            return float(val)
        except:
            return 0

    def turn_off_TEC(self):
        self.arroyo.write("TEC:OUT " + str(0))

    def get_wavelength(self):
        return self.wavelength_set

    def get_power(self):
        return 0

    def get_wavelength_set(self):
        return self.wavelength_set

    def get_power_set(self):
        return self.get_temperature()


    def get_current(self):
        return self.float(self.ask("LAS:I?", True))

    def get_voltage(self):
        return self.float(self.ask("LAS:LDV?", True))

    def get_temperature(self):

        return self.float(self.ask("TEC:T?", True))

    def set_maximum_current(self, I):
        if I <= 200:
            self.arroyo.write("LAS:LIM:I " + str(I))
        else:
            print("The specified current " + str(I) + " mA is above the maximum current of 200 mA")

    def set_maximum_voltage(self, V):
        if V <= 2:
            self.arroyo.write("LAS:LIM:LDV " + str(V))
        else:
            print("The specified voltage " + str(V) + " V is above the maximum voltage of 2 V")

    def set_wavelength(self, wavelength):
        self.set_wavelength_from_temperatur(wavelength)

    def set_wavelength_from_current(self, wavelength):
        func = lambda current: self.wavelength_model(current, self.temperature_set) - wavelength
        current_guess = self.current_set
        current_solution = fsolve(func, current_guess)
        self.set_current(current_solution[0])

    def set_wavelength_from_temperatur(self, wavelength):
        func = lambda temperature: self.wavelength_model(self.current_set, temperature) - wavelength
        temperature_guess = self.temperature_set
        temperature_solution = fsolve(func, temperature_guess)
        self.set_temperature(temperature_solution[0])
        plt.pause(2)

    def set_current(self, current):
        if current > 200 or not self.arroyo.write("LASer:I " + str(current)):
            print("Unable to set current")
        else:
            self.wavelength_set = self.wavelength_model(current, self.temperature_set)
            self.current_set = current

    def set_temperature(self, temperature):
        if temperature > 35 or temperature < 20 or not self.arroyo.write("TEC:T " + str(temperature)):
            print("Temperature is not within range")
        else:
            self.arroyo.write("TEC:T " + str(temperature))
            self.wavelength_set = self.wavelength_model(self.current_set, temperature)
            self.temperature_set = temperature

    def gradually_set_temperature(self, target_temperature):
        start_temperature = self.get_temperature()
        temperature_list = np.arange(start_temperature, target_temperature, 1)
        print(start_temperature)
        print(target_temperature)
        for temperature in temperature_list:
            print(temperature)
            self.arroyo.write("TEC:T " + str(temperature))
            plt.pause(1)

    def print_emission_status(self):
        if bool(self.ask("LASER:OUTput?")):
            print("Emission status: The laser is on and emitting´light")
        else:
            print("Emission status: The laser is off and not emitting any light")

    def close(self):
        """End communication"""
        self.save_settings()
        self.arroyo.write("LASER:OUTput " + str(0))
        self.arroyo.write("TEC:OUTput " + str(0))
        self.arroyo.close()

    def model_calibration(self, I, T):
        """
        Poly21 fit model of the wavelength of the central peak of Arroyo laser measured on the on Yokogawa

        @param I: Current [mA]
        @param T: Temperature [C]
        @return: Wavelength of Arroyo Laser [nm]
        """

        # poly22((I, T), 2.31381220e+03,  2.26273409e-02,  1.71199320e-01, -1.40816348e-05, 9.47478970e-05,  6.42857141e-04)
        # poly21((I, T), 2.31348863e+03,  2.26273409e-02,  2.00127891e-01, -1.40816348e-05, 9.47478970e-05)
        # poly21((I, T), 2.31480233e+03, 1.26166667e-02, 1.42500000e-01, 3.74999998e-04,
        #        1.02666664e-04)
        return poly222((I, T), 2.31389091e+03, 2.39794447e-02, 1.52386054e-01, 1.17614905e-04,
                       7.11415203e-05, 1.29244957e-03, 9.96585633e-07, -7.82251331e-06)
        # return poly222((I, T), 2.31493315e+03, 1.37859444e-02, 6.89041391e-02, 8.16156022e-04,
        #               9.10611855e-05, 2.96172910e-03, 1.63859682e-07, -1.93236935e-05)

    def load_settings(self):
        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.set_wavelength_nm = settings_dict["wavelength"]
            self.set_wavelength(self.set_wavelength_nm)


    def save_settings(self):
        dictionary = {
            "wavelength": self.set_wavelength_nm,
        }

        with open(self.settings_path, "w") as text_file:
            json.dump(dictionary, text_file)

    def get_name(self):
        return "Arroyo laser"

    def get_min_wavelength(self):
        return 2324

    def get_max_wavelength(self):
        return 2326

    def get_min_power(self):
        return self.get_current()

    def get_max_power(self):
        return self.get_temperature()