import tkinter as tk
from tkinter import ttk

from GUI.Functions.functions import *


class Tune_Piezo_Window:
    def __init__(self, instrument_controller, gui_controller):
        self.right_frame = None
        self.middle_frame = None
        self.left_frame = None
        self.tune_step_voltage = 1
        self.gui_controller = gui_controller
        self.update_bool = None

        self.button_down_x = None
        self.button_down_y = None
        self.button_down_z = None

        self.button_up_x = None
        self.button_up_y = None
        self.button_up_z = None

        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_4 = None
        self.button_5 = None
        self.button_6 = None
        self.entry_1 = None
        self.instrument_controller = instrument_controller
        self.frame = None
        self.label = None
        self.info_label = None

    def open(self, parent_frame):
        if self.frame is None:
            self.update_bool = True
            self.frame = tk.Frame(parent_frame, bg="white")

            msg = self.get_message()
            self.label = ttk.Label(self.frame, text=msg, font="Arial", background="white")
            self.label.pack(side="top", fill="x", pady=10)

            self.left_frame = tk.Frame(self.frame, bg="white")
            self.left_frame.pack(side="left", fill="both", expand=True)

            self.right_frame = tk.Frame(self.frame, bg="white")
            self.right_frame.pack(side="right", fill="both", expand=True)

            self.middle_frame = tk.Frame(self.frame, bg="white")
            self.middle_frame.pack(fill="both", expand=True)

            self.button_down_x = ttk.Button(self.left_frame)
            self.button_down_x["text"] = "X: -" + str(self.tune_step_voltage) + " V"
            self.button_down_x["command"] = lambda: self.button_down_x_command()
            self.button_down_x.pack(fill='both', expand=True)
            self.button_down_y = ttk.Button(self.left_frame)
            self.button_down_y["text"] = "Y: -" + str(self.tune_step_voltage) + " V"
            self.button_down_y["command"] = lambda: self.button_down_y_command()
            self.button_down_y.pack(fill='both', expand=True)
            self.button_down_z = ttk.Button(self.left_frame)
            self.button_down_z["text"] = "Z: -" + str(self.tune_step_voltage) + " V"
            self.button_down_z["command"] = lambda: self.button_down_z_command()
            self.button_down_z.pack(fill='both', expand=True)

            self.button_up_x = ttk.Button(self.right_frame)
            self.button_up_x["text"] = "X: +" + str(self.tune_step_voltage) + " V"
            self.button_up_x["command"] = lambda: self.button_up_x_command()
            self.button_up_x.pack(fill='both', expand=True)
            self.button_up_y = ttk.Button(self.right_frame)
            self.button_up_y["text"] = "Y: +" + str(self.tune_step_voltage) + " V"
            self.button_up_y["command"] = lambda: self.button_up_y_command()
            self.button_up_y.pack(fill='both', expand=True)
            self.button_up_z = ttk.Button(self.right_frame)
            self.button_up_z["text"] = "Z: +" + str(self.tune_step_voltage) + " V"
            self.button_up_z["command"] = lambda: self.button_up_z_command()
            self.button_up_z.pack(fill='both', expand=True)

            self.button_7 = ttk.Button(self.middle_frame)
            self.button_7["text"] = "Next Piezo"
            self.button_7["command"] = lambda: self.next_piezo_button()
            self.button_7.pack(fill='both', expand=True)

            self.entry_1 = ttk.Entry(self.middle_frame)
            self.button_1 = ttk.Button(self.middle_frame)
            self.button_1["text"] = "Set X Voltage"
            self.button_1["command"] = lambda: self.set_x_voltage_button()
            self.button_1.pack(fill='both', expand=True)
            self.entry_1.insert(0, "Set X Voltage...")
            self.entry_1.bind("<FocusIn>", lambda event: self.entry_1.delete(0, "end"))
            self.entry_1.pack(fill='both', expand=True)

            self.entry_2 = ttk.Entry(self.middle_frame)
            self.button_2 = ttk.Button(self.middle_frame)
            self.button_2["text"] = "Set Y Voltage"
            self.button_2["command"] = lambda: self.set_y_voltage_button()
            self.button_2.pack(fill='both', expand=True)
            self.entry_2.insert(0, "Set Y Voltage...")
            self.entry_2.bind("<FocusIn>", lambda event: self.entry_2.delete(0, "end"))
            self.entry_2.pack(fill='both', expand=True)

            self.entry_3 = ttk.Entry(self.middle_frame)
            self.button_3 = ttk.Button(self.middle_frame)
            self.button_3["text"] = "Set Z Voltage"
            self.button_3["command"] = lambda: self.set_z_voltage_button()
            self.button_3.pack(fill='both', expand=True)
            self.entry_3.insert(0, "Set Z Voltage...")
            self.entry_3.bind("<FocusIn>", lambda event: self.entry_3.delete(0, "end"))
            self.entry_3.pack(fill='both', expand=True)

            self.entry_4 = ttk.Entry(self.middle_frame)
            self.button_4 = ttk.Button(self.middle_frame)
            self.button_4["text"] = "Set X Resolution"
            self.button_4["command"] = lambda: self.set_x_resolution_button()
            self.button_4.pack(fill='both', expand=True)
            self.entry_4.insert(0, "Set X Resolution...")
            self.entry_4.bind("<FocusIn>", lambda event: self.entry_4.delete(0, "end"))
            self.entry_4.pack(fill='both', expand=True)

            self.entry_5 = ttk.Entry(self.middle_frame)
            self.button_5 = ttk.Button(self.middle_frame)
            self.button_5["text"] = "Set Y Resolution"
            self.button_5["command"] = lambda: self.set_y_resolution_button()
            self.button_5.pack(fill='both', expand=True)
            self.entry_5.insert(0, "Set Y Resolution...")
            self.entry_5.bind("<FocusIn>", lambda event: self.entry_5.delete(0, "end"))
            self.entry_5.pack(fill='both', expand=True)

            self.entry_6 = ttk.Entry(self.middle_frame)
            self.button_6 = ttk.Button(self.middle_frame)
            self.button_6["text"] = "Set Z Resolution"
            self.button_6["command"] = lambda: self.set_z_resolution_button()
            self.button_6.pack(fill='both', expand=True)
            self.entry_6.insert(0, "Set Z Resolution...")
            self.entry_6.bind("<FocusIn>", lambda event: self.entry_6.delete(0, "end"))
            self.entry_6.pack(fill='both', expand=True)

            return self.frame

    def get_message(self):
        return self.get_osa_info() + "\n"

    def update_window(self):
        if self.update_bool:
            self.label.config(text=self.get_message())
            if len(self.instrument_controller.get_piezo_list()) > 0:
                target_piezo = self.instrument_controller.get_target_piezo()
                self.button_down_x.configure(text="X: -" + str(target_piezo.get_x_resolution()) + " V")
                self.button_up_x.configure(text="X: +" + str(target_piezo.get_x_resolution()) + " V")
                self.button_down_y.configure(text="Y: -" + str(target_piezo.get_y_resolution()) + " V")
                self.button_up_y.configure(text="Y: +" + str(target_piezo.get_y_resolution()) + " V")
                self.button_down_z.configure(text="Z: -" + str(target_piezo.get_z_resolution()) + " V")
                self.button_up_z.configure(text="Z: +" + str(target_piezo.get_z_resolution()) + " V")


    def close(self):
        self.update_bool = False

    def get_osa_info(self):
        if len(self.instrument_controller.get_osa_list()) > 0  :
            controller = self.instrument_controller.get
            return "Voltage X: " + str(controller.get_x_voltage()) + ", " \
                                                                     "Y: " + str(controller.get_y_voltage()) + ", " \
                                                                                                               "Z: " + str(
                controller.get_z_voltage()) + ", ""\n" + \
                "Resolution X: " + str(controller.get_x_resolution()) + ", " \
                                                                        "Y: " + str(controller.get_y_resolution()) + ", " \
                                                                                                                     "Z: " + str(
                    controller.get_z_resolution())
        else:
            return ""

    def set_x_voltage_button(self):
        self.instrument_controller.input_piezo_controller.set_x_voltage(
            get_float_from_string(self.entry_1.get(),
                                  self.instrument_controller.input_piezo_controller.get_x_voltage()))


