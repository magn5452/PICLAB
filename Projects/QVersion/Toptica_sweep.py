################################################################
# Qversion, Toptica running - Emil Z. Ulsig, AU
################################################################
from Python_lib.Toptica_CTL950 import *
from Python_lib.Thorlabs_PM100U import Thorlabs_PM100U
#from Python_lib.Yokogawa import Yokogawa
import tkinter as tk
from tkinter import ttk
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pyvisa as visa
import h5py
import  datetime
#from GUI import *

rm = visa.ResourceManager()
rl = rm.list_resources()
print(rl)
# sys.exit()
################################################################
# Scan settings

chip = 'Normalization_10%'
device = ''
add_info = ''
scan = '1nm'

power_laser_mW = 20 # [mW] Laser output power 

wav_min_nm = 920 # [nm]
wav_max_nm = 980 # [nm]

step_size = 1 # [nm]

wav_array = np.arange(wav_min_nm, wav_max_nm + 0.01, step_size, dtype=float)

wav_nm = (wav_max_nm + wav_min_nm)/2
wav_PD_nm = wav_nm  # [nm]



beginning = datetime.datetime.now()
fname_base = beginning.strftime("%Y-%m-%d_%H-%M-%S") +\
            chip +\
            device +\
            scan +\
            '_Run_' + \
            str(power_laser_mW) + 'mW_' + \
            str(wav_nm) + 'nm_' + add_info

################################################################
# Initialize

# Detector - input monitor
thor_PM100usb_ch = 'USB0::0x1313::0x8076::M00905456::INSTR'
det_in = Thorlabs_PM100U(rm, thor_PM100usb_ch)
det_in.set_detector_wavelength(wav_PD_nm)
det_in.set_units('W')
#det_in.set_averaging(20)
# det_.zero()

## Output detector
thor_PM100usb_conf =  'USB0::0x1313::0x8076::M00905457::INSTR'
det_out = Thorlabs_PM100U(rm, thor_PM100usb_conf)
det_out.set_detector_wavelength(wav_PD_nm)
det_out.set_units('W') # dBm or W, dBm may not work
#det_out.set_averaging(20)
#det_out.zero()

# Laser controller
CTL = Toptica_CTL950()

CTL.set_power_stabilization_status(True)
CTL.set_power_stabilization_parameters(0.3, 15, 0, 1)
CTL.set_wavelength(wav_nm)
CTL.set_power(power_laser_mW)


######

def btn_cmd():
    global acquisition_flag
    running = False


def popupmsg():
    popup = tk.Tk()
    popup.wm_title("Data acquisition")
    msg = "Aquisition running..."
    label = ttk.Label(popup, text=msg, font="Arial")
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="End acquisition", command=btn_cmd)
    B1.pack()
    w = 400  # width for the Tk root
    h = 100  # height for the Tk root
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = (ws / 2) - (w / 2)
    y = hs - h - 50
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return popup, ws, hs


def jog(CTL, step):
    currentWav = CTL.get_detector_wavelength()
    moveTo = currentWav + step
    if (moveTo < 980) and (moveTo > 910):
        CTL.set_wavelength_nm(currentWav + step)
    else:
        print('Error: Maximal range are between 910-980nm.')


def set_wav(CTL, wav):
    CTL.set_wavelength_nm(wav)

def set_step(step):
    global tune_step
    tune_step = float(step)


def update_label(label, CTL):
    msg = "Wavelength = %0.3f nm" % (CTL.get_detector_wavelength())
    label.config(text=msg)


