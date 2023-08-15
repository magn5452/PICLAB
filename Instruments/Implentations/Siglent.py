import json


class Siglent:  # SDG6022X

    def __init__(self, resource_manager, settings_path, resource):
        self.settings_path = settings_path
        self.resource_manager = resource_manager
        self.siglent = resource_manager.open_resource(resource)
        self.voltage_set = None
        self.mode_set = None
        self.is_alive()

        self.channel = "C1"

        self.set_voltage(0)
        self.set_mode("DC")

        self.turn_on()

    def is_alive(self):
        is_alive = self.siglent.write('*IDN?')
        if is_alive != 0:
            print("Siglent is alive")

    def toggle(self):
        pass

    def get_mode(self):
        return self.get("WVTP")

    def get(self, type="WVTP"):
        string = self.siglent.query(self.channel + ":" + "BSWV?")
        index_start = string.rfind(type) + len(type) + 1
        index_end = string.find(",", index_start)
        res = string[index_start: index_end]
        return res

    def set_mode(self, mode): # {SINE, SQUARE, RAMP, PULSE, NOISE, ARB, DC, PRBS}
        self.mode_set = mode
        self.siglent.write(self.channel + ":" + "BSWV WVTP," + str(mode))

    def set_voltage(self, voltage):
        self.voltage_set = voltage
        self.siglent.write(self.channel + ":" + "BSWV OFST," + str(voltage) + "V")

    def get_voltage_set(self):
        return self.voltage_set

    def get_voltage(self):
        return float(self.get("OFST")[0:-1])

    def load_settings(self):
        with open(self.settings_path, "r") as text_file:
            settings_dict = json.load(text_file)
            # self.set_wavelength_nm = settings_dict["wavelength"]

    def save_settings(self):
        pass

    def close(self):
        """End communication"""
        self.save_settings()
        self.turn_off()

    def turn_on(self):
        # Enable the output
        self.siglent.write("OUTPUT ON")

    def turn_off(self):
        # Enable the output
        self.siglent.write("OUTPUT OFF")

    def get_wave_data(self):
        """get wave from the devide"""
        self.siglent.write("WVDT? user,wave1")  # "X" series (SDG1000X/SDG2000X/SDG6000X/X-E)

        data = self.siglent.read()
        data_pos = data.find("WAVEDATA,") + len("WAVEDATA,")
        wave_data = data[data_pos:]
        print(wave_data)
