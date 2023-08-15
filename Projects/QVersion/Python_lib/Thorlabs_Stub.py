#!/usr/bin/env python
import numpy as np


class Thorlabs_Stub:

    def __init__(self):
        self.units = 'dBm'
        self.config_power = 0.015
        self.wavelength = 980
        self.averaging = 1
        self.info = 'info'

    def zero(self):
        return None

    def get_averaging(self):
        """Get the averaging"""
        return self.averaging

    def set_averaging(self, N_avg):
        """Get the averaging"""
        self.averaging = N_avg

    def set_config_power(self):
        """Set the wavelength in nm"""
        self.config_power = 0.015

    def set_auto_range(self, auto_range='ON'):
        """Set the wavelength in nm"""

    def set_beam(self, beam='MIN'):
        """Set the wavelength in nm"""

    def set_wavelength(self, wavelength_nm):
        """Set the wavelength in nm"""
        self.wavelength = float(wavelength_nm)

    def set_units(self, unit_str):
        """Set the units to W or dBm"""
        self.units = unit_str

    def get_power(self):
        """Get a power measurement"""
        return self.config_power + 0.001*np.random.normal(0, 1, 1)[0]

    def reset(self):
        """Reset"""

    def get_name(self):
        return "Stubs"

    def close(self):
        """End communication"""
