from pyvisa import constants
from scipy.optimize import fsolve


class Arroyo_Stub:  # developer: Magnus Linnet Madsen
    def __init__(self):
        self.wavelength_model = lambda current, temperature: self.model_poly21(current, temperature)
        self.temperature_set = 25
        self.current_set = 150
        self.wavelength_set = self.wavelength_model(self.current_set, self.temperature_set)

    def query(self, command):
        pass

    def ask(self, command, print_bool=False):
        pass

    def set_maximum_current(self, I):
        pass

    def reset(self):
        pass

    def turn_on_laser(self):
        pass

    def turn_off_laser(self):
        pass

    def turn_on_TEC(self):
        pass

    def turn_off_TEC(self):
        pass

    def get_wavelength(self):
        pass

    def set_wavelength(self, wavelength):
        """
        Set the wavelength of the laser based on calibration
        @param wavelength: Wavelenght in nm within 2318 and 2327
        """
        function = lambda current: self.wavelength_model(current, self.temperature_set) - wavelength
        current_guess = self.current_set
        current_solution = fsolve(function, current_guess)
        print(current_solution)

    def set_current(self, current):
        pass

    def print_emission_status(self):
        if True:
            print("Emission status: The laser is on and emitting´light")
        else:
            print("Emission status: The laser is off and not emitting any light")

    def close(self):
        """End communication"""
        pass

    def model_poly21(self, I, T):
        """
        Poly21 fit model of the wavelength of the central peak of Arroyo laser measured on the on Yokogawa

        @param I: Current [mA]
        @param T: Temperature [C]
        @return: Wavelength of Arroyo Laser [nm]
        """
        p00 = 2313.53210077781
        p10 = 0.021149148546667
        p01 = 0.204626113816945
        p20 = 1.026188229451297e-04
        p11 = -4.667933943058038e-05
        return p00 + p10 * I + p01 * T + p20 * I ** 2 + p11 * I * T

    def model_poly22(self, I, T):
        """
        Poly22 fit model of the wavelength of the central peak of Arroyo laser measured on the on Yokogawa

        @param I: Current [mA]
        @param T: Temperature [C]
        @return: Wavelength of Arroyo Laser [nm]
        """
        p00 = 2.313822846391841e+03
        p10 = 0.021149148546667
        p01 = 0.178468219081220
        p20 = 1.026188229451297e-04
        p11 = -4.667933943058005e-05
        p02 = 5.833333333084118e-04
        return p00 + p10 * I + p01 * T + p20 * I ** 2 + p11 * I * T + p02 * T ** 2


