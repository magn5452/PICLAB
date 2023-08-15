import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

global detector_plot
global acquisition_flag
global sweep_flag
global save_bool  # Global flags
global units_mW

detector_plot_index = 2
save_bool = True
acquisition_flag = True
sweep_flag = True
units_mW = True


def set_wavelength(laser, detector_list, wavelength):
    laser.set_wavelength_nm(wavelength)
    for detector in detector_list:
        detector.set_wavelength_nm(wavelength)


def get_float_from_string(str, original_step):
    if str == '':
        return original_step
    else:
        return float(str)


def power_W_to_dBm(power_W):
    return 10 * np.log10(power_W * 1000)


def power_to_dB(power_1, power_2):
    return 10 * np.log10(power_1 / power_2)


def update_label(label, laser):
    msg = "Wavelength = %0.2f nm" % (laser.get_detector_wavelength()) + "\n Power = %0.2f mW" % (laser.get_detector_power())
    label.config(text=msg)


def tune_laser_window_button(laser, detector_list, step, label):
    current_wavelength = laser.get_detector_wavelength()
    update_wavelength = current_wavelength + step
    set_wavelength(laser, detector_list, update_wavelength)
    update_label(label, laser)


def button_1_2(laser, detector_list, step, label):
    current_wavelength = laser.get_detector_wavelength()
    update_wavelength = current_wavelength + step
    set_wavelength(laser, detector_list, update_wavelength)
    update_label(label, laser)


def button3(entry, laser, detector_list, label):
    set_wavelength(laser, detector_list,
                   get_float_from_string(entry.get(), laser.get_detector_wavelength()))
    update_label(label, laser)


def button_5_6(laser, step, label):
    current_power = laser.get_detector_power()
    update_power = current_power + step
    laser.set_power_mW(update_power)
    update_label(label, laser)


def button7(entry, laser, label):
    laser.set_power_mW(get_float_from_string(entry.get(), laser.get_detector_power()))
    update_label(label, laser)


def set_step_power(step):
    global tune_step_power
    tune_step_power = float(step)


def set_step_wavelength(step):
    global tune_step_wavelength
    tune_step_wavelength = float(step)


def button4(entry, button_1, button_2):
    set_step_wavelength(get_float_from_string(entry.get(), tune_step_wavelength))
    button_1.configure(text="+" + str(tune_step_wavelength) + " nm")
    button_2.configure(text="-" + str(tune_step_wavelength) + " nm")


def button8(entry, button_5, button_6):
    set_step_power(get_float_from_string(entry.get(), tune_step_power))
    button_5.configure(text="+" + str(tune_step_power) + " mW")
    button_6.configure(text="-" + str(tune_step_power) + " mW")


def toggle_units_mW():
    global units_mW
    units_mW = not units_mW


def end_acquisition():
    global acquisition_flag
    acquisition_flag = False


def end_everything():
    global acquisition_flag, sweep_flag, save_bool
    acquisition_flag = False
    sweep_flag = False
    save_bool = False


def toggle_save_bool(label):
    global save_bool
    save_bool = not save_bool
    print("Save bool is set to: " + str(save_bool))
    label.config(text="Aquisition running... Save bool: " + str(save_bool))


def data_acquisition_window():
    global save_bool
    popup = tk.Tk()
    popup.wm_title("Data acquisition")
    msg = "Aquisition running... Save bool: " + str(save_bool)
    label = ttk.Label(popup, text=msg, font="Arial")
    label.pack(side="top", fill="x", pady=10)

    button_1 = ttk.Button(popup)
    button_1["text"] = "End acquisition"
    button_1["command"] = lambda: end_acquisition()
    button_1.pack()

    button_2 = ttk.Button(popup)
    button_2["text"] = "End everything"
    button_2["command"] = lambda: end_everything()
    button_2.pack()

    button_3 = ttk.Button(popup)
    button_3["text"] = "Toggle Save Sweep"
    button_3["command"] = lambda: toggle_save_bool(label)
    button_3.pack()

    w = 300  # width for the Tk root
    h = 150  # height for the Tk root
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (w / 2)
    y = hs - h - 50
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return popup, ws, hs


