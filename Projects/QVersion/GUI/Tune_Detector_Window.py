import tkinter as tk
from tkinter import ttk
from GUI.Functions.functions import *


class Tune_Detector_Window:
    def __init__(self, instrument_controller):
        self.update_bool = None
        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.entry_1 = None
        self.instrument_controller = instrument_controller
        self.detector_list = None
        self.frame = None
        self.label = None
        self.info_label = None

    def open(self, parent_frame):
        if self.frame is None:
            self.update_bool = True
            self.frame = tk.Frame(parent_frame, bg="white")

            msg = self.get_message()
            self.label = ttk.Label(self.frame, text=msg, font="Arial",  background="white")
            self.label.pack(side="top", fill='both', expand=True, pady=10)

            # self.button_2 = ttk.Button(self.window)
            # self.button_2["text"] = "Previous Detector"
            # self.button_2["command"] = lambda: self.previous_detector_button()
            # self.button_2.pack()

            # self.button_3 = ttk.Button(self.window)
            # self.button_3["text"] = "Update Label"
            # self.button_3["command"] = lambda: self.update_button()
            # self.button_3.pack()

            self.entry_1 = ttk.Entry(self.frame)
            self.button_4 = ttk.Button(self.frame)
            self.button_4["text"] = "Set Wavelength [nm]"
            self.button_4["command"] = lambda: self.set_wavelength_button()
            self.button_4.pack(fill='both', expand=True)
            self.entry_1.insert(0, "Set Wavelength [nm]...")
            self.entry_1.bind("<FocusIn>", lambda event: self.entry_1.delete(0, "end"))
            self.entry_1.pack(fill='both', expand=True)

            self.entry_2 = ttk.Entry(self.frame)
            self.button_5 = ttk.Button(self.frame)
            self.button_5["text"] = "Set Averaging"
            self.button_5["command"] = lambda: self.set_averaging_button()
            self.button_5.pack(fill='both', expand=True)
            self.entry_2.insert(0, "Set Averaging...")
            self.entry_2.bind("<FocusIn>", lambda event: self.entry_2.delete(0, "end"))
            self.entry_2.pack(fill='both', expand=True)

            self.button_1 = ttk.Button(self.frame)
            self.button_1["text"] = "Next Detector"
            self.button_1["command"] = lambda: self.next_detector_button()
            self.button_1.pack(fill='both', expand=True)

            info = self.get_info()
            self.info_label = ttk.Label(self.frame, text=info, font="Arial", background="white")
            self.info_label.pack(side="top", fill="x", pady=10)
            return self.frame

    def next_detector_button(self):
        print("next")
        self.instrument_controller.next_detector()

    def set_wavelength_button(self):
        self.instrument_controller.get_target_detector().set_detector_wavelength_set(
            get_float_from_string(self.entry_1.get(),
                                  self.instrument_controller.get_target_detector().get_detector_wavelength_set()))

    def set_averaging_button(self):
        self.instrument_controller.get_target_detector().set_averaging(get_float_from_string(self.entry_2.get(),
                                                                                             self.instrument_controller.get_target_detector().get_averaging()))

    def previous_detector_button(self):
        self.instrument_controller.previous_detector()

    def get_message(self):
        if self.instrument_controller.instrument_connected_bool:
            detector = self.instrument_controller.get_target_detector()
            return self.get_detector_info(detector) + "\n"
        else:
            return ""

    def get_info(self):
        info_string = ""
        for detector in self.instrument_controller.get_detector_list():
            info_string += self.get_detector_info(detector) + "\n"
        return info_string


    def get_detector_info(self, detector):
        if self.instrument_controller.instrument_connected_bool:
            power_W = detector.get_detector_power_get()
            info_string = detector.get_name() + ": " + str(np.round(power_W * 1000, 6)) + " mW, " + str(
                np.round(power_W_to_dBm(power_W), 1)) + " dBm, " + str(np.round(detector.get_detector_wavelength_set(),6)) + " nm, " + str(
                detector.get_averaging_set())
            return info_string
        else:
            return ""


    def update_window(self):
        if self.update_bool:
            self.label.config(text=self.get_message())
            self.info_label.config(text=self.get_info())

    def close(self):
        self.update_bool = False
        if self.frame is not None:
            self.frame.destroy()
