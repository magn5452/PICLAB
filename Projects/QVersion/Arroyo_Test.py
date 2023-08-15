import pyvisa as visa
from matplotlib import pyplot as plt

from Python_lib.Arroyo import Arroyo
from Python_lib.Arroyo_Stub import Arroyo_Stub
from Python_lib.Yokogawa import Yokogawa

resource_manager = visa.ResourceManager()
list = resource_manager.list_resources()
print(list)
laser = Arroyo(resource_manager, 'ASRL3::INSTR')

laser.set_temperature(23)
laser.set_wavelength(2321)

yoko_conf = 'GPIB0::7::INSTR' ## replace 1 with the GPIB number
yokogawa = Yokogawa(resource_manager, yoko_conf)
yokogawa.set_sensitivity('MID')
yokogawa.set_wavelength_center(laser.get_wavelength())
yokogawa.set_span_wav(10) # [nm]
yokogawa.set_RBW(0.05)

print(yokogawa.get_trace(plot_bool=True))

laser.close()





