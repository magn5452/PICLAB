#!/usr/bin/env python
import json

import matplotlib.pyplot as plt
import numpy as np

from GUI.Functions.functions import power_dBm_to_W


# from scipy.interpolate import interp1d

# AQ63XX OSA

class Yokogawa:

    def __init__(self, resource_manager, yoko_conf, settings_path):
        """Connect to OSA"""
        self.settings_path = settings_path
        self.detector_averaging = 1
        self.detector_power_get = 1
        self.detector_wavelength_set = 1550
        self.wavelength_center_set = 1550
        self.wavelength_span_set = 6
        self.meter = resource_manager.open_resource(yoko_conf)
        self.meter.timeout = 5 * 60e3
        self.reset()
        wait = 0
        while (not wait):
            self.meter.write('*OPC?')
            wait = self.meter.read()
        self.meter.write('*IDN?')
        self.info = self.meter.read()
        wait = 0
        while (not wait):
            self.meter.write('*OPC?')
            wait = self.meter.read()

        self.set_sensitivity('NORMAL')  # NORM/HOLD, NORM/AUTO, NORMAL, MID, HIGH1, HIGH2, HIGH3
        self.set_sweep('SINGLE')  # SINGLE, REPEAT, AUTO
        self.is_alive()
        self.set_RBW(0.05)  # minimum of 0.05 nm
        self.set_sweep_speed('2x')  # 1x for lasers, 2x for broadband
        self.set_y_axis_unit('DBM')  # 'DBM/NM' or 'DBM'
        self.set_wavelength_center(self.wavelength_center_set)
        self.set_wavelength_span(self.wavelength_span_set)
        self.meter.write(':SENS:SWE:POINTS:AUTO 1') # sampling points auto

        #self.load_settings()


    def is_alive(self):
        is_alive = self.meter.write('*IDN?')
        if is_alive != 0:
            print("Yokogawa is alive")

    def set_sensitivity(self, sens_mode):
        if (sens_mode == 'NORM/HOLD'):
            sens_mode_Yoko = '0'
        elif (sens_mode == 'NORM/AUTO'):
            sens_mode_Yoko = '1'
        elif (sens_mode == 'MID'):
            sens_mode_Yoko = '2'
        elif (sens_mode == 'HIGH1'):
            sens_mode_Yoko = '3'
        elif (sens_mode == 'HIGH2'):
            sens_mode_Yoko = '4'
        elif (sens_mode == 'HIGH3'):
            sens_mode_Yoko = '5'
        else:  # NORMAL
            sens_mode_Yoko = '6'

        msg = ':SENS:SENS %s' % (sens_mode_Yoko)
        self.meter.write(msg)

    def set_sweep(self, sweep_mode):
        if (sweep_mode == 'SINGLE'):
            sweep_mode_Yoko = '1'
        elif (sweep_mode == 'REPEAT'):
            sweep_mode_Yoko = '2'
        else:  # AUTO
            sweep_mode_Yoko = '3'

        msg = ':INIT:SMOD %s' % (sweep_mode_Yoko)
        self.meter.write(msg)

    def set_sweep_speed(self, speed):
        # 1x for lasers, 2x for broadband
        msg = ':SENS:SWE:SPE %s' % (speed)
        self.meter.write(msg)

    def set_y_axis_unit(self, unit):
        msg = ':DISP:TRAC:Y1:UNIT %s' % (unit)  # 'DBM/NM' or 'DBM'
        self.meter.write(msg)

    def set_RBW(self, RBW_nm):
        msg = ':SENS:BWID:RES %snm' % (str(RBW_nm))
        self.meter.write(msg)

    def set_wavelength_range(self, wav_start_nm, wav_stop_nm):
        msg = ':SENS:WAV:STAR %snm' % (str(wav_start_nm))
        self.meter.write(msg)
        msg = ':SENS:WAV:STOP %snm' % (str(wav_stop_nm))
        self.meter.write(msg)

    def set_wavelength_center(self, wavelength_center_nm):
        self.wavelength_center_set = wavelength_center_nm
        msg = ':SENS:WAV:CENT %snm' % (str(wavelength_center_nm))
        self.meter.write(msg)

    def set_wavelength_span(self, wavelength_span_nm):
        self.wavelength_span_set = wavelength_span_nm
        msg = ':SENS:WAV:SPAN %snm' % (str(wavelength_span_nm))
        self.meter.write(msg)

    def get_trace(self, plot_bool=False):
        msg = ':INIT'  # make a sweep, single mode
        self.meter.write(msg)
        wait = 0
        while (not wait):
            self.meter.write('*OPC?')
            wait = self.meter.read()

        Trace_Lett = 'A'
        msg = ':TRACE:X? TR%s' % (Trace_Lett)
        self.meter.write(msg)
        wav_str = self.meter.read()
        wav_list = wav_str.split(',')
        wavelength_nm = np.zeros(len(wav_list))
        for kk in range(len(wav_list)):
            wavelength_nm[kk] = float(wav_list[kk]) * 1e9

        msg = ':TRACE:Y? TR%s' % (Trace_Lett)
        self.meter.write(msg)
        power_str = self.meter.read()
        power_list = power_str.split(',')
        power_dBm_pr_nm = np.zeros(len(power_list))
        for kk in range(len(power_list)):
            power_dBm_pr_nm[kk] = float(power_list[kk])  # [dBm/nm]

        # msg = ':TRACE:DELETE TR%s' % (Trace_Lett)
        # self.meter.write(msg)

        if plot_bool:
            self.plot_trace(wavelength_nm, power_dBm_pr_nm)

        return wavelength_nm, power_dBm_pr_nm

    def plot_trace(self, wavelength_nm, power_dBm_pr_nm):
        plt.figure()
        plt.plot(wavelength_nm, power_dBm_pr_nm)


    def get_max_trace(self):
        wavelength_nm, power_dBm_pr_nm = self.get_trace()
        max_index = np.argmax(power_dBm_pr_nm)
        max_wavelength_nm = wavelength_nm[max_index]
        max_power_dBm_pr_nm = power_dBm_pr_nm[max_index]
        return max_wavelength_nm, max_power_dBm_pr_nm, max_index

    def get_detector_power(self):
        wavelength_nm, power_dBm_pr_nm = self.get_trace()
        max_index = np.argmax(power_dBm_pr_nm)
        self.detector_wavelength_set = wavelength_nm[max_index]
        self.detector_power_get = power_dBm_to_W(power_dBm_pr_nm[max_index])
        return self.detector_power_get

    def get_detector_wavelength(self):
        return self.detector_wavelength_set

    def set_detector_wavelength_set(self, wavelength):
        self.wavelength_center_set = wavelength

    def set_detector_wavelength(self):
        self.set_wavelength_center(self.wavelength_center_set)

    def get_detector_power_get(self):
        return self.detector_power_get

    def get_averaging_set(self):
        return self.get_averaging()

    def get_detector_wavelength_set(self):
        return self.detector_wavelength_set

    def get_averaging(self):
        """Get the averaging"""
        return self.detector_averaging

    def set_averaging(self, sens_mode):
        print(sens_mode)
        if (sens_mode == 0):
            sens_mode_Yoko = '0'
        elif (sens_mode == 1):
            sens_mode_Yoko = '1'
        elif (sens_mode == 2):
            sens_mode_Yoko = '2'
        elif (sens_mode == 3):
            sens_mode_Yoko = '3'
        elif (sens_mode == 4):
            sens_mode_Yoko = '4'
        elif (sens_mode == 5):
            sens_mode_Yoko = '5'
        else:  # NORMAL
            sens_mode_Yoko = '6'

        msg = ':SENS:SENS %s' % (sens_mode_Yoko)
        self.meter.write(msg)

    def reset(self):
        """Reset the DMM and it's registers."""
        self.meter.write('*RST')
        self.meter.write('*CLS')

    def load_settings(self):
        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.set_detector_wavelength_set(settings_dict["wavelength"])
            self.set_averaging(settings_dict["sensitivity"])
            self.set_wavelength_span(settings_dict["wavelength_span"])

    def save_settings(self):
        dictionary = {
            "wavelength": self.get_detector_wavelength(),
            "sensitivity": self.get_averaging(),
            "wavelength_span": self.get_wavelength_span()
        }

        with open(self.settings_path, "w") as text_file:
            json.dump(dictionary, text_file)

    def get_wavelength_span(self):
        return self.wavelength_span_set

    def get_name(self):
        return "Yokogawa"

    def close(self):
        """End communication"""
        self.save_settings()
        self.meter.close()
