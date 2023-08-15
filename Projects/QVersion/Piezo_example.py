import pyvisa as visa

from Python_lib.Piezo_Controller import Piezo_Controller_Visa

settings_path = r"C:\Users\shd-PhotonicLab\Documents\Python Scripts\Qversion_exp\Settings\piezo_controller_settings.txt"

resource_manager = visa.ResourceManager()

piezo_controller = Piezo_Controller_Visa(resource_manager, settings_path, 'ASRL4::INSTR')
