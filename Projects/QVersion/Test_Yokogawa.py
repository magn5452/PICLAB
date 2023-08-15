## Yokogawa
from Python_lib.Yokogawa import Yokogawa
import pyvisa as visa

resource_manager = visa.ResourceManager()
resource_list = resource_manager.list_resources()
print(resource_list)

yoko_conf = "GPIB1::7::INSTR"
yoko = Yokogawa(resource_manager, yoko_conf)
wavelength_nm, power_dBm_pr_nm = yoko.get_trace(False)
print(power_dBm_pr_nm)
print(wavelength_nm)
