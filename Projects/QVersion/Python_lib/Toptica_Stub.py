import numpy as np


class Toptica_Stub:

    def __init__(self, IP_address='192.168.1.100'):
        self.power_stabilization_status = True
        self.emission_status = True
        self.power = 15
        self.wavelength = 980
        self.current = 15
        self.IP_address = IP_address

    def get_emission_status(self) -> bool:
        return self.emission_status

    def print_emission_status(self):
        if self.get_emission_status():
            print("Emission status: The Toptica stub is on")
        else:
            print("Emission status: The Toptica stub is off")

    def get_power_stabilization_status(self):
        return self.power_stabilization_status

    def set_power_stabilization_status(self, enabled=True):
        self.power_stabilization_status = enabled
        return None

    def get_power_stabilization_parameters(self):
        return None

    def set_power_stabilization_parameters(self, p, i, d=0, gain=1):
        return None

    def get_power(self):
        """
        Return the power [mW] of the laser
        @rtype: float
        @return: power of the laser [mW]
        """
        return self.power

    def set_power(self, power_mW: float):
        """
        Set the power [mW] of the laser
        @param power_mW: power of the laser [mW]
        @return: None
        """
        self.power = power_mW
        return None

    def get_wavelength(self):
        """
        Returns the wavelength [nm] of the laser
        @rtype: float
        @return: wavelength [nm]
        """
        return self.wavelength

    def set_wavelength(self, wavelength_nm: float):
        """
        Set wavelength [nm] of the laser
        @param wavelength_nm: wavelength of the laser [nm]
        @return: None
        """
        """Set the wavelength in nm"""
        if wavelength_nm < 910 or wavelength_nm > 980:
            print('ERROR in Toptica->SetWavelength: wavelength range exceeded')
        else:
            self.wavelength = float(wavelength_nm)

    def get_current(self):
        """
        Return the current [mA] of the laser
        @rtype: float
        @return: power of the laser [mA]
        """
        return self.current

    def set_current(self, current_mA: float):
        """
        Set the current [mA] of the laser
        @param current_mA: current of the laser [mA]
        @return: None
        """
        self.current = current_mA
        return None

    def get_min_wavelength(self):
        return 910

    def get_max_wavelength(self):
        return 980

    def get_name(self):
        """
        Set the current [mA] of the laser
        @param current_mA: current of the laser [mA]
        @return: None
        """
        return "Toptica Stubs"

    def close(self):
        """
        Closes the connection to the laser
        @return: None
        """
        return None