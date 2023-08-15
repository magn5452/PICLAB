from abc import ABCMeta, abstractmethod


class Detector:
    @abstractmethod
    def set_wavelength_detector(self):
        pass

    @abstractmethod
    def get_wavelength_detector(self):
        pass

    @abstractmethod
    def get_power_detector(self):
        pass
