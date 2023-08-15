import tkinter as tk
from tkinter import ttk

from GUI.Functions.functions import get_float_from_string


class Sweep_Voltage_Menu_Window:

    def __init__(self, instrument_controller, gui_controller):
        self.update_bool = None
        self.label = None
        self.instrument_controller = instrument_controller
        self.gui_controller = gui_controller
        self.button_6 = None
        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.button_5 = None
        self.button_6 = None
        self.entry_1 = None
        self.entry_2 = None
        self.entry_3 = None
        self.entry_4 = None
        self.frame = None

    def open(self, parent_frame):
        if self.frame is None:
            self.update_bool = True
            self.frame = tk.Frame(parent_frame, bg="white")

            msg = self.get_message()
            self.label = ttk.Label(self.frame, text=msg, font="Arial", background="white")
            self.label.pack(side="top", fill="x", pady=10)

            self.button_1 = ttk.Button(self.frame)
            self.button_1["text"] = "Run Sweep"
            self.button_1["command"] = lambda: self.run_sweep_button()
            self.button_1.pack(fill='both', expand=True)

            self.entry_4 = ttk.Entry(self.frame)
            self.button_6 = ttk.Button(self.frame)
            self.button_6["text"] = "Set Voltage"
            self.button_6["command"] = lambda: self.set_voltage_button()
            self.button_6.pack(fill='both', expand=True)
            self.entry_4.pack(fill='both', expand=True)
            self.entry_4.insert(0, "Set Voltage...")
            self.entry_4.bind("<FocusIn>", lambda event: self.entry_4.delete(0, "end"))

            self.entry_2 = ttk.Entry(self.frame)
            self.button_4 = ttk.Button(self.frame)
            self.button_4["text"] = "Set Min Voltage"
            self.button_4["command"] = lambda: self.set_min_voltage_button()
            self.button_4.pack(fill='both', expand=True)
            self.entry_2.pack(fill='both', expand=True)
            self.entry_2.insert(0, "Set Minimum Voltage...")
            self.entry_2.bind("<FocusIn>", lambda event: self.entry_2.delete(0, "end"))

            self.entry_3 = ttk.Entry(self.frame)
            self.button_5 = ttk.Button(self.frame)
            self.button_5["text"] = "Set Max Voltage"
            self.button_5["command"] = lambda: self.set_max_voltage_button()
            self.button_5.pack(fill='both', expand=True)
            self.entry_3.pack(fill='both', expand=True)
            self.entry_3.insert(0, "Set Max Voltage...")
            self.entry_3.bind("<FocusIn>", lambda event: self.entry_3.delete(0, "end"))

            self.entry_1 = ttk.Entry(self.frame)
            self.button_3 = ttk.Button(self.frame)
            self.button_3["text"] = "Set Sweep Voltage"
            self.button_3["command"] = lambda: self.set_sweep_voltage_button()
            self.button_3.pack(fill='both', expand=True)
            self.entry_1.pack(fill='both', expand=True)
            self.entry_1.insert(0, "Set Sweep Voltage...")
            self.entry_1.bind("<FocusIn>", lambda event: self.entry_1.delete(0, "end"))

            self.button_2 = ttk.Button(self.frame)
            self.button_2["text"] = "Toggle Save"
            self.button_2["command"] = lambda: self.toggle_save_bool_button()
            self.button_2.pack(fill='both', expand=True)

            self.entry_4 = ttk.Entry(self.frame)
            self.button_4 = ttk.Button(self.frame)
            self.button_4["text"] = "Set Save Path"
            self.button_4["command"] = lambda: self.set_save_path_button()
            self.button_4.pack(fill='both', expand=True)
            sweep_voltage_save_path = self.gui_controller.get_voltage_sweep_save_path()
            self.entry_4.insert(0, sweep_voltage_save_path)
            self.entry_4.pack(fill='both', expand=True)

            return self.frame

    def set_save_path_button(self):
        save_path = self.entry_4.get()
        self.gui_controller.set_wavelength_sweep_save_path(save_path)

    def get_message(self):
        if len(self.instrument_controller.get_waveform_generator_list()) > 0:
            waveform_generator = self.instrument_controller.get_waveform_generator_list()[0]
            return "Save Bool: " + str(self.gui_controller.get_save_bool()) + "\n" + \
                "Voltage: " + str(waveform_generator.get_voltage()) + " V \n" + \
                "Min voltage: " + str(self.instrument_controller.get_min_voltage()) + " V \n" + \
                "Max voltage: " + str(self.instrument_controller.get_max_voltage()) + " V \n" + \
                "Sweep voltage: " + str(self.instrument_controller.get_sweep_voltage()) + " V "
        else:
            return ""

    def run_sweep_button(self):
        self.gui_controller.run_sweep_voltage()
        self.update_window()

    def set_voltage_button(self):
        waveform_generator_list = self.instrument_controller.get_waveform_generator_list()
        for waveform_generator in waveform_generator_list:
            voltage = get_float_from_string(self.entry_4.get(), waveform_generator.get_voltage())
            waveform_generator.set_voltage(voltage)
        self.update_window()

    def set_sweep_voltage_button(self):
        sweep_voltage = get_float_from_string(self.entry_1.get(), self.instrument_controller.get_sweep_voltage())
        self.instrument_controller.set_sweep_voltage(sweep_voltage)
        self.update_window()

    def set_min_voltage_button(self):
        min_voltage = get_float_from_string(self.entry_2.get(), self.instrument_controller.get_min_voltage())
        self.instrument_controller.set_min_voltage(min_voltage)
        self.update_window()

    def set_max_voltage_button(self):
        max_voltage = get_float_from_string(self.entry_3.get(), self.instrument_controller.get_max_voltage())
        self.instrument_controller.set_max_voltage(max_voltage)
        self.update_window()

    def toggle_save_bool_button(self):
        self.gui_controller.toggle_save_bool()
        self.update_window()

    def get_toggle_save_button_label(self):
        return self.gui_controller.save_bool

    def update_window(self):
        if self.update_bool:
            self.label.config(text=self.get_message())

    def close(self):
        self.update_bool = False
        if self.frame is not None:
            self.frame.destroy()