def increment_detector_window(detector_list):
    popup = tk.Tk()
    popup.wm_title("Change Detector")
    label = ttk.Label(popup, text="", font="Arial")
    label.pack(side="top", fill="x", pady=10)
    button_1 = ttk.Button()
    button_1["text"] = "Increment Detector"
    button_1["command"] = lambda: increment_detector_plot(detector_list)
    button_1.pack()

    w = 150  # width for the Tk root
    h = 100  # height for the Tk root
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (w / 2) + 200
    y = hs - h - 50
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return popup


def increment_detector_plot(detector_list):
    global detector_plot_index
    detector_plot_index = np.mod(detector_list.index(detector_list[detector_plot_index]) + 1, len(detector_list))


def tune_laser_window(laser, detector_list):
    popup = tk.Tk()
    popup.wm_title("Tune Laser")
    window_width = 400  # width for the Tk root
    window_height = 230  # height for the Tk root
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = ws - window_width * 2
    y = hs - window_height - 50
    popup.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

    msg = "Wavelength = %0.2f nm" % (laser.get_detector_wavelength()) + " Power = %0.2f mW" % (laser.get_detector_power() * 1000)
    label = ttk.Label(popup, text=msg, font="Arial")
    label.pack(side="top", fill="x", pady=10)

    global tune_step_wavelength
    tune_step_wavelength = 1.0
    button_1 = ttk.Button(popup)
    button_1["text"] = "+" + str(tune_step_wavelength) + " nm"
    button_1["command"] = lambda: button_1_2(laser, detector_list,
                                             tune_step_wavelength, label)
    button_1.pack(side='right', fill='y')

    button_2 = ttk.Button(popup)
    button_2["text"] = "-" + str(tune_step_wavelength) + " nm"
    button_2["command"] = lambda: button_1_2(laser, detector_list,
                                             -tune_step_wavelength, label)
    button_2.pack(side='left', fill='y')

    global tune_step_power
    tune_step_power = 1.0
    button_5 = ttk.Button(popup)
    button_5["text"] = "+" + str(tune_step_power) + " mW"
    button_5["command"] = lambda: button_5_6(laser, tune_step_power, label)
    button_5.pack(side='right', fill='y')

    button_6 = ttk.Button(popup)
    button_6["text"] = "-" + str(tune_step_power) + " mW"
    button_6["command"] = lambda: button_5_6(laser, -tune_step_power, label)
    button_6.pack(side='left', fill='y')

    entry_1 = ttk.Entry(popup)
    button_3 = ttk.Button(popup)
    button_3["text"] = "Go to [nm]"
    button_3["command"] = lambda: button3(entry_1, laser, detector_list, label)
    button_3.pack(fill='y')
    entry_1.pack()

    entry_2 = ttk.Entry(popup)
    button_4 = ttk.Button(popup)
    button_4["text"] = "Set step [nm]"
    button_4["command"] = lambda: button4(entry_2, button_1, button_2)
    button_4.pack(fill='y')
    entry_2.pack()

    entry_3 = ttk.Entry(popup)
    button_7 = ttk.Button(popup)
    button_7["text"] = "Go to [mW]"
    button_7["command"] = lambda: button7(entry_3, laser, label)
    button_7.pack(fill='y')
    entry_3.pack()

    entry_4 = ttk.Entry(popup)
    button_8 = ttk.Button(popup)
    button_8["text"] = "Set step [mW]"
    button_8["command"] = lambda: button8(entry_4, button_5, button_6)
    button_8.pack(fill='y')
    entry_4.pack()

    return popup


