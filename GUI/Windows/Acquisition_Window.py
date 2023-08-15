import threading

import datetime

import matplotlib as mpl

mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from GUI.Functions.functions import power_W_to_dBm


class Acquisition_Window:
    def __init__(self, instrument_controller, gui_controller):
        self.acqusition_plot_thread = None
        self.detector_acquisition_thread_list = []
        self.detector_acquisition_flag = True
        self.pause_flag = False
        self.gui_controller = gui_controller
        self.instrument_controller = instrument_controller
        self.ws = 2000
        self.hs = 1500
        self.plotting_flag = False
        self.fig = None
        self.ax = None

        self.power_list, self.power_dBm_list, self.power_dBm_max_list, self.time_list = [], [], [], []

        self.y_c = None

        self.points_plot = None
        self.power_max_plot = None
        self.yrange, self.xrange = 2, 45  # [dB] +/-, [s]
        self.T0 = datetime.datetime.now()

        self.graph = None

    def setup_figure(self, main_window):

        self.plotting_flag = True

        ## Transmission alignment

        power_list, power_dBm_list, power_dBm_max_list, time_list = [], [], [], []
        T = self.T0 - self.T0

        power = self.instrument_controller.get_target_detector().get_detector_power()
        self.power_list.append(power)

        power_dBm = power_W_to_dBm(power)
        self.power_dBm_list.append(power_dBm)

        power_dBm_max = power_dBm
        self.power_dBm_max_list.append(power_dBm_max)

        self.time_list.append(T.seconds + T.microseconds / 1e6)

        self.y_c = int(power_dBm) + (power_dBm % 1 > 0)

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
            self.graph = FigureCanvasTkAgg(self.fig, master=main_window)
            self.graph.get_tk_widget().pack(side="right", fill='both', expand=True)

            self.ax = self.fig.add_subplot(111)
            self.ax.set(xlabel='Time (s)', ylabel='Power (dBm)')
            self.ax.grid()

        self.points_plot, = self.ax.plot(time_list, power_dBm_list, linestyle='-', color='red', mec='k')
        self.power_max_plot, = self.ax.plot(time_list, power_dBm_max_list, marker='', linestyle='-', color='blue',
                                            mec='k')

    def detector_acquisition(self, detector):
        while self.detector_acquisition_flag:
            if not self.pause_flag:
                detector.set_detector_wavelength()
                detector.get_detector_power()



    def update(self):
        self.start_acquisition()
        self.start_plotting()

    def start_plotting(self):
        self.acquisition_plot()

    def acquisition_plot(self):
        while self.plotting_flag:
            T = datetime.datetime.now() - self.T0
            T_up = T.seconds + T.microseconds / 1e6
            # Update Plot

            self.time_list.append(T_up)
            power_dBm = power_W_to_dBm(self.instrument_controller.get_target_detector().get_detector_power_get())
            self.power_dBm_list.append(power_dBm)
            self.points_plot.set_data(self.time_list, self.power_dBm_list)

            x_left_limit_index = 0
            power_dBm_max = max(self.power_dBm_list[x_left_limit_index: -1])
            self.power_dBm_max_list.append(power_dBm_max)
            self.power_max_plot.set_data(self.time_list, self.power_dBm_max_list)

            self.ax.set_xlim([T_up - self.xrange, T_up])
            if power_dBm > (self.y_c + (self.yrange - 0.1)):
                self.y_c = int(power_dBm)
            if power_dBm < (self.y_c - (self.yrange - 0.1)):
                self.y_c = int(power_dBm + 1)

            self.ax.set_ylim([self.y_c - self.yrange, self.y_c + self.yrange])
            if self.plotting_flag:
                self.graph.draw()
        self.gui_controller.is_wavelength_sweep_on = False

    def start_acquisition(self):
        for detector in self.instrument_controller.get_detector_list():
            detector_thread = threading.Thread(target=self.detector_acquisition, args=[detector])
            detector_thread.start()
            self.detector_acquisition_thread_list.append(detector_thread)

    def set_pause_flag(self, flag):
        self.pause_flag = flag

    def close(self):
        self.pause_flag = True
        self.detector_acquisition_flag = False
        for thread in self.detector_acquisition_thread_list:
            thread.join()

        self.plotting_flag = False
