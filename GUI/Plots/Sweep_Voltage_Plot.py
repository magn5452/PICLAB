import matplotlib as mpl

mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import h5py
import datetime

from GUI.Functions.functions import *


class Sweep_Voltage_Plot_Window:
    def __init__(self, instrument_controller, gui_controller):
        self.voltage_array = None
        self.power_dBm_plot_list = None
        self.power_W_plot_list = None
        self.voltage_array_plot = None
        self.power_dBm_array = None
        self.power_W_array = None
        self.points_plot = None
        self.graph = None
        self.ax = None
        self.folder = "Attenuation"
        self.scan = 'Voltage'  # Loss, DFG, SFG
        self.chip = 'Filter'  # STOA, STOB, ST1, ST2
        self.component = ''  # 1750nm_WG1, Loss_980,
        self.add_info = ''

        self.instrument_controller = instrument_controller
        self.gui_controller = gui_controller
        self.target_detector = None
        self.laser = None
        self.target_detector_index = 0
        self.detector_list = None
        self.waveform_generator = None

        self.fig = None

    def setup_figure(self, frame):

        self.target_detector = self.instrument_controller.get_target_detector()
        self.target_detector_index = self.instrument_controller.get_target_detector()
        self.detector_list = self.instrument_controller.get_detector_list()
        self.laser = self.instrument_controller.get_target_laser()
        self.waveform_generator = self.instrument_controller.get_waveform_generator_list()[0]

        for detector in self.detector_list:
            detector.set_detector_wavelength(self.laser.get_wavelength())

        self.voltage_array = np.arange(self.instrument_controller.get_min_voltage(),
                                  self.instrument_controller.get_max_voltage() + self.instrument_controller.get_sweep_voltage(),
                                  self.instrument_controller.get_sweep_voltage(), dtype=float)

        rows, cols = (len(self.detector_list), len(self.voltage_array))

        self.power_W_array, self.power_dBm_array = np.empty([rows, cols]), np.empty([rows, cols])
        self.voltage_array_plot, self.power_W_plot_list, self.power_dBm_plot_list = [], [], []

        if self.fig is None:
            SMALL_SIZE, MEDIUM_SIZE, BIGGER_SIZE = 22, 24, 26
            mpl.rcParams['font.sans-serif'] = "Arial"
            plt.rc('font', size=MEDIUM_SIZE)
            plt.rc('axes', titlesize=MEDIUM_SIZE, labelsize=MEDIUM_SIZE)
            plt.rc('xtick', labelsize=SMALL_SIZE)
            plt.rc('ytick', labelsize=SMALL_SIZE)
            plt.rc('legend', fontsize=SMALL_SIZE)
            plt.rc('figure', titlesize=BIGGER_SIZE)

            SMALL_SIZE, MEDIUM_SIZE, BIGGER_SIZE = 22, 24, 26
            mpl.rcParams['font.sans-serif'] = "Arial"
            plt.rc('font', size=MEDIUM_SIZE)
            plt.rc('axes', titlesize=MEDIUM_SIZE, labelsize=MEDIUM_SIZE)
            plt.rc('xtick', labelsize=SMALL_SIZE)
            plt.rc('ytick', labelsize=SMALL_SIZE)
            plt.rc('legend', fontsize=SMALL_SIZE)
            plt.rc('figure', titlesize=BIGGER_SIZE)
            mpl.use("TkAgg")  # set the backend

            self.fig = Figure()
            self.graph = FigureCanvasTkAgg(self.fig, master=frame)
            self.graph.get_tk_widget().pack(side="right", fill='both', expand=True)

            self.ax = self.fig.add_subplot(111)
            self.ax.set(xlabel='Voltage (V)', ylabel='Power (dBm)')
            self.ax.grid()

        self.ax.set_xlim([self.instrument_controller.get_min_wavelength(), self.instrument_controller.get_max_wavelength()])
        self.points_plot, = self.ax.plot(self.voltage_array[0], 1,
                          marker='o', linestyle='-', color='blue', mec='k')

    def update(self):

        # Data Acquisition
        for voltage_index in range(len(self.voltage_array)):
            voltage = round(self.voltage_array[voltage_index], 3)
            self.waveform_generator.set_voltage(voltage)
            plt.pause(0.1)
            # Data Acquisition
            for detector_index in range(0, len(self.detector_list)):
                detector = self.detector_list[detector_index]
                power_W = detector.get_detector_power()
                power_dBm = power_W_to_dBm(power_W)

                self.power_W_array[detector_index][voltage_index] = power_W
                self.power_dBm_array[detector_index][voltage_index] = power_dBm

                if detector_index == self.instrument_controller.get_target_detector_index():
                    self.power_W_plot_list.append(power_W)
                    self.power_dBm_plot_list.append(power_dBm)
                    self.voltage_array_plot.append(voltage)

            # Plot
            self.points_plot.set_data(self.voltage_array_plot, self.power_dBm_plot_list)

            self.ax.set_ylim([min(self.power_dBm_plot_list) - 1, max(self.power_dBm_plot_list) + 1])

            self.graph.draw()
            plt.pause(0.5)

        self.save_data()
        self.gui_controller.is_wavelength_seep_on = False

    def save_data(self):
        beginning_time = datetime.datetime.now()
        filename = beginning_time.strftime("%Y-%m-%d_%H-%M-%S") + "_" + \
                   self.scan + "_" + \
                   self.chip + "_" + \
                   self.component + "_" + \
                   self.add_info + \
                   str(self.laser.get_name()) + "_" + \
                   str(self.laser.get_wavelength()) + "_" + \
                   str(self.instrument_controller.get_min_voltage()) + "_" + \
                   str(self.instrument_controller.get_max_voltage()) + "_" + \
                   str(self.instrument_controller.get_sweep_voltage())

        if self.gui_controller.save_bool:
            header = \
                "#\n# Date: %s\n#\n" % beginning_time.strftime("%Y-%m-%d_%H-%M-%S") + "_" \
                                                                                      "# Scan type: %s\n" % self.scan + \
                "# Chip: %s\n" % self.chip + \
                "# Component: %s\n" % self.component + \
                "# Additional info: %s\n#\n" % self.add_info + \
                "# Laser: %s\n" % self.laser.get_name()

            # Transmission alignment

            self.fig.savefig("Figures/" + filename + ".pdf", bbox_inches='tight')
            hf = h5py.File('Data/' + self.folder + '/' + filename + '.h5', 'w')
            hf.create_dataset('Header', data=header)
            hf.create_dataset('Voltage_V', data=self.voltage_array)
            for detector_index in range(0, len(self.detector_list)):
                hf.create_dataset(self.detector_list[detector_index].get_name() + "_power_W",
                                  data=self.power_W_array[detector_index])

            hf.close()

    def close(self):
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
