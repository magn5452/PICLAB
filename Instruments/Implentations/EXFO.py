## Authour Emil Z. Ulsig @2023
# EXFO T100S-HP
import json

from Instruments.Interfaces.Laser import Laser


class EXFO(Laser):

    def __init__(self, resource_manager, settings_path, exfo_conf='GPIB0::10::INSTR'):

        self.settings_path = settings_path
        self.exfo = resource_manager.open_resource(exfo_conf)
        self.exfo.timeout = 5 * 60e3
        self.exfo.write('INIT')
        self.reset()
        wait = 0
        while (not wait):
            self.exfo.write('*OPC?')
            wait = self.exfo.read()
        self.exfo.write('*IDN?')
        self.info = self.exfo.read()
        wait = 0
        while (not wait):
            self.exfo.write('*OPC?')
            wait = self.exfo.read()

        self.is_alive()

        exfo_sweep_speed = 10  # [nm/s]
        self.set_power_unit_mW()
        self.automatic_power_control()
        self.set_sweep_speed(exfo_sweep_speed)
        self.detector_wavelength_set = self.get_detector_wavelength()
        self.detector_power_get = self.get_detector_power()
        self.power_on_off = None
        self.power_set = None
        self.wavelength_set = None
        self.onoff = True

        self.load_settings()

    def is_alive(self):
        is_alive = self.exfo.write('*IDN?')
        if is_alive != 0:
            print("EXFO is alive")

    def set_power_unit_mW(self):
        msg = 'MW'
        self.exfo.write(msg)
        return

    def set_power_unit_dBm(self):
        msg = 'DBM'
        self.exfo.write(msg)
        return

    def set_power_laser(self, power_mW):  # [mW]
        self.power_set = power_mW
        msg = 'P=%s' % (str(power_mW))
        self.exfo.write(msg)

    def get_set_power_mW(self):
        return self.power_on_off

    def get_power(self):  # [mW]
        msg = 'P?'
        self.exfo.write(msg)
        try:
            res = float(self.exfo.read()[2:])
        except:
            res = 0
        return res

    def set_detector_wavelength_set(self, wavelength):
        self.detector_wavelength_set = wavelength

    def set_detector_wavelength(self):
        pass

    def get_detector_power_get(self):
        return self.detector_power_get

    def get_detector_power(self):  # [W]
        self.detector_power_get = self.get_power() / 1000
        return self.detector_power_get

    def get_detector_wavelength_set(self):
        return self.detector_wavelength_set

    def get_detector_wavelength(self):
        wavelength = self.get_wavelength()
        self.detector_wavelength_set = wavelength
        return wavelength

    def get_averaging_set(self):
        return 1

    def set_wavelength_laser(self, wavelength):  # [nm]
        self.wavelength_set = wavelength
        msg = 'L=%s' % (str(wavelength))
        self.exfo.write(msg)

    def get_power_set(self):
        return self.power_set

    def get_wavelength_set(self):
        return self.wavelength_set

    def get_wavelength_laser(self):
        msg = 'L?'
        self.exfo.write(msg)
        res = self.exfo.read()[2:]
        # print(res[:-2])
        return float(res[:-2])

    def set_sweep_speed(self, nm):  # [nm/s]
        sweep_speeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                        17, 18, 20, 22, 25, 29, 33, 40, 50, 67, 100]
        if nm in sweep_speeds:
            msg = 'MOTOR_SPEED=%s' % (str(nm))
            self.exfo.write(msg)
        else:
            print('Sweep speed requires to be among the intervals [nm/s]:')
            print(str(sweep_speeds))
        return

    def get_sweep_speed(self):
        msg = 'MOTOR_SPEED?'
        self.exfo.write(msg)
        return self.exfo.read()

    def set_finescan(self, wl_change):  # Change in wavelength [pm]
        msg = 'FSCL=%s' % (str(wl_change))
        self.exfo.write(msg)
        return

    def active_cavity_control_on(self):
        msg = 'ACTCTRLON'
        self.exfo.write(msg)
        return

    def active_cavity_control_off(self):
        msg = 'ACTCTRLOFF'
        self.exfo.write(msg)
        return

    def automatic_power_control(self):
        msg = 'APCON'
        self.exfo.write(msg)
        return

    def constant_current(self):
        msg = 'APCOFF'
        self.exfo.write(msg)
        return

    def set_laser_on(self):
        msg = 'ENABLE'
        self.exfo.write(msg)
        return 'Laser is emitting'

    def set_laser_off(self):
        msg = 'DISABLE'
        self.exfo.write(msg)
        return 'Laser is off'

    def toggle_laser(self):
        if self.onoff:
            self.power_on_off = self.power_set
            self.power_set = 0
            self.onoff = not self.onoff
            self.laser_off()
        else:
            self.laser_on()
            self.power_set = self.power_on_off
            self.set_power(self.power_on_off)
            self.onoff = not self.onoff

    def get_name(self):
        return "EXFO laser"

    def reset(self):
        self.exfo.write('*RST')  # reset laser
        return

    def load_settings(self):
        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            self.wavelength_set = settings_dict["wavelength"]
            self.power_on_off = settings_dict["power"]
            self.set_wavelength(self.wavelength_set)
            self.set_power(self.power_on_off)

    def save_settings(self):
        dictionary = {
            "wavelength": self.wavelength_set,
            "power": self.power_on_off
        }

        with open(self.settings_path, "w") as text_file:
            json.dump(dictionary, text_file)

    def close(self):
        """End communication"""
        self.save_settings()
        try:
            self.laser_off()
            self.exfo.close()
        except:
            print("EXFO already closed")

    def get_min_wavelength(self):
        return 1500

    def get_max_wavelength(self):
        return 1630

    def get_min_power(self):
        return 0.2

    def get_max_power(self):
        return 20
