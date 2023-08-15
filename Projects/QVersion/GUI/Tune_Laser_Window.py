import tkinter as tk
from tkinter import ttk

from GUI.Functions.functions import *


class Tune_Laser_Window:
    def __init__(self, instrument_controller):
        self.instrument_controller = instrument_controller
        self.tune_step_wavelength = 1.0
        self.tune_step_power = 1.0
        self.frame = None

        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.button_5 = None
        self.button_6 = None
        self.button_7 = None
        self.button_8 = None
        self.button_9 = None
        self.button_10 = None
        self.entry_1 = None
        self.entry_2 = None
        self.entry_3 = None
        self.entry_4 = None

        self.label = None
        self.info_label = None
        self.close_bool = None

    def open(self, parent_frame):
        if self.frame is None:
            self.close_bool = False

            self.frame = tk.Frame(parent_frame, bg="white")

            msg = self.get_message()
            self.label = ttk.Label(self.frame, text=msg, font="Arial", background="white")
            self.label.pack(side="top", fill="x", pady=10)

            info_string = self.get_info()
            self.info_label = ttk.Label(self.frame, text=info_string, font="Arial", background="white")
            self.info_label.pack(side="top", fill='both', pady=10)
            self.info_label.pack(side="bottom", fill='both', pady=10)

            self.button_1 = ttk.Button(self.frame)
            self.button_1["text"] = "+" + str(self.tune_step_wavelength) + " nm"
            self.button_1["command"] = lambda: self.button1()
            self.button_1.pack(side='right', fill='both')

            self.button_2 = ttk.Button(self.frame)
            self.button_2["text"] = "-" + str(self.tune_step_wavelength) + " nm"
            self.button_2["command"] = lambda: self.button2()
            self.button_2.pack(side='left', fill='both')

            self.button_5 = ttk.Button(self.frame)
            self.button_5["text"] = "+" + str(self.tune_step_power) + " mW"
            self.button_5["command"] = lambda: self.button5()
            self.button_5.pack(side='right', fill='both')

            self.button_6 = ttk.Button(self.frame)
            self.button_6["text"] = "-" + str(self.tune_step_power) + " mW"
            self.button_6["command"] = lambda: self.button6()
            self.button_6.pack(side='left', fill='both')

            self.entry_1 = ttk.Entry(self.frame)
            self.button_3 = ttk.Button(self.frame)
            self.button_3["text"] = "Go to [nm]"
            self.button_3["command"] = lambda: self.button3()
            self.button_3.pack(fill='both')
            self.entry_1.insert(0, "Go to [nm]...")
            self.entry_1.bind("<FocusIn>", lambda event: self.entry_1.delete(0, "end"))
            self.entry_1.pack(fill='both')

            self.entry_2 = ttk.Entry(self.frame)
            self.button_4 = ttk.Button(self.frame)
            self.button_4["text"] = "Set step [nm]"
            self.button_4["command"] = lambda: self.button4()
            self.button_4.pack(fill='both')
            self.entry_2.insert(0, "Set step [nm]...")
            self.entry_2.bind("<FocusIn>", lambda event: self.entry_2.delete(0, "end"))
            self.entry_2.pack(fill='both')

            self.entry_3 = ttk.Entry(self.frame)
            self.button_7 = ttk.Button(self.frame)
            self.button_7["text"] = "Go to [mW]"
            self.button_7["command"] = lambda: self.button7()
            self.button_7.pack(fill='both')
            self.entry_3.insert(0, "Go to [mW]...")
            self.entry_3.bind("<FocusIn>", lambda event: self.entry_3.delete(0, "end"))
            self.entry_3.pack(fill='both')

            self.entry_4 = ttk.Entry(self.frame)
            self.button_8 = ttk.Button(self.frame)
            self.button_8["text"] = "Set step [mW]"
            self.button_8["command"] = lambda: self.button8()
            self.button_8.pack(fill='both')
            self.entry_4.insert(0, "Set set [mW]...")
            self.entry_4.bind("<FocusIn>", lambda event: self.entry_4.delete(0, "end"))
            self.entry_4.pack(fill='both')

            self.button_9 = ttk.Button(self.frame)
            self.button_9["text"] = "Next laser"
            self.button_9["command"] = lambda: self.next_laser()
            self.button_9.pack(fill='both')

            self.button_9 = ttk.Button(self.frame)
            self.button_9["text"] = "On/Off"
            self.button_9["command"] = lambda: self.on_off_button()
            self.button_9.pack(fill='both')

            return self.frame

    def on_off_button(self):
        self.instrument_controller.get_target_laser().toggle_laser()

    def get_info(self):
        if self.instrument_controller.instrument_connected_bool:
            info_string = ""
            for laser in self.instrument_controller.get_laser_list():
                info_string += self.get_info_string(laser) + "\n"
            return info_string
        else:
            return ""

    def get_info_string(self, laser):
        if self.instrument_controller.instrument_connected_bool:
            info_string = ""
            if laser.get_name() == "Arroyo laser":
                info_string = laser.get_name() + ": %0.2f nm" % (
                    laser.get_wavelength_set()) + ", %0.2f mA" % (laser.get_current()) + ", %0.2f C" % (
                    laser.get_temperature()) + ", %0.2f V" % (laser.get_voltage())
                return info_string
            else:
                info_string = laser.get_name() + ": %0.2f nm" % (
                    laser.get_wavelength_set()) + ", %0.2f mW" % (
                               laser.get_power_set()) + "\n"
                return info_string
        else:
            return ""

    def get_message(self):
        if self.instrument_controller.instrument_connected_bool:
            laser = self.instrument_controller.get_target_laser()
            return self.get_info_string(laser)
        else:
            return "Instruments Not Connected"

    def set_wavelength(self, wavelength):
        laser = self.instrument_controller.get_target_laser()
        laser.set_wavelength(wavelength)

    def button1(self):
        if self.instrument_controller.instrument_connected_bool:
            laser = self.instrument_controller.get_target_laser()
            current_wavelength = laser.get_wavelength_set()
            update_wavelength = current_wavelength + self.tune_step_wavelength
            self.set_wavelength(update_wavelength)
        else:
            pass

    def button2(self):
        if self.instrument_controller.instrument_connected_bool:
            laser = self.instrument_controller.get_target_laser()
            current_wavelength = laser.get_wavelength_set()
            update_wavelength = current_wavelength - self.tune_step_wavelength
            self.set_wavelength(update_wavelength)
        else:
            pass

    def button3(self):
        if self.instrument_controller.instrument_connected_bool:
            laser = self.instrument_controller.get_target_laser()
            self.set_wavelength(get_float_from_string(self.entry_1.get(), laser.get_wavelength_set()))
        else:
            pass

    def button5(self):
        if self.instrument_controller.instrument_connected_bool:
            laser = self.instrument_controller.get_target_laser()
            current_power = laser.get_power_set()
            update_power = current_power + self.tune_step_power
            laser.set_power(update_power)
        else:
            pass

    def button6(self):
        if self.instrument_controller.instrument_connected_bool:
            laser = self.instrument_controller.get_target_laser()
            current_power = laser.get_power_set()
            update_power = current_power - self.tune_step_power
            laser.set_power(update_power)
        else:
            pass

    def button7(self):
        if self.instrument_controller.instrument_connected_bool:
            laser = self.instrument_controller.get_target_laser()
            laser.set_power(get_float_from_string(self.entry_3.get(), laser.get_power_set()))
        else:
            pass

    def set_step_power(self, step):
        self.tune_step_power = float(step)

    def set_step_wavelength(self, step):
        self.tune_step_wavelength = float(step)

    def button4(self):
        if self.instrument_controller.instrument_connected_bool:
            self.set_step_wavelength(get_float_from_string(self.entry_2.get(), self.tune_step_wavelength))
        else:
            pass

    def button8(self):
        if self.instrument_controller.instrument_connected_bool:
            self.set_step_power(get_float_from_string(self.entry_4.get(), self.tune_step_power))
        else:
            pass

    def update_window(self):
        if not self.close_bool:
            self.button_1.configure(text="+" + str(self.tune_step_wavelength) + " nm")
            self.button_2.configure(text="-" + str(self.tune_step_wavelength) + " nm")
            self.button_5.configure(text="+" + str(self.tune_step_power) + " mW")
            self.button_6.configure(text="-" + str(self.tune_step_power) + " mW")
            msg = self.get_message()
            info_string = self.get_info()
            self.label.config(text=msg)
            self.info_label.config(text=info_string)

    def next_laser(self):
        self.instrument_controller.next_laser()

    def close(self):
        self.close_bool = True
        if self.frame is not None:
            self.frame.destroy()
            self.frame = None


def get_float_from_string(str, original_step):
    if str == '':
        return original_step
    else:
        return float(str)