def main_window(toptica_laser, detector_list):
    popup = tk.Tk()
    popup.wm_title("Tune Laser")
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    window_width = ws  # width for the Tk root
    window_height = hs  # height for the Tk root
    x = ws  # - window_width * 2
    y = hs  # - window_height - 50
    popup.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

    ##Create window frames
    right_frame = tk.Frame(popup, width=window_width / 10, height=window_height / 10)
    right_frame.pack(side='right', fill='both', padx=10, pady=5, expand=True)

    bottom_frame = tk.Frame(popup, width=window_width / 8, height=window_height / 10)
    bottom_frame.pack(side='bottom', fill='both', padx=10, pady=5, expand=True)

    ## Packing buttons
    # Data aquisition window
    msg_bool = "Aquisition running... Save bool: " + str(save_bool)
    label_bool = ttk.Label(bottom_frame, text=msg_bool, font="Arial")
    label_bool.pack(side="top", fill="x", pady=10)

    button_end = ttk.Button(bottom_frame)
    button_end["text"] = "End acquisition"
    button_end["command"] = lambda: end_acquisition()
    button_end.pack(side='left', expand=True)

    button_end_all = ttk.Button(bottom_frame)
    button_end_all["text"] = "End everything"
    button_end_all["command"] = lambda: end_everything()
    button_end_all.pack(side='left', expand=True)

    button_sweep = ttk.Button(bottom_frame)
    button_sweep["text"] = "Toggle Save Sweep"
    button_sweep["command"] = lambda: toggle_save_bool(label_bool)
    button_sweep.pack(side='left', expand=True)

    # Increment detector
    button_inc = ttk.Button(bottom_frame)
    button_inc["text"] = "Increment Detector"
    button_inc["command"] = lambda: increment_detector_plot(detector_list)
    button_inc.pack(side='left', expand=True)

    # Change units
    button_units = ttk.Button(bottom_frame)
    button_units["text"] = "Change units"
    button_units["command"] = lambda: toggle_units_mW()
    button_units.pack(side='left', expand=True)

    ## Wavelength tuning
    msg_wav = "Wavelength = %0.2f nm" % (toptica_laser.get_detector_wavelength()) + "\n Power = %0.2f mW" % (
        toptica_laser.get_detector_power())
    label = ttk.Label(right_frame, text=msg_wav, font="Arial")
    label.pack(side="top", fill="y", pady=10)

    global tune_step_wavelength
    tune_step_wavelength = 1.0

    button_frame = tk.Frame(right_frame, width=0, height=0)
    button_frame.pack(side='top', fill='x', padx=10, pady=10, expand=False)

    button_1 = ttk.Button(button_frame)
    button_1["text"] = "+" + str(tune_step_wavelength) + " nm"
    button_1["command"] = lambda: button_1_2(toptica_laser, detector_list,
                                             tune_step_wavelength, label)
    button_1.pack(side='right')

    button_2 = ttk.Button(button_frame)
    button_2["text"] = "-" + str(tune_step_wavelength) + " nm"
    button_2["command"] = lambda: button_1_2(toptica_laser, detector_list,
                                             -tune_step_wavelength, label)
    button_2.pack(side='left')

    global tune_step_power
    tune_step_power = 1.0
    button_power_frame = tk.Frame(right_frame, width=0, height=0)
    button_power_frame.pack(side='top', fill='x', padx=10, pady=10, expand=False)

    button_5 = ttk.Button(button_power_frame)
    button_5["text"] = "+" + str(tune_step_power) + " mW"
    button_5["command"] = lambda: button_5_6(toptica_laser, tune_step_power, label)
    button_5.pack(side='right', fill='y')

    button_6 = ttk.Button(button_power_frame)
    button_6["text"] = "-" + str(tune_step_power) + " mW"
    button_6["command"] = lambda: button_5_6(toptica_laser, -tune_step_power, label)
    button_6.pack(side='left', fill='y')

    entry_1 = ttk.Entry(right_frame)
    button_3 = ttk.Button(right_frame)
    button_3["text"] = "Go to [nm]"
    button_3["command"] = lambda: button3(entry_1, toptica_laser, detector_list, label)
    button_3.pack(fill='x')
    entry_1.pack()

    entry_2 = ttk.Entry(right_frame)
    button_4 = ttk.Button(right_frame)
    button_4["text"] = "Set step [nm]"
    button_4["command"] = lambda: button4(entry_2, button_1, button_2)
    button_4.pack(fill='x')
    entry_2.pack()

    entry_3 = ttk.Entry(right_frame)
    button_7 = ttk.Button(right_frame)
    button_7["text"] = "Go to [mW]"
    button_7["command"] = lambda: button7(entry_3, toptica_laser, label)
    button_7.pack(fill='x')
    entry_3.pack()

    entry_4 = ttk.Entry(right_frame)
    button_8 = ttk.Button(right_frame)
    button_8["text"] = "Set step [mW]"
    button_8["command"] = lambda: button8(entry_4, button_5, button_6)
    button_8.pack(fill='y')
    entry_4.pack()

    return popup, ws, hs
