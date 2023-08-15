from tkinter import ttk
from tqdm import tk


class Tune_Laser_Window:
    def __init__(self, root, laser, detector_list):
        self.tune_step = 1
        self.laser = laser
        self.detector_list = detector_list

        popup = ttk.Tk()
        popup.wm_title("Tune Laser")
        window_width = 250  # width for the Tk root
        window_height = 155  # height for the Tk root
        ws = popup.winfo_screenwidth()  # width of the screen
        hs = popup.winfo_screenheight()  # height of the screen
        x = ws - window_width * 2
        y = hs - window_height - 50
        popup.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        msg = "Wavelength = %0.2f nm" % (self.laser.get_detector_wavelength())
        label = popup.Label(popup, text=msg, font="Arial")
        label.pack(side="top", fill="x", pady=10)

        self.label = label

        button_1 = ttk.Button(popup)
        button_1["text"] = "+" + str(tune_step) + " nm"
        button_1["command"] = lambda: button_1_2()
        button_1.pack(side='right', fill='y')

        button_2 = ttk.Button(popup)
        button_2["text"] = "-" + str(tune_step) + " nm"
        button_2["command"] = lambda: button_1_2()
        button_2.pack(side='left', fill='y')

        entry_1 = ttk.Entry(popup)
        button_3 = ttk.Button(popup)
        button_3["text"] = "Go to [nm]"
        button_3["command"] = lambda: button3(entry_1, laser, label)
        button_3.pack(fill='y')
        entry_1.pack()

        entry_2 = ttk.Entry(popup)
        button_4 = ttk.Button(popup)
        button_4["text"] = "Set step [nm]"
        button_4["command"] = lambda: button4(entry_2, button_1, button_2)
        button_4.pack(fill='y')
        entry_2.pack()

        def set_step(step):
            global tune_step
            tune_step = float(step)

        def set_wavelength(wavelength):
            if (wavelength <= 980) and (wavelength >= 910):
                self.laser.set_wavelength_nm(wavelength)
            else:
                print("Error: " + str(round(wavelength, 1)) + " is not within the range 910-980nm")

        def update_label():
            message = "Wavelength = %0.2f nm" % (self.laser.get_detector_wavelength())
            self.label.config(text=message)

        def button_1_2():
            current_wavelength = self.laser.get_detector_wavelength()
            update_wavelength = current_wavelength + self.step
            set_wavelength(update_wavelength)
            update_label()

        def button3(entry):
            set_wavelength(get_float_from_string(entry.get(), self.laser.get_detector_wavelength()))
            update_label()

        def button4(entry, button_1, button_2):
            set_step(get_float_from_string(entry.get(), tune_step))
            button_1.configure(text="+" + str(tune_step) + " nm")
            button_2.configure(text="-" + str(tune_step) + " nm")

        def get_float_from_string(str, original_step):
            if str == '':
                return original_step
            else:
                return float(str)


if __name__ == "__main__":
    root = tk.Tk()
    app = Tune_Laser_Window(root)
    root.mainloop()