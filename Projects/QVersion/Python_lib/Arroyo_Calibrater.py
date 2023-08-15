import pyvisa as visa
from matplotlib import pyplot as plt

from Functions.functions import poly21, poly22, poly222
from Python_lib.Arroyo import Arroyo
from Python_lib.Yokogawa import Yokogawa
import numpy as np
import scipy


class Arroyo_Calibrater:

    def __init__(self, yokogawa=None, arroyo=None):
        self.yokogawa = yokogawa
        self.arroyo = arroyo

    def connect(self):
        if self.yokogawa is None or self.arroyo is None:
            resource_manager = visa.ResourceManager()
            list = resource_manager.list_resources()

            self.arroyo = Arroyo(resource_manager, 'ASRL3::INSTR')
            self.arroyo.set_temperature(25)
            self.arroyo.set_current(150)

            self.yokogawa = Yokogawa(resource_manager, 'GPIB0::7::INSTR')
            self.yokogawa.set_sensitivity('MID')
            self.yokogawa.set_wavelength_center(self.arroyo.get_wavelength())
            self.yokogawa.set_span_wav(15)  # [nm]
            self.yokogawa.set_RBW(0.05)

    def calibrate(self):
        self.connect()
        [wavelength_fit_list, current_fit_list, temperature_fit_list] = self.collect_calibration()
        print(wavelength_fit_list)
        print(current_fit_list)
        print(temperature_fit_list)
        model = self.fit(wavelength_fit_list, current_fit_list, temperature_fit_list)
        self.arroyo.close()
        return model

    def collect_calibration(self):
        min_temperature = 20
        max_temperature = 30
        delta_temperature = 1
        min_current = 50
        max_current = 190
        delta_current = 5
        temperature_collect_list = range(min_temperature, max_temperature + 1, delta_temperature)
        current_collect_list = range(min_current, max_current + 1, delta_current)

        wavelength_fit_list = []
        current_fit_list = []
        temperature_fit_list = []
        for temperature in temperature_collect_list:
            self.arroyo.set_temperature(temperature)
            for current in current_collect_list:
                self.arroyo.set_current(current)
                current_fit_list.append(current)
                temperature_fit_list.append(temperature)
                plt.pause(5)
                [max_wavelength_nm, max_power_dBm_pr_nm, max_index] = self.yokogawa.get_max_trace()
                wavelength_fit_list.append(max_wavelength_nm)
                print(max_wavelength_nm)

        return wavelength_fit_list, current_fit_list, temperature_fit_list

    def test_calibration(self):
        self.connect()
        wavelength_list = [2319, 2320, 2321, 2322, 2323]
        for wavelength in wavelength_list:
            self.arroyo.set_wavelength_nm(wavelength)
            plt.pause(5)
            [max_wavelength_nm, max_power_dBm_pr_nm, max_index] = self.yokogawa.get_max_trace()
            print(str(max_wavelength_nm) + " and " + str(wavelength))
            print(str(self.arroyo.get_current()))
            print(str(self.arroyo.get_current()))
    def fit(self, wavelength_fit_list, current_fit_list, temperature_fit_list):
        param0 = 1, 1, 1, 1, 1, 1, 1, 1
        model = scipy.optimize.curve_fit(poly222, (current_fit_list, temperature_fit_list), wavelength_fit_list,
                                         param0)
        return model
