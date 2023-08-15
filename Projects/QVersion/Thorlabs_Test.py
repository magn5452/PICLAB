import pyvisa as visa

from Python_lib.Thorlabs_PM100U import Thorlabs_PM100U

rm = visa.ResourceManager()
list = rm.list_resources()

print(list)
detector = Thorlabs_PM100U(resource_manager=rm, port=list[0])

print(detector.get_detector_wavelength())