def tune(CTL):
    popup = tk.Tk()
    popup.wm_title("Tuning")
    msg = "Wavelength = %0.3f nm" % (CTL.get_detector_wavelength())
    label = ttk.Label(popup, text=msg, font="Arial")
    label.pack(side="top", fill="x", pady=10)
    global tune_step
    tune_step = 1.0
    B1 = ttk.Button(popup, text="+", command=lambda: [jog(CTL, tune_step), update_label(label, CTL)])
    B1.pack(side='right', fill='y')
    B2 = ttk.Button(popup, text="-", command=lambda: [jog(CTL, -tune_step), update_label(label, CTL)])
    B2.pack(side='left', fill='y')

    E1 = ttk.Entry(popup)
    B3 = ttk.Button(popup, text="Go to", command=lambda: [set_wav(CTL, float(E1.get())), update_label(label, CTL)])
    B3.pack(fill='y')
    E1.pack()

    E2 = ttk.Entry(popup)
    B4 = ttk.Button(popup, text="Set step", command=lambda: [set_step(E2.get())])
    B4.pack(fill='y')
    E2.pack()

    w = 222  # width for the Tk root
    h = 135  # height for the Tk root
    ws = popup.winfo_screenwidth()  # width of the screen
    hs = popup.winfo_screenheight()  # height of the screen
    x = ws - w * 1.5
    y = hs - h - 50
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return popup


SMALL_SIZE, MEDIUM_SIZE, BIGGER_SIZE = 22, 24, 26
LW, MS, MEW = 2.0, 5.0, 0.5
mpl.rcParams['font.sans-serif'] = "Arial"
plt.rc('font', size=MEDIUM_SIZE)
plt.rc('axes', titlesize=MEDIUM_SIZE, labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=SMALL_SIZE)
plt.rc('ytick', labelsize=SMALL_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE)
mpl.use("TkAgg")  # set the backend
yrange, xrange = 2, 45  # [dB] +/-, [s]


################################################################
# Run alignment

print("Running alignment...")

## Transmission alignment

split_ratio = 0  # [dB]

P_in_W, P_out_W, x = [], [], []
T0 = datetime.datetime.now()
T = T0 - T0

P_in_W_up = det_in.get_detector_power()
P_in_W.append(P_in_W_up)

P_out_W_up = det_out.get_detector_power()
P_out_W.append(P_out_W_up)

P_dB_up = 10 * np.log10(P_out_W_up / P_in_W_up)
P_dB = 10 * np.log10(np.array(P_out_W) / np.array(P_in_W)) - split_ratio
P_dBm = 10 * np.log10(np.array(P_out_W) * 1e3)

x.append(T.seconds + T.microseconds / 1e6)
pmax = np.ones(len(x)) * P_dB_up
y_c = int(P_dB_up) + (P_dB_up % 1 > 0)

pm, ws, hs = popupmsg()
pt = tune(CTL)
figT, ax = plt.subplots()
points, = ax.plot(x, P_dBm,
                  marker='o', linestyle='-', color='k',
                  lw=LW, ms=MS, mec='k', mew=MEW)
pmaxs, = ax.plot(x, pmax,
                 marker='', linestyle='-', color='b',
                 lw=LW, ms=MS, mec='k', mew=MEW)
ax.set(xlabel='Time (s)', ylabel='Power (dBm)')
ax.grid()
DPI = figT.get_dpi()
figT.set_size_inches((ws - 80) / DPI, (hs - 200) / DPI, forward=True)
figT.canvas.manager.window.wm_geometry('+80+0')

acquisition_flag = True  # Global flag
while acquisition_flag:

    T = datetime.datetime.now() - T0
    T_up = T.seconds + T.microseconds / 1e6

    P_in_W_up = det_in.get_detector_power()
    P_in_W.append(P_in_W_up)

    P_out_W_up = det_out.get_detector_power()
    P_out_W.append(P_out_W_up)

    P_dB_up = 10 * np.log10(P_out_W_up / P_in_W_up) - split_ratio
    P_dB = 10 * np.log10(np.array(P_out_W) / np.array(P_in_W)) - split_ratio

    P_dBm_up = 10 * np.log10(P_out_W_up * 1e3)
    P_dBm = 10 * np.log10(np.array(P_out_W) * 1e3)

    x.append(T_up)
    points.set_data(x, P_dBm)
    
    max_y = max(P_dBm)
    pmax = np.ones(len(P_dBm)) * max_y
    pmaxs.set_data(x, pmax)

    ax.set_xlim([T_up - xrange, T_up])
    if (P_dBm_up > (y_c + (yrange - 0.1))):
        y_c = int(P_dBm_up)
    if (P_dBm_up < (y_c - (yrange - 0.1))):
        y_c = int(P_dBm_up + 1)
    ax.set_ylim([y_c - yrange, y_c + yrange])


    plt.pause(0.001)

