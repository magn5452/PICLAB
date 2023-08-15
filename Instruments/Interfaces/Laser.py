from abc import ABCMeta, abstractmethod


class Laser:

    @abstractmethod
    def set_power_laser(self, power_mW: float):
        """
        This method is an absract method to be implemented that can set the power of a laser.
        :param power_mW: The power to be set of the laser in units of mW
        """
        pass

    @abstractmethod
    def set_wavelength_laser(self, wavelength_nm: float):
        """
        This method is an absract method to be implemented that can set the wavelength of a laser.
        :param wavelength_nm: The wavelength to be set of the laser in units of nW
        """
        pass

    @abstractmethod
    def get_power_laser(self) -> float:
        """
        This method is an absract method to be implemented that can get the current power of a laser.
        :return the current power of the laser in mW
        """
        pass

    @abstractmethod
    def get_wavelength_laser(self) -> float:
        """
        This method is an absract method to be implemented that can get the current wavelength of a laser.
        :return the current wavelength of the laser in nm
        """
        pass

    @abstractmethod
    def get_power_laser_set(self) -> float:
        """
        This method is an absract method to be implemented that can get the wavelength of a laser that was previously set.
        :return the wavelength of the laser in nm that was previously set in mW
        """
        pass

    @abstractmethod
    def get_wavelength_laser_set(self) -> float:
        """
        This method is an absract method to be implemented that can get the power of a laser that was previously set.
        :return the power of the laser in mW that was previously set in mW
        """
        pass

    @abstractmethod
    def set_laser_on(self):
        """
        This method is an absract method to be implemented that can turn on a laser
        """
        pass

    @abstractmethod
    def set_laser_off(self):
        """
        This method is an absract method to be implemented that can turn off a laser
        """
        pass

    @abstractmethod
    def get_min_wavelength_laser(self) -> float:
        """
        This method is an absract method to be implemented that returns the minimum wavelength of the laser
        :return The minimum wavelength of the laser in nm
        """
        pass

    @abstractmethod
    def get_max_wavelength_laser(self) -> float:
        """
        This method is an absract method to be implemented that returns the maximum wavelength of the laser
        :return The maximum wavelength of the laser in nm
        """
        pass

    @abstractmethod
    def get_min_power_laser(self) -> float:
        """
        This method is an absract method to be implemented that returns the minimum power of the laser
        :return The minimum power of the laser in mW
        """
        pass

    @abstractmethod
    def get_max_power_laser(self) -> float:
        """
        This method is an absract method to be implemented that returns the maximum power of the laser
        :return The maximum power of the laser in mW
        """
        pass