pm.destroy()
pt.destroy()
plt.close(figT)

################################################################
# Run sweep

P_in_W, P_out_W, x = [], [], []

P_in_W_up = det_in.get_detector_power()
P_in_W.append(P_in_W_up)

P_out_W_up = det_out.get_detector_power()
P_out_W.append(P_out_W_up)

P_dB_up = 10 * np.log10(P_out_W_up / P_in_W_up)
P_dB = 10 * np.log10(np.array(P_out_W) / np.array(P_in_W)) - split_ratio
P_dBm = 10 * np.log10(np.array(P_out_W) * 1e3)

x.append(wav_array[0])

figL, ax = plt.subplots()
points, = ax.plot(x, P_dBm,
                  marker='o', linestyle='-', color='k',
                  lw=LW, ms=MS, mec='k', mew=MEW)

ax.set(xlabel='Wavelength (nm)', ylabel='Power (dBm)')
ax.grid()
ax.set_xlim([wav_min_nm, wav_max_nm])
DPI = figL.get_dpi()
figL.set_size_inches((ws - 80) / DPI, (hs - 200) / DPI, forward=True)
figL.canvas.manager.window.wm_geometry('+80+0')

for kk in range(len(wav_array)):
    CTL.set_wavelength(wav_array[kk])

    P_in_W_up = det_in.get_detector_power()
    P_in_W.append(P_in_W_up)

    P_out_W_up = det_out.get_detector_power()
    P_out_W.append(P_out_W_up)

    P_dB_up = 10 * np.log10(P_out_W_up / P_in_W_up) - split_ratio
    P_dB = 10 * np.log10(np.array(P_out_W) / np.array(P_in_W)) - split_ratio

    P_dBm_up = 10 * np.log10(P_out_W_up * 1e3)
    P_dBm = 10 * np.log10(np.array(P_out_W) * 1e3)

    x.append(wav_array[kk])
    points.set_data(x, P_dBm)

    ax.set_ylim([min(P_dBm), max(P_dBm)])



    plt.pause(0.001)

plt.close()

################################################################
# Save data

filename = fname_base

header = \
    "#\n# Date: %s\n#\n" % beginning.strftime("%Y-%m-%d_%H-%M-%S") + \
    "# Scan type: %s\n" % scan + \
    "# Chip: %s\n" % chip + \
    "# Device: %s\n" % device + \
    "# Additional info: %s\n#\n" % add_info + \
    "# Alignment wavelength: %s nm\n#\n" % wav_nm + \
    "# Input detector: %s\n" % det_in.info[0:-1] + \
    "# Output detector: %s\n" % det_out.info[0:-1] + \
    "# Laser: Toptica\n"

# Transmission alignment
figL.savefig("Figures/" + filename + "_L.pdf", bbox_inches='tight')
hf = h5py.File('Data/' + filename + '_L.h5', 'w')
hf.create_dataset('header', data=header)
hf.create_dataset('Time', data=x)
hf.create_dataset('P_in_W', data=P_in_W)
hf.create_dataset('P_out_W', data=P_out_W)
hf.close()

################################################################
# Finalize equipment

CTL.close()
det_in.close()
det_out.close()

################################################################
# End

ending = datetime.datetime.now()
elapsed = ending - beginning
elapsed_min = int(elapsed.seconds / 60)
elapsed_sec = elapsed.seconds - elapsed_min * 60

print("Elapsed time = {0:2d} minutes {1:2d} seconds".format(elapsed_min, elapsed_sec))

################################################################