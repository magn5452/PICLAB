########################################################################################
###PYTHON DRIVERS FOR LAB INSTRUMENTS###################################################
###By the PIC group at AU ENG###########################################################
########################################################################################
###Version 1.13##########################################################################
###Version history:
##1.13 - Added Keithley class, optical BW class, and Agilent funcionality (Lars) <Date: 23-08-21> 
#			* Now a fast free running sweep of the Agilent laser is possible with the new GetWLScan function
#			* It is possible to get the sampled arrays of the Agilent power meters from the sweep through the 
#			  functions: ReadPower0Array and ReadPower1Array
#			* A driver class, FILT_WLTF, for the WLTF optical bandpass filter from WL Photonics has been addded
#			* A driver class, DC_KEITHLEY_GRAPH, for the "new" Keithleys has been added
#			* Bugs in the Sweep2D class was fixed. Now all combinations of lists 
#			  and integers should be valid as inputs to the get and set functions
##1.12 - Added new equipment drivers (Lars)  <Date: 16-02-2021>
#           * ESA_SIGLENT class added for Siglent ESA
#           * PM100USB class added for Thorlabs USB power meters
#			* TLPM class added --> needed by PM100USB
##1.11 - Added Piezo controller driver and automatic alignment functionality (Lars)  <Date: 02-06-2020>
#           * PZ_BPC303 class added
#           * AutomaticAlignment class added
##1.10 - Added functions and bug fixing (Andreas)  <Date: 15-05-2020>
#           * PRO8000 PID settings; read and write
#           * Sweep functions have been fixed where possible
##1.09a - Tested and fixed continuous and step tuning options
##1.09 - Added functions for Agilent 8164B (untested)
#           * Amplitude modulation
#           * Coherence Control (artificial laser linewidth broadening)
#           * Sweep functions (continuous and step)
##1.08 - Added functionality (Mircea Balauroiu) <Date: 04-12-2019>
#           * For the R&S®FSW50 ESA, use the same class as for the FSV30.Use 192.168.1.100 for the IP address.
#           * Mailing function added.(still prototype).
#           * Rudimentary simple 1-D plotting has been added.
#           * Rudimentary GPIB connection function has been added.
##1.07 - Added HP 8153A Power Meter Funcionality (Mircea Balauroiu, Hanna Becker)
#           * HP 8153A has been implemented with rudimentary functionality 
#			* NOT all funconalities validated yet
##1.06 - Minor fixes to EDFA and additions to ESA and EDFA functionallity (P. Tønning) <Date: 28-08-2019>
#           * EDFA: control of EDFA fixed, NOTE: remote control only possible in full range 
#             for Set Current (ACC) mode, APC mode only functional in 20-30dBm range.
#             The EDFA only takes integer inputs! See EDFA code documentation for more details  
#           * ESA: the function ReadPeakPower has been added which returns just the peak power
#             of single peak, assuming the position of this peak is known.       
##1.05 - Minor fixes and added instruments (A. Hänsel, L. Nielsen) DATE: 02-08-2019
#           * ESA: function ReadSpectrumPN() added for future support of phase noise
#			  measurements.
#           * OSA: StartMeasurement() and ReadSpectrumSimple() added. ReadPeakData() has
#			  has been update. Also, OSA is now initialized to be in single sweep mode.
#           * New instruments:
#			 - Tektronix TDS 320 oscilloscope class added:  OSC_TDS320 (limited/beta)
#            - OZ optics ODL650 variable delay line class added: DL_ODL_650 
#            - Keopsys EDFA class added: EDFA_KEOPSYS
###1.04 - Major update of OSA ethernet interface + minor (Lars Nielsen) DATE: 11-03-2019
#           * socketInstrument class added to emulate pyVISA interface for TCP/IP socket
#           * OSA_YENISTA_OSA20 instrument class can now use ethernet connection by
#             setting GPIB_interface=-1, and reductionFactor has been removed.
#           * Default interface for ESA is now ethernet, number of datapoints in
#             sweep is 20001, and the reset of the instrument in initialization removed.
#           * SetCurrentFast() added to DC_PRO8000
#           * Sweep2D live plotting now only diplays the recent traces from spectrum
#             analyzers. This reduces memory consumption and increases speed.
#           * Functions added to DC_KEITHLEY: SetIntegrationtime, 
#             GetIntegrationtime, SetMode, GetMode, SetWire, GetWire (Hanna Becker)
###1.03 - Major update (Lars Nielsen) DATE: 22-01-2019
#           * Analyze2D for analyzing data generated with Sweep2D added
#           * GetMeas() of DC_KEITHLEY corrected to return float instead of string
#           * The default interface for ESA_RS_FSV30 is now TCP/IP
#           * SetReverseBias() function added to DC_NI_cdaq (line 287+):
#           * "import PyDAQmx" and "from PyDAQmx import Task" has been uncommented
###1.02 - Added LMS_AGILENT_8164B Laser Functionality
###1.01 - Added functionality (Lars Nielsen)
#           * Yenista ReadSpectrum() is now working (but slow!)
#           * The GPIB interface number is now chosen from the 'GPIB_interface' argument
#           * BETA AnalyzeData class added for loading data generated with SWEEP2D
###1.0 - Initial release (Designers: Lars Nielsen, Andreas Hänsel)
##NOTES:###############################################################################
## 1) All frequencies should be given in MHz
## 2) Voltages and currents in Ampere and Volt (if on linear scale)
## 3) Temperatures in degree Celsius

##SUPPORTED INSTRUMENTS:###############################################################
##Spectrum Analyzers:						####
##1.1) Rhode & Schwarz FSV30                (ESA_RS_FSV30)        [IP: 192.168.1.7] or 
##                                                                [GPIB:20]
##1.2) Yenista Optics OSA20                 (OSA_YENISTA_OSA20)   [GPIB:16] or 
##                                                                [IP: 192.168.1.3, port=5025]
##1.3) Siglent								(ESA_SIGLENT)		  [IP: 192.168.1.11]
##Quasi DC:									####
##2.1) Thorlabs PRO8000 + cards             (DC_PRO8000)          [GPIB:10] NOT TESTED
##2.2) Keithley 2401 Source Meter           (DC_KEITHLEY)         [GPIB:21,24] 
##2.3) NI cDAQ multi-channel Voltage source (DC_NI_cDAQ)          [USB connection]
##Signal Generators:						####
##3.1) Rhode & Schwarz SMF100A 1..22 GHz    (SG_RS_SMF100A)       [GPIB:09]
##Lightwave Measurement Systems:			####
##4.1) Agilent 8164B                        (LMS_AGILENT_8164B)   [GPIB:18]
##4.2) Ando AQ4321A                         (LMS_ANDO_AQ4321A)    [GPIB:19]
##4.3) HP 8153A                             (LMS_HP_8153A)        [GPIB:22]
##4.4) Thorlabs power meters				(PM100USB)	          [USB connection]
##Oscilloscopes								####
##5.1) Tektronix TDS 320					(OSC_TDS320)		  [GPIB:30]
##Amplifiers:								####
##6.1) Keopsys EDFA							(EDFA_KEOPSYS)		  [IP: 192.168.1.20]
##Misc:										####
##7.1) OZ optics ODL 650 variable delay line (DL_ODL_650)		  [COM5]
##7.2) Thorlabs Piezo Controller BPC303     (PZ_BPC303)           [COM3] (can be set) USB virtual COM port!!!
##Lasers:								####
##8.1) Toptica CTL 950						(TOPTICA_CTL950)	  [IP: 192.168.1.100]

##SUPPORTED FUNCTIONALITY:############################################################
##Sweeps:
##1.1) 2-dimensional sweep available        (Sweep2D)
##Data analysis:
##2.1) Simple load function available       (Analyze2D)
##Instrument control:
##3.1) Automatic alignment algorithm        (AutomaticAlignment)
##Misc. Functions:
##4.1) send emails (Email class)
##4.2) Print GPIB connections (showResources() function)
##4.3) 1D liveplotting (livePlotting() function)
##EXAMPLE OF USE:######################################################################
##EX. 1 - READ POWER FROM POWER METER IN SLOT 3 OF AGILENT AND PRINT IT
#   import PIC_lab_control
#   LMS1 = PIC_lab_control.LMS_AGILENT_8164B()
#   Pout = LMS1.ReadPower0()
#   print(Pout)
#   LMS1.CloseConnection()
##EX. 2 - SWEEP WITH Sweep2D CLASS. SWEEPING SIGNAL GENERATOR POWER (SG_RS_SMF100A) 
#         OUTPUT POWER AND READING POWER METER (LMS_AGILENT_8164B)
#   import PIC_lab_control
#   SG1 = PIC_lab_control.SG_RS_SMF100A()
#   LMS1 = PIC_lab_control.LMS_AGILENT_8164B()
#   PowerIN=[-20,-19,-18,-17,-16,-15]
#   SWEEP0 = PIC_lab_control.Sweep2D(sweepPar=PowerIN, SetFunction=SG1.SetPower,..
#            ..GetFunction=LMS1.ReadPower, timeFromSetToGet=0.5,..
#            ..setLabels='POWER_IN [dBm]', getLabels=['POWER_OUT [dBm]'])
#   SWEEP0.Run(plotting=True)
#   SWEEP0.SaveAllTxt(sweepName = 'POWER_OUT_vs_POWER_I')
#   ESA1.CloseConnection()
#   SG1.CloseConnection()
##EX. 3 -Send and recieve emails (with pictures)
#      test=PIC.Email("MyEMAIL@eng.au.dk")
#      test.sendMail("Subject","Body text","C:/Users/Me/Downloads/testPic1.png",/
#                                          "C:/Users/Me/Downloads/testPic2.png")
#
# EX. 4 -Live plotting example
#        import piclab as pic
#        import numpy as npy
#        i=0
#        x=npy.array([])
#        y=npy.array([])
#        while 1:
#            i+=1
#            x=npy.append(x,i)
#            y=npy.append(y,i*i)
#            plt=pic.liveplotting(x,y)
#            if i== 20: break
#######################################################################################
#######################CODE:###########################################################
#######################################################################################

# Import relevant packages:
# import visa
import pyvisa as visa
import numpy as np
import time
import matplotlib as Plot
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.animation as animation
import os, os.path
import PyDAQmx  # requires nidaqmx # Not Found
from PyDAQmx import Task
import socket
import re
import paramiko  # pip install paramiko #ISSUES WHEN USING VISUAL STUDIO CODE IDE =>COMMENT
import email  # <-For e-mailing
import smtplib  # <-For e-mailing
from email.message import EmailMessage  # <- For e-mailing
import imghdr  # <- For e-mailing
from tqdm import tqdm  # used for progress bars
import sys  # allows stopping the entire runtime
import serial
# from bitstring import BitArray
import math
# from TLPM import TLPM #TLPM added at end of file instead
# os.add_dll_directory(r'C:\Program Files\IVI Foundation\VISA\Win64\Bin')
from ctypes import cdll, c_long, c_ulong, c_uint32, byref, create_string_buffer, c_bool, c_char_p, c_int, c_int16, \
    c_double, sizeof, c_voidp

import nest_asyncio
import toptica.lasersdk.dlcpro.v2_4_0 as toptica


# Create a class for driving each instrument#############################################

# ELECTRICAL SPECTRUM ANALYZERS:#
class ESA_RS_FSV30:  # developer: Lars Nielsen <<!!!please use 192.168.1.100 for R&S®FSW50!!!>>

    def __init__(self, channel=20, GPIB_interface=-1, IP_address='192.168.1.7', spanFreq=1000, centerFreq=15000,
                 videoBW=0.01, resolutionBW=1, dataPointsInSweep=20001):
        self.channel = channel
        rm = visa.ResourceManager()
        if GPIB_interface > -1:  # Set GPIB_interface=0 to use GPIB instead of TCP/IP
            resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        else:
            resourceName = 'TCPIP0::' + IP_address + '::inst0::INSTR'

        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        self.instr.timeout = 10000
        if alive != 0:
            print('ESA_RS_FSV is alive')
            print(alive)

        self.spanFreq = spanFreq
        self.centerFreq = centerFreq
        self.videoBW = videoBW
        self.resolutionBW = resolutionBW
        self.dataPointsInSweep = dataPointsInSweep
        # self.instr.write('*RST')                                #Reset
        self.instr.write('SYST:DISP:UPD ON')  # Show on ESA display as well
        self.instr.write('INIT:CONT OFF')  # Single sweep
        self.instr.write('BAND:AUTO OFF')
        self.instr.write('BAND:VID:AUTO OFF')

    def SetSpectrumParameters(self, spanFreq=1000, centerFreq=15000, videoBW=0.01, resolutionBW=1,
                              dataPointsInSweep=20001):
        self.spanFreq = spanFreq
        self.centerFreq = centerFreq
        self.videoBW = videoBW
        self.resolutionBW = resolutionBW
        self.dataPointsInSweep = dataPointsInSweep

    def ReadSpectrum(self):
        self.instr.clear()
        self.instr.write('FREQ:CENT ' + str(self.centerFreq) + ' MHz')  # Center frequency
        self.instr.write('FREQ:SPAN ' + str(self.spanFreq) + ' MHz')  # Frequency span
        self.instr.write('BAND ' + str(self.resolutionBW) + ' MHz')  # Resolution bandwidth
        self.instr.write('BAND:VID ' + str(self.videoBW * 1000) + ' kHz')  # Video bandwidth
        self.instr.write('SWE:POIN ' + str(int(self.dataPointsInSweep)))  # Number of data points in sweep

        self.instr.write('INIT')  # Start frequency sweep
        self.instr.query('*OPC?')  # Wait until

        dataOut = np.array(self.instr.query_binary_values('FORM REAL,32;:TRAC? TRACE1'))
        freqAxis = (10 ** 6) * np.arange(self.centerFreq - self.spanFreq / 2, self.centerFreq + self.spanFreq / 2,
                                         self.spanFreq / len(dataOut))  # Generate corresponding frequency axis

        return [dataOut.tolist(),
                freqAxis.tolist()]  # Return x and y values, corresponding to frequency and power/res respectively

    def ReadPeakPower(self, Nread=5):
        power = []
        for x in range(
                Nread):  # Make "N" sweeps to make sure that no "dead" readouts are happening due to the instability of the heterodyne system.
            time.sleep(0.2)
            self.instr.clear()
            self.instr.write('FREQ:CENT ' + str(self.centerFreq) + ' MHz')  # Center frequency
            self.instr.write('FREQ:SPAN ' + str(self.spanFreq) + ' MHz')  # Frequency span
            self.instr.write('BAND ' + str(self.resolutionBW) + ' MHz')  # Resolution bandwidth
            self.instr.write('BAND:VID ' + str(self.videoBW * 1000) + ' kHz')  # Video bandwidth
            self.instr.write('SWE:POIN ' + str(int(self.dataPointsInSweep)))  # Number of data points in sweep

            self.instr.write('INIT')  # Start frequency sweep
            self.instr.query('*OPC?')  # Wait until

            dataOut = np.array(self.instr.query_binary_values('FORM REAL,32;:TRAC? TRACE1'))
            power.append(np.max(dataOut))  # Record the maximum point on all 5 sweeps
        powermax = np.max(power)  # Only pass on the maximum of the 5 peak values found
        return float(powermax)  # Return only the power value of the maximum within the sweep

    def ReadSpectrumPN(self):
        self.instr.clear()
        self.instr.write('INST:SEL PNO')
        self.instr.write('FREQ:STAR 10kHZ')
        self.instr.write('FREQ:STOP 1GHZ')
        self.instr.write('SWE:MODE NORM')
        self.instr.write('FREQ:TRAC ON')
        # self.instr.query_binary_values('FETC:PNO2:RPM?')

        self.instr.query('INIT;*WAI')  # Start frequency sweep
        # self.instr.query('*OPC?')                               #Wait until

        dataOut = np.array(self.instr.query_binary_values('FORM REAL,32;:TRAC? TRACE1'))
        freqAxis = (10 ** 6) * np.arange(self.centerFreq - self.spanFreq / 2, self.centerFreq + self.spanFreq / 2,
                                         self.spanFreq / len(dataOut))  # Generate corresponding frequency axis

        return [dataOut.tolist(),
                freqAxis.tolist()]  # Return x and y values, corresponding to frequency and power/res respectively

    def CloseConnection(self):
        self.instr.close()


# QUASI-DC CURRENT/VOLTAGE SOURCES:#
class DC_PRO8000:  # developer: Andreas Hänsel

    def __init__(self, channel=10, slot=1, GPIB_interface=0):
        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        if alive != 0:
            print('Thorlabs PRO8000 is alive')
            print(alive)
        self.slot = slot;
        self.instr.write(':SLOT ' + str(int(slot)));
        print('Active slot: ' + str(int(slot)));
        # print(self.instr.query(":TYPE:ID?"))

    def SetSlot(self, slot=1):
        self.slot = slot;
        self.instr.write(':SLOT ' + str(int(self.slot)));

    def SetTemperature(self, Celsius=15):
        self.instr.write(':SLOT ' + str(int(self.slot)));  # line needed if multiple slots of device are used
        self.instr.write(':TEMP:SET ' + str(Celsius));

    def GetTemperature(self):
        self.instr.write(':SLOT ' + str(int(self.slot)));  # line needed if multiple slots of device are used
        QueryString = self.instr.query(':TEMP:ACT?')
        return float(QueryString.split()[-1])  # string -> float

    def SetCurrent(self, current=0):  # unit: A
        self.instr.write(':SLOT ' + str(int(self.slot)));  # line needed if multiple slots of device are used
        self.instr.write(':ILD:SET ' + str(current));
        QueryString = self.instr.query(":LIMCP:ACT?")
        MaxCurrentHardware = float(QueryString.split()[-1])
        QueryString = self.instr.query(":LIMC:SET?")
        MaxCurrentSoftware = float(QueryString.split()[-1])
        if (current > MaxCurrentSoftware):
            print('Set Current higher than software limit. ILIM = ' + str(MaxCurrentSoftware))
        else:
            if (current > MaxCurrentHardware):
                print('Set Current higher than software limit. IMAX = ' + str(MaxCurrentHardware))

    def SetCurrentFast(self, current=0):  # unit: A
        self.instr.write(':ILD:SET ' + str(current));

    def GetVoltage(self):  # unit: V
        self.instr.write(':SLOT ' + str(int(self.slot)));  # line needed if multiple slots of device are used
        QueryString = self.instr.query(':VLD:ACT?');
        return float(QueryString.split()[-1])  # string -> float

    def SetCurrentLimit(self, current=0.2):  # unit: A
        self.instr.write(':SLOT ' + str(int(self.slot)));  # line needed if multiple slots of device are used
        self.instr.write(':LIMC:SET ' + (str(current)))

    def GetPID(self):
        Pstr = self.instr.query(':SHAREP:SET?');
        P = float(Pstr.split()[-1])
        Istr = self.instr.query(':SHAREI:SET?');
        I = float(Istr.split()[-1])
        Dstr = self.instr.query(':SHARED:SET?');
        D = float(Dstr.split()[-1]);
        print('PID values:');
        print();
        print(P);
        print(I);
        print(D);
        PID = dict();
        PID['P'] = P;
        PID['I'] = I;
        PID['D'] = D;
        return PID

    def SetPID(self, P=80.0, I=2.5, D=30.25):
        self.instr.write(':SHAREP:SET ' + str(P));
        self.instr.write(':SHAREI:SET ' + str(I));
        self.instr.write(':SHARED:SET ' + str(D));

    def SetPIDdict(self, dictionary):
        P = dictionary['P'];
        I = dictionary['I'];
        D = dictionary['D'];
        self.SetPID(P, I, D);

    def WriteGPIB(self, string):
        self.instr.write(string);

    def QueryGPIB(self, string):
        return self.instr.query(string);

    def CloseConnection(self):
        self.instr.close()


class DC_KEITHLEY_GRAPH:  # developer: Peter Tønning. adabted to Keithley 2450 commands, main difference in compliance (Now limit: ILIM/VLIM) and "FORM" class (https://www.tek.com/keithley-source-measure-units/keithley-smu-2400-series-sourcemeter-manual/model-2450-interactive-sou)
    # Ethernet interface added by Lars
    def __init__(self, channel=17, GPIB_interface=-1, IP_address='192.168.1.32'):
        self.Meas = 'Volt';
        self.Source = 'Current'

        self.channel = channel
        rm = visa.ResourceManager()
        if GPIB_interface < 0:
            resourceName = 'TCPIP0::' + IP_address + '::inst0::INSTR'
        else:
            resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        self.instr.timeout = 100000
        if alive != 0:
            print('Keithley is alive')
            print(alive)
        #:OUTP ON
        self.IsOn = int(self.instr.query(':OUTP?'));
        if self.IsOn == 1:
            print('Source output is ON');
        else:
            if self.IsOn == 0:
                print('Source output is OFF');

    def SwitchOn(self):
        if self.instr.query(':OUTP?') != 1:
            self.instr.write(':OUTP ON');
            print('Source output turned ON');
            self.IsOn = 1;
        else:
            print('Source output was already ON');

    def SwitchOff(self):
        if self.instr.query(':OUTP?') != 0:
            self.instr.write(':OUTP OFF');
            print('Source output turned OFF');
            self.IsOn = 0;
        else:
            print('Source output was already OFF');

    def SetMeasCurr(self):
        self.instr.write(":SENS:FUNC 'CURR'");
        # self.instr.write(":FORM:ELEM CURR");
        self.Meas = 'Current';

    def SetMeasVolt(self):
        self.instr.write(":SENS:FUNC 'VOLT'");
        # self.instr.write(":FORM:ELEM VOLT");
        self.Meas = 'Volt';

    def SetSourceVolt(self):
        self.instr.write('SOUR:FUNC VOLT')
        self.Source = 'Volt';

    def SetSourceValue(self, Value):
        if (self.Source == 'Volt'):
            # self.instr.write('SOUR1:VOLT '+str(Value))
            self.instr.write('SOUR:VOLT ' + str(Value))
        else:
            if (self.Source == 'Current'):
                self.instr.write('SOUR:CURR ' + str(Value))  # not tested

    def SetSourceCurr(self):
        self.instr.write('SOUR:FUNC CURR')
        self.Source = 'Current';

    def SetCompliance(self, Compliance=0.05):
        # so far compliance is based on measured value; could be changed later

        if (self.Source == 'Current'):
            self.instr.write(':SOUR:CURR:VLIM ' + str(Compliance))
        else:
            if (self.Source == 'Volt'):
                self.instr.write(':SOUR:VOLT:ILIM ' + str(Compliance))
            else:
                print('Measurement function undefined');

    def GetMeas(self):
        if (self.Meas == 'Current'):
            # self.instr.write(":FORM:ELEM 'CURR'");
            Value = float((self.instr.query_ascii_values('READ?'))[0]);
        else:
            if (self.Meas == 'Volt'):
                # self.instr.write(":FORM:ELEM 'VOLT'");
                Value = float((self.instr.query_ascii_values('READ?'))[0]);
            else:
                print('Measurement function undefined');
                Value = 0;
        return Value;

    def WriteGPIB(self, string):
        self.instr.write(string);

    def QueryGPIB(self, string):
        return self.instr.query(string);

    def CloseConnection(self):
        self.instr.close()


class DC_KEITHLEY:  # developer: Andreas Hänsel + functionalities added by Hanna Becker (SetIntegrationtime, GetIntegrationtime;SetMode, GetMode, SetWire, GetWire)

    def __init__(self, channel=21, GPIB_interface=0):
        self.Meas = 'Volt';
        self.Source = 'Current'

        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        self.instr.timeout = 10000
        if alive != 0:
            print('Keithley is alive')
            print(alive)
        #:OUTP ON
        self.IsOn = int(self.instr.query(':OUTP?'));
        if self.IsOn == 1:
            print('Source output is ON');
        else:
            if self.IsOn == 0:
                print('Source output is OFF');

    def SwitchOn(self):
        if self.instr.query(':OUTP?') != 1:
            self.instr.write(':OUTP ON');
            print('Source output turned ON');
            self.IsOn = 1;
        else:
            print('Source output was already ON');

    def SwitchOff(self):
        if self.instr.query(':OUTP?') != 0:
            self.instr.write(':OUTP OFF');
            print('Source output turned OFF');
            self.IsOn = 0;
        else:
            print('Source output was already OFF');

    def SetMeasCurr(self):
        self.instr.write(":SENS:FUNC 'CURR'");
        self.instr.write(":FORM:ELEM CURR");
        self.Meas = 'Current';

    def SetMeasVolt(self):
        self.instr.write(":SENS:FUNC 'VOLT'");
        self.instr.write(":FORM:ELEM VOLT");
        self.Meas = 'Volt';

    def SetSourceVolt(self):
        self.instr.write('SOUR:FUNC:MODE VOLT')
        self.Source = 'Volt';

    def SetSourceValue(self, Value):
        if (self.Source == 'Volt'):
            # self.instr.write('SOUR1:VOLT '+str(Value))
            self.instr.write('SOUR:VOLT ' + str(Value))
        else:
            if (self.Source == 'Current'):
                self.instr.write('SOUR:CURR ' + str(Value))  # not tested

    def SetSourceCurr(self):
        self.instr.write('SOUR:FUNC:MODE CURR')
        self.Source = 'Current';

    def SetCompliance(self, Compliance=0.05):
        # so far compliance is based on measured value; could be changed later
        if (self.Meas == 'Current'):
            self.instr.write('SENS:CURR:PROT ' + str(Compliance))
        else:
            if (self.Meas == 'Volt'):
                self.instr.write('SENS:VOLT:PROT ' + str(Compliance))
            else:
                print('Measurement function undefined');

    def GetMeas(self):
        if (self.Meas == 'Current'):
            # self.instr.write(":FORM:ELEM 'CURR'");
            Value = float((self.instr.query_ascii_values('READ?'))[0]);
        else:
            if (self.Meas == 'Volt'):
                # self.instr.write(":FORM:ELEM 'VOLT'");
                Value = float((self.instr.query_ascii_values('READ?'))[0]);
            else:
                print('Measurement function undefined');
                Value = 0;
        return Value;

    def WriteGPIB(self, string):
        self.instr.write(string);

    def QueryGPIB(self, string):
        return self.instr.query(string);

    def CloseConnection(self):
        self.instr.close()

    def SetMode(self, mode_string):
        # set 'Voltage' for voltage source, measure current
        # set 'Current for current source, measure voltage
        # ATTENTION: this setting includes a full reset and resets the compliance levels each time used!!!
        if mode_string == 'Voltage':
            # initialization of Keithley:
            self.instr.write("*RST;*CLS;*SRE 32;*ESE 1")  # reset etc
            print("The current limit will be set to 0.010A.")
            print("The voltage limit will be set to 20V.")
            self.instr.write('SENS:CURR:PROT 0.01')
            self.instr.write('SENS:VOLT:PROT 20')
            self.instr.write(":SYST:RSEN OFF")  # set 2 wire sensing
            self.instr.write(":SOUR:FUNC VOLT")
            print(
                "The machine has been set to 2-wire (2-probe) sensing, change this by typing myInstrument.SetWire = 'Four'")
            print("The machine has been set to VOLTAGE mode, change this by typing myInstrument.SetMode = 'Current'")
            print("---------------------------------------------------------------")
            self.instr.write(":SOUR:VOLT:MODE FIX")
            self.instr.write(':SENS:FUNC "CURR" ')
            self.instr.write(":FORM:ELEM CURR");
            self.Source = 'Volt'
            self.Meas = 'Current'

        elif mode_string == 'Current':
            # initialization of Keithley:
            self.instr.write("*RST;*CLS;*SRE 32;*ESE 1")  # reset etc
            print("The current limit will be set to 0.010A.")
            print("The voltage limit will be set to 20V.")
            self.instr.write('SENS:CURR:PROT 0.01')
            self.instr.write('SENS:VOLT:PROT 20')
            self.instr.write(":SYST:RSEN OFF")  # set 2 wire sensing
            self.instr.write(":SOUR:FUNC CURR")
            print(
                "The machine has been set to 2-wire (2-probe) sensing, change this by typing myInstrument.SetWire = 'Four'")
            print("The machine has been set to CURRENT mode, change this by typing myInstrument.SetMode = 'Voltage'")
            print("---------------------------------------------------------------")
            self.instr.write(":SOUR:CURR:MODE FIX")  # Fixed current source mode
            self.instr.write(':SENS:FUNC "VOLT" ')  # Volts measure function
            self.instr.write(":FORM:ELEM VOLT");
            self.Source = 'Current'
            self.Meas = 'Volt'
        else:
            AttributeError(
                "Got invalid reponse for mode of the instrument: requires 'Voltage' or 'Current' but got %s" % str(
                    mode_string))

    def GetMode(self):
        return self.Source

    def SetWire(self, wire):
        if wire == None:
            self.instr.write(":SYST:RSEN OFF")
        elif wire == 'Two':
            self.instr.write(":SYST:RSEN OFF")
            self.__wire__ = 'Two'
        elif wire == 'Four':
            if self.Source == 'Volt':
                print(
                    "4-wire sensing possible only with 'Current' mode. Change mode from 'Voltage' to 'Current'. Now executing 2-wire sensing.")
            elif self.Source == 'Current':
                self.instr.write(":SYST:RSEN ON")
                self.__wire__ = 'Four'
                print("Sensing set by user as 4-wire. Resetting machine to 4-wire sensing")
        else:
            AttributeError(
                "Got invalid reponse for mode of the instrument: requires 'Two' or 'Four' but got %s" % str(wire))

    def GetWire(self):
        return self.__wire__

    def SetIntegrationtime(self, int_time=1.00):
        #  integration time is specified in parameters based on the number of power line cycles (NPLC)
        # FAST — Sets speed to 0.01 PLC and sets display resolution to 3½ digits.
        # MED — Sets speed to 0.10 PLC and sets display resolution to 4½ digits.
        # NORMAL — Sets speed to 1.00 PLC and sets display resolution to 5½ digits.
        # HI ACCURACY — Sets speed to 10.00 PLC and sets display resolution to 6½digits.
        # OTHER — Use to set speed to any PLC value from 0.01 to 10
        if (self.Meas == 'Current'):
            self.instr.write(":SENS:CURR:NPLC %g" % int_time)
        else:
            self.instr.write(":SENS:VOLT:NPLC %g" % int_time)
        self.__integtime__ = int_time

    def GetIntegrationtime(self):
        return self.__integtime__


class DC_NI_cDAQ:  # developer: Andreas

    def __init__(self, aochannel=0, Device='cDAQ1Mod1'):
        self.PhysicalAddress = '/' + Device + '/ao' + str(aochannel);
        self.task = Task();
        MinV = -10.0;
        MaxV = 10.0;  # limits for NI 9264
        self.task.CreateAOVoltageChan(self.PhysicalAddress, "A" + str(aochannel), MinV, MaxV, PyDAQmx.DAQmx_Val_Volts,
                                      None)
        self.task.StartTask()

    def SetV(self, value=0):
        self.task.WriteAnalogScalarF64(1, 10.0, value, None)

    def SetReverseBias(self, value=0):
        self.SetV(-abs(value))

    def CloseConnection(self):
        value = 0;
        self.task.WriteAnalogScalarF64(1, 10.0, value, None)
        self.task.StopTask();

    # SIGNAL GENERATORS:#


class SG_RS_SMF100A:  # developer: Lars Nielsen

    def __init__(self, channel=9, GPIB_interface=0):
        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        if alive != 0:
            print('SG_RS_SMF100A is alive')
            print(alive)

        self.instr.write('FREQ:MODE CW')

    def SetFrequency(self, freq=10000):  # Frequency in MHz
        self.instr.write('FREQ ' + str(freq) + 'MHz')  # Set RF frequency

    def SetPower(self, power_dBm=-20):
        self.instr.write('SOUR:POW:POW ' + str(power_dBm))  # Set RF power

    def Output(self, ON=0):
        if ON == 1:
            self.instr.write('OUTP ON')  # Turn ON
        elif ON == 0:
            self.instr.write('OUTP OFF')  # TURN OFF

    def CloseConnection(self):
        self.instr.close()


# LIGHTWAVE MEASUREMENT SYSTEMS:#
class LMS_AGILENT_8164B:  # developer: Lars Nielsen, Mads Larsen, Andreas Hänsel

    def __init__(self, channel=18, slot=[3, 4], channelInSlot=1, GPIB_interface=0, SourceSlot=2):
        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        self.instr.timeout = 60000
        if alive != 0:
            print('LMS_AGILENT_8164B is alive')
            print(alive)

        self.slot = slot
        self.channelInSlot = channelInSlot
        self.SourceSlot = SourceSlot

        self.lambdaArr = []

    # Power Meter
    def SetContinuous0(self, mode='On'):
        if isinstance(self.slot, list):
            slotTemp = self.slot[0]
        else:
            slotTemp = self.slot

        if (mode == 'On' or mode == 'on' or mode == 'ON' or mode == 1):
            self.instr.write('init' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':cont 1')
        elif (mode == 'Off' or mode == 'off' or mode == 'OFF' or mode == 0):
            self.instr.write('init' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':cont 0')
        else:
            print('Unknown state for continuous mesurement setting')

    def SetContinuous1(self, mode='On'):
        if isinstance(self.slot, list):
            slotTemp = self.slot[1]
        else:
            slotTemp = self.slot

        if (mode == 'On' or mode == 'on' or mode == 'ON' or mode == 1):
            self.instr.write('init' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':cont 1')
        elif (mode == 'Off' or mode == 'off' or mode == 'OFF' or mode == 0):
            self.instr.write('init' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':cont 0')
        else:
            print('Unknown state for continuous mesurement setting')

    def ReadPower0(self):
        if isinstance(self.slot, list):
            slotTemp = self.slot[0]
        else:
            slotTemp = self.slot

        self.instr.write('trig3:inp ign')  # Set power meter 3 to act on trigger

        self.instr.write('init' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':imm')
        powerOut = self.instr.query_ascii_values('fetc' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':pow?')
        return float(powerOut[0])

    def ReadPowerLong0(self):
        # Regular read power leads to timeout exception when integration time is too long,
        # but the additional query of ReadPowerLong slows down operation where this does not matter
        if isinstance(self.slot, list):
            slotTemp = self.slot[0]
        else:
            slotTemp = self.slot
        wait = self.GetAveragingTime0() - 0.1;
        self.instr.write('init' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':imm')
        time.sleep(wait);
        powerOut = self.instr.query_ascii_values('fetc' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':pow?')
        return float(powerOut[0])

    def ReadPowerLong1(self):
        # Regular read power leads to timeout exception when integration time is too long,
        # but the additional query of ReadPowerLong slows down operation where this does not matter
        if isinstance(self.slot, list):
            slotTemp = self.slot[1]
        else:
            slotTemp = self.slot
        wait = self.GetAveragingTime0() - 0.1;
        self.instr.write('init' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':imm')
        time.sleep(wait);
        powerOut = self.instr.query_ascii_values('fetc' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':pow?')
        return float(powerOut[0])

    def ReadPower1(self):
        if isinstance(self.slot, list):
            slotTemp = self.slot[1]
        else:
            slotTemp = self.slot

        self.instr.write('trig4:inp ign')  # Set power meter 4 to act on trigger

        self.instr.write('init' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':imm')
        powerOut = self.instr.query_ascii_values('fetc' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':pow?')
        return float(powerOut[0])

    def ReadPower0Array(self):
        if isinstance(self.slot, list):
            slotTemp = self.slot[0]
        else:
            slotTemp = self.slot

        # print(self.instr.query('sens'+str(slotTemp)+':func:res?'))
        # powerArr = self.instr.query_ascii_values('sens'+str(slotTemp)+':func:res?')
        # waveArr = self.instr.query_ascii_values('sour'+str(self.SourceSlot)+':read:data? llog')#placeholder for WL array
        powerArr = self.instr.query_binary_values('sens' + str(slotTemp) + ':func:res?', datatype='f',
                                                  is_big_endian=False)
        waveArr = self.lambdaArr  # self.instr.query_binary_values('sour'+str(self.SourceSlot)+':read:data? llog')#placeholder for WL array
        return [powerArr, waveArr]

    def ReadPower1Array(self):
        if isinstance(self.slot, list):
            slotTemp = self.slot[1]
        else:
            slotTemp = self.slot

        # powerArr = self.instr.query_ascii_values('sens'+str(slotTemp)+':chan'+str(self.channelInSlot)+':func:res?')
        powerArr = self.instr.query_binary_values('sens' + str(slotTemp) + ':func:res?', datatype='f',
                                                  is_big_endian=False)
        waveArr = self.lambdaArr  # self.instr.query_binary_values('sour'+str(self.SourceSlot)+':read:data? llog')#placeholder for WL array
        # waveArr=self.instr.query_binary_values('sour'+str(self.SourceSlot)+':read:data? llog')#placeholder for WL array
        return [powerArr, waveArr]

    def ReadWLArray(self):
        return [self.lambdaArr, self.lambdaArr]

    def SetReadWL0(self, Value):  # Sets measured wavelength
        if isinstance(self.slot, list):
            slotTemp = self.slot[0]
        else:
            slotTemp = self.slot
        self.instr.write(':SENS' + str(int(slotTemp)) + ':pow:wav ' + str(Value) + 'NM');

    def SetReadWL1(self, Value):  # Sets measured wavelength
        if isinstance(self.slot, list):
            slotTemp = self.slot[1]
        else:
            slotTemp = self.slot
        self.instr.write(':SENS' + str(int(slotTemp)) + ':pow:wav ' + str(Value) + 'NM');

    def GetAveragingTime0(self):
        if isinstance(self.slot, list):
            slotTemp = self.slot[0]
        else:
            slotTemp = self.slot
        atime = self.instr.query('sens' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':pow:atim?')
        return float(atime)

    def GetAveragingTime1(self):
        if isinstance(self.slot, list):
            slotTemp = self.slot[1]
        else:
            slotTemp = self.slot
        atime = self.instr.query('sens' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':pow:atim?')
        return float(atime)

    def SetAveragingTime0(self, seconds=0.2):
        # only allows certain standard values; device rounds automatically
        # allowed values: 100e-6, 200e-6, 500e-6, 1e-3, ..... ,10
        if isinstance(self.slot, list):
            slotTemp = self.slot[0]
        else:
            slotTemp = self.slot
        self.instr.write('sens' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':pow:atim ' + str(seconds));

    def SetAveragingTime1(self, seconds=0.2):
        # only allows certain standard values; device rounds automatically
        # allowed values: 100e-6, 200e-6, 500e-6, 1e-3, ..... ,10
        if isinstance(self.slot, list):
            slotTemp = self.slot[1]
        else:
            slotTemp = self.slot
        self.instr.write('sens' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':pow:atim ' + str(seconds));

        # Laser

    def LaserON(self):
        self.instr.write('SOUR' + str(int(self.SourceSlot)) + ':POWer:STATe 1')
        print('Agilent Laser: ON')

    def LaserOFF(self):
        self.instr.write('SOUR' + str(int(self.SourceSlot)) + ':POWer:STATe 0')
        print('Agilent Laser: OFF')

    def GetLaserState(self):
        LaserState = self.instr.query('SOUR' + str(int(self.SourceSlot)) + ':POWer:STATe?')
        LaserState = int(LaserState)
        if LaserState == 1:
            print('Agilent Laser: ON')
            return 1;
        elif LaserState == 0:
            print('Agilent Laser: OFF')
            return 0;
        else:
            print('Agilent Laser state unknown')

    def LaserCW(self):  # Set CW mode
        self.instr.write('INIT' + str(int(self.SourceSlot)) + ':CONT 1')

    def SetLaserWL(self, Value):  # nm
        self.instr.write(':SOURce' + str(int(self.SourceSlot)) + ':WAVe ' + str(Value) + 'NM')

    def SetLaserPower(self, Value):  # mW
        self.instr.write('SOUR' + str(int(self.SourceSlot)) + ':POW ' + str(Value) + 'MW')  # Set Laser Power  [mW]

    #### <untested>       #Modulation and sweeps
    def GetCoherenceLevel(self):  # in percent; 100% corresponds to minimum linewidth, 0% maximum lw.
        return self.instr.query(':SOURce' + str(int(self.SourceSlot)) + ':AM:COHCtrl:COHLevel?')

    def SetCoherenceLevel(self, Value=98):  # in percent; between 1 and 99.8, or 'MIN', 'MAX', 'DEF'
        self.instr.write(':SOURce' + str(int(self.SourceSlot)) + ':AM:COHCtrl:COHLevel ' + str(Value))

    def AmplitudeModulationOFF(self):
        self.instr.write(':SOURce' + str(int(self.SourceSlot)) + ':AM:STATe 0')
        # 0 = 'OFF'

    def AM_OFF(self):
        self.AmplitudeModulationOFF();  # redundancy for different calls

    def AMoff(self):
        self.AmplitudeModulationOFF();  # redundancy for different calls

    def AmplitudeModulationON(self):
        self.instr.write(':SOURce' + str(int(self.SourceSlot)) + ':AM:STATe 1')
        # 1 = 'ON'

    def AM_ON(self):
        self.AmplitudeModulationON();  # redundancy for different calls

    def AMon(self):
        self.AmplitudeModulationON();  # redundancy for different calls

    def GetAmplitudeModulationState(self):
        return self.instr.query(':SOURce' + str(int(self.SourceSlot)) + ':AM:STATe?')
        # 1 = 'ON', 0 = 'OFF'

    def GetAM_State(self):
        return self.GetAmplitudeModulationState();

    def GetAMstate(self):
        return self.GetAmplitudeModulationState();

    def SetAMstate(self, state):
        if (state == 1 or state == 'on' or state == 'ON' or state == 'On'):
            self.AmplitudeModulationON()
        elif (state == 0 or state == 'off' or state == 'OFF' or state == 'Off'):
            self.AmplitudeModulationOFF()
        else:
            print('Unknown AM state')

    def SetAMfrequency(self, Value=1e3, Unit='HZ'):  # sets frequency for amplitude modulation
        # THZ|GHZ|MHZ|KHZ|HZ
        self.instr.write(':SOURce' + str(int(self.SourceSlot)) + ':AM:FREQuency ' + str(Value) + Unit);

    def SetAmplitudeModulationFrequency(self, Value=10, Unit='KHZ'):
        self.SetAMfrequency(Value, Unit);

    def SetAM_Frequency(self, Value=10, Unit='KHZ'):
        self.SetAMfrequency(Value, Unit);

    def GetAM_Frequency(self):  # AM frequency in Hertz
        return self.instr.query(':SOURce' + str(int(self.SourceSlot)) + ':AM:FREQuency?');

    def GetAMfrequency(self):
        return self.GetAM_Frequency();

    def GetAmplitudeModulationFrequency(self):
        return self.GetAM_Frequency();

    def GetAM_Type(self):
        answer = self.instr.query(':SOURce' + str(int(self.SourceSlot)) + ':AM:sour?')
        if (answer == 0):
            print('Internal Amplitude modulation')
        elif (answer == 1):
            print('Coherence Control')
        else:
            print('Mode not supported by PIC_lab_control')
        return answer;

    def GetAmplitudeModulationType(self):
        return self.GetAM_Type()

    def GetAMtype(self):
        return self.GetAM_Type()

    def SetAM_Type(self, Value=0):
        self.instr.write('sour' + str(int(self.SourceSlot)) + ':am:sour ' + str(int(Value)));
        # 0:internal  1:coherence control; other modes not yet supported

    def SetAMtype(self, Value=0):
        self.SetAM_Type(Value);

    def SetAmplitudeModulationType(self, Value=0):
        self.SetAM_Type(Value);

    def SetCoherenceControl(self):  # Sets AM Modulation to coherence control
        self.SetAM_Type(1);

    def SetInternalAM(self):  # Sets AM modulation to internal modulation
        self.SetAM_Type(0);

    #### </untested>

    def StepSweep(self, Power=10, StartWL=1540, StopWL=1560, Steps=1001, DwellTime=0.2, Cycles=1, SweepMode='oneway'):
        # power in mW, WL in nm, DwellTime in secs; Cycles=0 for infinite
        self.SetLaserPower(Power);
        self.SetLaserWL(StartWL);
        self.LaserON();
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:MODE STEP')
        if (SweepMode == 'oneway') or (SweepMode == 'ONEWAY') or (SweepMode == 'Oneway') or (SweepMode == 'OneWay')(
                SweepMode == 1):
            self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:REP ONEW')
        elif (SweepMode == 'twoway') or (SweepMode == 'TWOWAY') or (SweepMode == 'Twoway') or (SweepMode == 'TwoWay')(
                SweepMode == 2):
            self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:REP TWOW')
        else:
            print('Unknown sweep mode');
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:STAR ' + str(StartWL) + 'NM');
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:STOP ' + str(StopWL) + 'NM');
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:DWELl ' + str(DwellTime));
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:CYCLes ' + str(int(Cycles)));
        StepWidth = (StopWL - StartWL) / (Steps - 1);
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:STEP ' + str(StepWidth) + 'NM');
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE STart')  # start the sweep
        self.LaserOFF();

    def StopSweep(self):
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE STOP')

    def GetWLScan(self, StartWL=1540, StopWL=1560, SweepSpeed=20, Cycles=1, stepWidthNM=1, SweepMode='oneway'):

        # Speed=int(round((StopWL-StartWL)/SweepTime)); #in nm/s
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:SPE ' + str(SweepSpeed) + 'NM/S')
        # self.instr.write(':SOUR'+str(int(self.SourceSlot))+':WAV:SWE:SPE 50NM/S')
        # self.instr.write(':SOUR'+str(int(self.SourceSlot))+':WAV:SWE:DWEL 2MS')
        #
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:REP ONEW')
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:LLOG 1')
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:STEP ' + str(stepWidthNM) + 'NM')
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:STAR ' + str(StartWL) + 'NM');
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:STOP ' + str(StopWL) + 'NM');
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:CYCLes ' + str(int(Cycles)));
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:MODE CONT')

        delta_lam = (StopWL - StartWL)
        N_points = round(delta_lam / stepWidthNM)
        self.lambdaArr = [StartWL + (delta_lam / N_points) * i for i in range(N_points + 1)]

        self.instr.write(
            'trig:conf loop')  # Set the trigger to automatically loop between output trigger from laser and input trigger of power modules
        self.instr.write('trig2:outp stf')  # Set each laser WL sweep step to generate an output trigger
        self.instr.write('trig4:inp sme')  # Set power meter 4 to act on trigger
        self.instr.write('trig3:inp sme')  # Set power meter 3 to act on trigger
        self.instr.write('sens3:func:par:logg ' + str(N_points + 1) + ',0.1ms')
        self.instr.write('sens4:func:par:logg ' + str(N_points + 1) + ',0.1ms')
        self.instr.write('sens3:func:stat logg,star')
        self.instr.write('sens4:func:stat logg,star')

        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE STart')

        print('Laser is sweeping...')
        while int(self.instr.query_ascii_values(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE?')[
                      0]):  # wait until sweep is done
            time.sleep(2.0)
        print('Laser sweep stopped...')

        self.lambdaArr = self.instr.query_binary_values('sour' + str(self.SourceSlot) + ':read:data? llog',
                                                        datatype='d', is_big_endian=False)

    def ResetAfterWLScan(self):

        self.instr.write('trig3:inp ign')
        self.instr.write('trig4:inp ign')

        self.instr.write('sens3:pow:atim 0.1s')
        self.instr.write('sens4:pow:atim 0.1s')

    def ContinuousSweep(self, Power=10, StartWL=1540, StopWL=1560, SweepTime=20, Cycles=1, SweepMode='oneway'):
        ##power in mW, WL in nm, SweepTime in secs; Cycles=0 for infinite
        ## The continuous sweep model only works for fixed speeds, which are very fast; use only for sparse data
        self.SetLaserPower(Power);
        self.SetLaserWL(StartWL);
        self.LaserON();
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:MODE CONT')
        if (SweepMode == 'oneway') or (SweepMode == 'ONEWAY') or (SweepMode == 'Oneway') or (SweepMode == 'OneWay')(
                SweepMode == 1):
            self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:REP ONEW')
        elif (SweepMode == 'twoway') or (SweepMode == 'TWOWAY') or (SweepMode == 'Twoway') or (SweepMode == 'TwoWay')(
                SweepMode == 2):
            self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:REP TWOW')
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:STAR ' + str(StartWL) + 'NM');
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:STOP ' + str(StopWL) + 'NM');
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:CYCLes ' + str(int(Cycles)));
        Speed = (StopWL - StartWL) / SweepTime;  # in nm/s
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:SPE ' + str(Speed) + 'NM/S')
        self.instr.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE STart');  # start the sweep
        self.LaserOFF();

    def LineMeasurementSimpleContinuous(self, Power=10, StartWL=1540, StopWL=1560, SweepTime=20, Cycles=1,
                                        DataPoints=101, SweepMode='oneway'):
        ## The continuous sweep model only works for fixed speeds, which are very fast;
        ## The data cannot be captured fast enough by the Agilent; this code will auto-fail
        P0List = np.array([]);
        P1List = np.array([]);
        DataDict = dict();
        DataDict['Error'] = 0;
        PauseTime = SweepTime / (DataPoints - 1);
        self.instr.write('init' + str(self.slot[0]) + ':chan' + str(
            self.channelInSlot) + ':cont 0')  # deactivates automatical power read out
        self.instr.write('init' + str(self.slot[1]) + ':chan' + str(self.channelInSlot) + ':cont 0')
        self.SetAveragingTime0(100e-6);
        self.SetAveragingTime1(100e-6);
        self.ContinuousSweep(Power, StartWL, StopWL, SweepTime, Cycles, SweepMode='oneway');
        for y in range(Cycles):
            print('Cycle ' + str(int(Cycles)))
            for x in tqdm(range(0, DataPoints)):  # progress bar along the sweep
                tic = time.time();
                P0List = np.append(P0List, self.ReadPower0());
                P1List = np.append(P1List, self.ReadPower1());
                toc = time.time();
                diff = toc - tic;
                if (diff < PauseTime):
                    time.sleep(PauseTime - diff);
                else:
                    print('Device too slow; measurement settings too fast!');
                    print(diff);
                    DataDict['Error'] = 1;  # error != 0 indicates error state
                    # break;
        DataDict['P0'] = P0List;
        DataDict['P1'] = P1List;
        DataDict['Wavelength'] = np.linspace(StartWL, StopWL, DataPoints);
        self.instr.write('init' + str(self.slot[0]) + ':chan' + str(
            self.channelInSlot) + ':cont 1')  # reactivates automatical power read out
        self.instr.write('init' + str(self.slot[1]) + ':chan' + str(self.channelInSlot) + ':cont 1')
        return DataDict;

    def LineMeasurementSimpleStep(self, Power=10, StartWL=1550, StopWL=1560, Steps=501, DwellTime=0.75, Cycles=1,
                                  SweepMode='oneway'):
        P0List = np.array([]);
        P1List = np.array([]);
        DataDict = dict();
        DataDict['Error'] = 0;
        PauseTime = DwellTime;
        self.instr.write('init' + str(self.slot[0]) + ':chan' + str(
            self.channelInSlot) + ':cont 0')  # deactivates automatical power read out
        self.instr.write('init' + str(self.slot[1]) + ':chan' + str(self.channelInSlot) + ':cont 0')
        self.SetAveragingTime0(100e-6);
        self.SetAveragingTime1(100e-6);
        self.StepSweep(Power, StartWL, StopWL, Steps, DwellTime, Cycles, SweepMode);
        time.sleep(2.0);  # rough waiting time for startup of measurement;
        # unfortunately this is system-dependent and will lead to systematic errors,
        # but there is no proper return flag in the system
        for y in range(Cycles):
            print('Cycle ' + str(int(Cycles)))
            for x in tqdm(range(0, Steps)):  # progress bar along the sweep
                tic = time.time();
                P0List = np.append(P0List, self.ReadPower0());
                P1List = np.append(P1List, self.ReadPower1());
                toc = time.time();
                diff = toc - tic;
                if (diff < PauseTime):
                    time.sleep(PauseTime - diff);
                else:
                    print('Device too slow; measurement settings too fast!');
                    print(diff);
                    DataDict['Error'] = 1;  # error != 0 indicates error state
                    # break;
        DataDict['P0'] = P0List;
        DataDict['P1'] = P1List;
        DataDict['Wavelength'] = np.linspace(StartWL, StopWL, Steps);
        self.instr.write('init' + str(self.slot[0]) + ':chan' + str(
            self.channelInSlot) + ':cont 1')  # reactivates automatical power read out
        self.instr.write('init' + str(self.slot[1]) + ':chan' + str(self.channelInSlot) + ':cont 1')
        return DataDict;

        # viPrintf(vi,"SENS1:CHAN1:POW:ATIME

    # Others
    def IsReady(self):
        ### Unfortunately, sweeps do not block the ready signal; neither do averaging procedures
        Ret = self.instr.query('*OPC?')
        if (Ret == '1'):
            return True
        elif (Ret == '0'):
            return False
        else:
            print('This should not happen; unknown ready state')

    def IsSweeping(self):
        ## To figure out, whether a sweep is running; sending commands in sweep state may crash the device
        RET = self.instr.query(':SOUR' + str(int(self.SourceSlot)) + ':WAV:SWE:STAT?');
        if (RET == '+1'):
            return True;
        elif (RET == '+0'):
            return False;
        else:
            print('This should not happen; unknown sweep state')

    def WaitForReady(self, WaitTime=0.2, timeout=10, HardStop=False):
        tic = time.time();
        while (self.IsReady() == False):
            time.sleep(WaitTime);
            toc = time.time()
            if (toc - tic > timeout):
                print('Waiting timed out!');
                if (HardStop):
                    sys.exit()
                else:
                    return 1;  # return 1 indicates error
        if (self.IsReady()): print('Device ready')
        return 0;

    def WriteGPIB(self, string):
        self.instr.write(string);

    def QueryGPIB(self, string):
        return self.instr.query(string);

    def CloseConnection(self):
        self.instr.close()


class OSA_YENISTA_OSA20:  # developer: Lars Nielsen, Andreas
    """
    - DESCRIPTION:
        This class is for controlling the Yenista OSA20

        channel : integer
            For choosing the GPIB channel of the GPIB communication.

        GPIB_interface : integer
            For choosing the GPIB interface of the GPIB communication. Set to -1 if ethernet communcation is used instead

        spanWave : float
            The span of the spectrum which is to be read from the instrument. Given in nanometers.

        centerWave : float
            The center wavelength of the spectrum which is to be read from the instrument. Given in nanometers.

        resolutionBW : float
            The resolution of the spectrum which is to be read from the instrument. Given in nanometers.

        sensitivity : int
            Chooses the dynamic sensitivity of the spectrum.
                1: -55 dBm (2000 nm/s)
                2: -60 dBm (700 nm/s)
                3: -65 dBm (200 nm/s)
                4: -70 dBm (20 nm/s)
                5: -75 dBm (2 nm/s)
                6: High (0.5 nm/s)
                7: Burst

        ip_address : string
            Sets the ip address of the TCP IP commuication when ethernet is used.

        tcp_port : integer
            Sets the port of the TCP IP commuication when ethernet is used.
    """

    def __init__(self, channel=16, GPIB_interface=0, spanWave=60, centerWave=1550, resolutionBW=0.05, sensitivity=5,
                 ip_address='192.168.1.3', tcp_port=5025):
        self.channel = channel
        rm = visa.ResourceManager()

        if GPIB_interface > -1:
            resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
            self.instr = rm.open_resource(resourceName)
            self.instr.open()
        else:
            self.instr = socketInstrument(ip_address=ip_address, tcp_port=tcp_port)

        alive = self.instr.query('*IDN?')
        if alive != 0:
            print('OSA_YENISTA_OSA20 is alive')
            print(alive)

        # Initalization:
        self.instr.write(':OSA 1')  # OSA mode
        self.instr.write(':STOP')  # Make sure that no scan is running
        self.instr.write(':INIT:SMOD SING')  # Set single sweep mode
        self.instr.write(':DISP: ON')  # Show on OSA display as well
        self.instr.write(':CALC:AUTO ON')  # Calculations -> automatic

        self.spanWave = spanWave
        self.centerWave = centerWave
        self.resolutionBW = resolutionBW
        self.sensitivity = sensitivity

    def StartMeasurement(self):
        self.instr.write(':INIT:IMM')  # Start frequency sweep
        # Ask OSA if measurement is done x20:
        count = 0
        while int(self.instr.query(':STAT:OPER:COND?')):  # Wait for 20 seconds or until the measurement is done
            time.sleep(1)
            count = count + 1
            if count > 20:
                break
        return 0;

    def ReadSpectrumSimple(self):
        # Leaves OSA scanning parameters untouched
        # Start OSA measurement:

        # Initilize parameters for trace fetch:
        dataOut = []
        waveAxis = []
        startTRACE = (self.instr.query_ascii_values(':TRAC1:DATA:STAR?')[0]) * (10 ** 9)
        lengthTRACE = int(self.instr.query_ascii_values(':TRAC1:DATA:LENG?')[0])
        sampTRACE = (self.instr.query_ascii_values(':TRAC1:DATA:SAMP?')[0]) * (10 ** 9)

        # Fetch trace data:
        for i in range(lengthTRACE):
            waveAxis.append(startTRACE + i * sampTRACE)
        dataOut = self.instr.query_ascii_values(':TRAC1:DATA? 0,0')

        return [dataOut, waveAxis]  # Return x-axis in nm and y-axis in dBm

    def ReadSpectrum(self):
        # Set the OSA scanning parameters:
        self.instr.write(':SENS:WAV:CENT ' + str(self.centerWave) + 'NM')  # Center frequency
        self.instr.write(':SENS:WAV:SPAN ' + str(self.spanWave) + 'NM')  # Frequency span
        self.instr.write(':SENS:BAND ' + str(self.resolutionBW * (10 ** 3)) + 'pm')  # Resolution bandwidth
        self.instr.write(':SENS ' + str(self.sensitivity))

        # Start OSA measurement:
        self.instr.write(':INIT:IMM')  # Start frequency sweep
        # Ask OSA if measurement is done x20:
        count = 0
        while int(self.instr.query(':STAT:OPER:COND?')):  # Wait for 20 seconds or until the measurement is done
            time.sleep(1)
            count = count + 1
            if count > 20:
                break

        # Initilize parameters for trace fetch:
        dataOut = []
        waveAxis = []
        startTRACE = (self.instr.query_ascii_values(':TRAC1:DATA:STAR?')[0]) * (10 ** 9)
        lengthTRACE = int(self.instr.query_ascii_values(':TRAC1:DATA:LENG?')[0])
        sampTRACE = (self.instr.query_ascii_values(':TRAC1:DATA:SAMP?')[0]) * (10 ** 9)

        # Fetch trace data:
        for i in range(lengthTRACE):
            waveAxis.append(startTRACE + i * sampTRACE)
        dataOut = self.instr.query_ascii_values(':TRAC1:DATA? 0,0')

        return [dataOut, waveAxis]  # Return x-axis in nm and y-axis in dBm

    #### Andreas

    def ReadPeakData(self):
        # returns dictionary; dictionaries are pythons version of structures
        self.instr.write(':CALC:PAR:SMSR ON');

        FullString = self.instr.query(":CALC:DATA:SMSR?")
        SplitString = FullString.split(',');  # splits into array; sep: comma

        try:
            PWL = float(SplitString[5])
        except:
            PWL = 0
        try:
            PL = float(SplitString[8])
        except:
            PL = 0
        try:
            S1WL = float(SplitString[14])
        except:
            S1WL = 0
        try:
            S1L = float(SplitString[17])
        except:
            S1L = 0
        try:
            S1DWL = float(SplitString[20])
        except:
            S1DWL = 0
        try:
            S1SMSR = float(SplitString[23])
        except:
            S1SMSR = 0
        try:
            S2WL = float(SplitString[29])
        except:
            S2WL = 0
        try:
            S2L = float(SplitString[32])
        except:
            S2L = 0
        try:
            S2DWL = float(SplitString[35])
        except:
            S2DWL = 0
        try:
            S2SMSR = float(SplitString[38])
        except:
            S2SMSR = 0

        ReturnDict = {
            'Peak_WL': PWL,
            'Peak_WL_Unit': SplitString[6],  # physical unit used; e.g. m
            'Peak_Level': PL,
            'Peak_Level_Unit': SplitString[9],
            'SideMode1_WL': S1WL,
            'SideMode1_WL_Unit': SplitString[15],
            'SideMode1_Level': S1L,
            'SideMode1_Level_Unit': SplitString[18],
            'SideMode1_DiffWL': S1DWL,
            'SideMode1_DiffWL_Unit': SplitString[21],
            'SideMode1_SMSR': S1SMSR,
            'SideMode1_SMSR_Unit': SplitString[24],
            'SideMode2_WL': S2WL,
            'SideMode2_WL_Unit': SplitString[30],
            'SideMode2_Level': S2L,
            'SideMode2_Level_Unit': SplitString[33],
            'SideMode2_DiffWL': S2DWL,
            'SideMode2_DiffWL_Unit': SplitString[36],
            'SideMode2_SMSR': S2SMSR,
            'SideMode2_SMSR_Unit': SplitString[39]
        }
        return ReturnDict;
        # Peak_WL = ReturnDict['Peak_WL']

    def ReadValue(self, Value='Peak_WL'):
        ReturnDict = self.ReadPeakData()
        return ReturnDict[Value]
        # return ReturnDict.get(Value)

    def WriteGPIB(self, string):
        self.instr.write(string);

    def QueryGPIB(self, string):
        return self.instr.query(string);

    def CloseConnection(self):
        self.instr.close()


class OSA_YOKOGAWA:  # developer: Peter Tønning (NOT FULLY TESTED)
    """
    - DESCRIPTION:
        This class is for controlling the YOKOGAWA OSA
    """

    def __init__(self, channel=1, GPIB_interface=0, sampPoints=10001):
        self.channel = channel
        rm = visa.ResourceManager()

        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        self.instr.open()
        alive = self.instr.query('*IDN?')
        if alive != 0:
            print('OSA_YOKOGAWA is alive')
            print(alive)

        self.instr.write("*RST")
        self.instr.write("CFORM1")
        self.instr.write(':SENSE:SWEEP:POINTS ' + str(sampPoints))

    def ReadSpectrum(self, centerWave=1540, spanWave=60, resolutionBW=0.05, sensitivity='normal'):
        # Set the OSA scanning parameters:

        self.instr.write(':sens:wav:cent ' + str(centerWave) + 'nm')  # Center frequency
        self.instr.write(':sens:wav:span ' + str(spanWave) + 'nm')  # Frequency span
        self.instr.write(':sens:band ' + str(resolutionBW) + 'nm')  # Resolution bandwidth
        self.instr.write(":sens:sens " + sensitivity)

        # Start OSA measurement:
        self.instr.write(":init:smode 1")
        self.instr.write("*CLS")
        self.instr.write(":init")  # Start frequency sweep
        # Ask OSA if measurement is done x20:
        # count=0
        # while int(self.instr.query(':STAT:OPER:COND?')): #Wait for 20 seconds or until the measurement is done
        #     time.sleep(1)
        #     count=count+1
        #     if count>20:
        #         break
        count = 0

        while int(self.instr.query(':STAT:OPER:even?')) == 0:  # Wait for 20 seconds or until the measurement is done
            time.sleep(1)
            count = count + 1
            if count > 200:
                break
        # Initilize parameters for trace fetch:
        WL = self.instr.query_ascii_values(':TRACE:X? TRA')
        Power = self.instr.query_ascii_values(':TRACE:Y? TRA')

        return [Power, WL]  # Return x-axis in nm and y-axis in dBm

    def CloseConnection(self):
        self.instr.close()


class SO_HP54120A:  # developer: Peter Tønning (NOT FULLY TESTED)
    """
    - DESCRIPTION:
        This class is for controlling the HP54120A sampling oscilloscope
    """

    def __init__(self, channel=7, GPIB_interface=0, channelRFin=4, timeBase=20 * 1e-09, voltSensitivity=20 * 1e-03):
        self.channel = channel
        rm = visa.ResourceManager()

        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        self.instr.open()
        alive = self.instr.query('*IDN?')
        if alive != 0:
            print('SO_HP54120A is alive')

        self.tBase = timeBase
        self.VSensitivity = voltSensitivity
        self.inChan = channelRFin
        self.instr.write(':TIMEBASE:RANGE ' + str(int(timeBase * 1e09)) + 'NS')
        self.instr.write(':CHAN' + str(int(channelRFin)) + ':RANGE ' + str(int(voltSensitivity * 1e03)) + 'MV')

    def ReadTrace(self):

        self.instr.write(':digitize channel' + str(int(self.inChan)))  # Run the measurement on the instrument side
        counter = 0
        while not (self.instr.query('*OPC?') == '1'):
            dummy = 1  # Wait
            counter = counter + 1
            if counter > 30:
                break  # break
        self.instr.write(':waveform:source wmem' + str(self.inChan))
        self.instr.write(':waveform:format word')
        preamb0 = self.instr.query_ascii_values(':waveform:preamble?')
        # buffer = self.instr.query(':waveform:data?')
        # print(buffer)
        # data_raw = np.frombuffer(buffer, dtype=np.int8)
        data_raw = self.instr.query_binary_values(':waveform:data?', datatype='H', is_big_endian=True)
        print('Here is the preamb:')
        print(preamb0)

        print(int(preamb0[2]))
        time = (np.asarray(range(int(preamb0[2]))) - preamb0[6]) * preamb0[4] + preamb0[5]
        voltage = (np.asarray(data_raw) - preamb0[9]) * preamb0[7] + preamb0[8]

        return [voltage, time]  # Return x-axis in nm and y-axis in dBm

    def CloseConnection(self):
        self.instr.close()


class LMS_ANDO_AQ4321A:  # developer: Andreas

    def __init__(self, channel=19, GPIB_interface=0):
        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        # self.instr.read_termination = '\n'
        # self.instr.write_termination = '\n'
        self.instr.timeout = 10000
        if alive != 0:
            print('Ando AQ4321A is alive')
            print(alive)

    def Unlock(self, password=4321):
        # Does not work; manual password entry on startup is still needed;
        # this function is for locking the device and has nothng to do with the startup
        if str(self.instr.query('LOCK?')) == 1:
            self.instr.write('LOCK0 ' + str(password));
            print('Device unlocked.');
        else:
            print('Device has already been unlocked.');

    def InitialiseDevice(self):
        # Not sure if this does anything
        self.instr.write('INIT');
        while (int(self.instr.query('INIT?')) == 1):
            time.sleep(0.5);
        print('Device initialised.');

    def SetLaserState(self, onoff=1):
        self.instr.write('L' + str(onoff));
        if (self.instr.query('L?') == 0):
            print('Laser off')
        else:
            if (self.instr.query('L?') == 1):
                print('Laser on');

    def SetPower(self, mW=5.0):
        self.instr.write('TPMW' + str(mW));

    def SetWL(self, nm=1550.0):
        self.instr.write('TWL' + str(nm));

    def WriteGPIB(self, string):
        self.instr.write(string);

    def QueryGPIB(self, string):
        return self.instr.query(string);

    def CloseConnection(self):
        self.instr.close()


class LMS_HP_8153A:  # developer: Mircea Balauroiu, adjusted by Hanna Becker, not all funconalities validated yet
    """
        HP Power meter class.
        * A.initialize(): initializes the power meter
        --- Comments ---
        None
        """

    def __init__(self, channel=22, GPIB_interface=0):
        self.channel = channel
        self.__allowed_channels__ = [15, 'A']
        rm = visa.ResourceManager()
        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        self.write("*RST;*CLS;*SRE;*ESE 1")
        alive = self.instr.query('*IDN?')
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        if alive != 0:
            print('HPPowerMeter8153A is alive')
            print(alive)
        else:
            print('No connection! Maybe it´s the wrong channel or interface')

    def Write(self, command='*RST'):
        self.instr.write(command)

    def Initialize(self):  # previously initialize
        # self.write("*RST;*CLS;*SRE;*ESE 1")
        self.write("*RST;*CLS;")
        self.SetChannel('A')

    def SetChannel(self, channel):  # previously set_channel
        if channel in self.__allowed_channels__:
            self.__channel__ = channel
        else:
            print("Not an allowed channel of the power meter!" + channel)
        self.write("INIT%s:CONT ON" % self.get_channel_str_12())

    def GetChannel(self):  # previously get_channel
        return self.__channel__

    # __wavelength_unit__ = NANOMETER
    def GetWavelength(self):  # previously __wavelength_get__
        wl = self.ask_float("SENS%s:POW:WAVE?" % self.get_channel_str_12())
        return wl * 1e9

    def SetWavelength(self, value):  # previously __wavelength_set__
        self.write("SENS%s:POW:WAVE %dNM" % (self.get_channel_str_12(), int(value)))

    # __power_unit_allowed__ = [ DBM, WATT]
    def GetPowerUnit(self):  # previously __power_unit_get__
        u = self.ask_float("SENS%s:POW:UNIT?" % self.get_channel_str_12())
        if u == 1:
            power_unit = 'WATT'
            return power_unit
        elif u == 0:
            power_unit = 'DBM'
            return power_unit

    def SetPowerUnit(self, unit):  # previously __power_unit_set__
        if unit == 'WATT':
            self.write("SENS%s:POW:UNIT W" % self.get_channel_str_12())  # Watt
        elif unit == 'DBM':
            self.write("SENS%s:POW:UNIT DBM" % self.get_channel_str_12())  # dBm

    def __get_power__(self):  # not sure what this does differently from get_power
        # power = self.ask_float("READ%s:POW?" % self.get_channel_str_12() )
        power = self.ask_float("FETCH%s:POW?" % self.get_channel_str_12())
        if power > 1e37:
            if self.power_unit == 'WATT':
                power = 0.0
            else:
                power = -120.0
        return power

    def GetPower(self):  # previously get_power
        # power = self.ask_float("READ%s:POW?" % self.get_channel_str_12() )
        power = self.instr.query_ascii_values("FETCH%s:POW?" % self.get_channel_str_12())
        return power

    def get_channel_str_12(self):
        return '1' if (self.__channel__ == 'A') else '2'

    def GetAveragingTime(self):  # previously __averaging_time_get__
        value = self.ask_float("SENS%s:POW:ATIME?" % self.get_channel_str_12())
        return value * 1000  # device returns seconds

    def SetAveragingTime(self, value):  # previously __averaging_time_set__
        command = "SENS%s:POW:ATIME %dMS" % (self.get_channel_str_12(), int(value))
        self.write(command)

    # allowed_values=['AUTO', 10*DBM, 0*DBM, -10*DBM, -20*DBM, -30*DBM, -40*DBM, -50*DBM, -60*DBM, -70*DBM]
    def SetRange(self, value):  # previously __range_set__
        if value == 'AUTO':
            self.write('SENSe%s:POWer:RANGe:AUTO 1' % self.get_channel_str_12())
        else:
            command = 'SENSe%s:POWer:RANGe:AUTO 0;' % self.get_channel_str_12()
            self.write(command)
            command = 'SENSe%s:POWer:RANGe %d;' % (self.get_channel_str_12(), value.get_value(DBM))
            self.write(command)

    def GetRange(self):  # previously __range_get__
        value = self.ask('SENSe%s:POWer:RANGe?' % (self.get_channel_str_12(),))
        return int(value) * DBM

    def CloseConnection(self):  # previously close
        self.instr.close()

    def ReadPower(self):  # previously read_power
        power = self.ask_float("READ%s:POW?" % self.get_channel_str_12())
        if power > 1e37:
            if self.power_unit == 'WATT':
                power = 0.0
            else:
                power = -120.0
        return power


class PM100USB:  # developer: Lars Nielsen

    def __init__(self, lambda0=1550, no=1):
        self.PDinstr = TLPM()
        deviceCount = c_uint32()
        self.PDinstr.findRsrc(byref(deviceCount))
        counter = 1
        resourceName = create_string_buffer(1024)
        for i in range(0, deviceCount.value):
            self.PDinstr.getRsrcName(c_int(i), resourceName)
            if no == counter:
                break

        self.PDinstr.close()

        self.PDinstr = TLPM()
        self.PDinstr.open(resourceName, c_bool(True), c_bool(True))
        self.PDinstr.setWavelength(c_double(lambda0))
        message = create_string_buffer(1024)
        self.PDinstr.getCalibrationMsg(message)
        print(message.value)

    def SetWavelength(self, lambda0=1550):
        self.PDinstr.setWavelength(c_double(lambda0))

    def GetPower(self):
        power = c_double()
        pU = c_int16()
        lam0 = c_double()
        self.PDinstr.measPower(byref(power))
        self.PDinstr.getPowerUnit(byref(pU))
        self.PDinstr.getPhotodiodeResponsivity(c_int16(0), byref(lam0))
        #        print('Power unit:',lam0)
        # print('Power unit:',self.PDinstr.getPowerUnit(byref(lam)))
        return power.value

    def CloseConnection(self):
        return self.PDinstr.close()


# OSCILLOSCOPES
class OSC_TDS320:  # developer: Lars Nielsen

    def __init__(self, channel=30, GPIB_interface=0):
        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        if alive != 0:
            print('TDS 320 is alive')
            print(alive)

    def GetTrace(self):
        self.instr.write('DATA:SOURCE CH1')
        self.instr.write('ACQUIRE:STATE:RUN')
        delta_t = self.instr.query_ascii_values('WFMPRe:CH1:XINcr?')[0]
        delta_y = self.instr.query_ascii_values('WFMPRe:CH1:YMUlt?')[0]
        dataOut = (np.asarray(self.instr.query_ascii_values('CURVe?')) * delta_y).tolist()
        timeAxis = [i * delta_t for i in range(len(dataOut))]

        return [dataOut, timeAxis]  # Return x-axis in s and y-axis in V

    def CloseConnection(self):
        self.instr.close()


# AMPLIFIERS
class EDFA_KEOPSYS:  # developer: Andreas Hänsel and Peter Tønning
    # Standard LAN settings:
    # IP: 192.168.1.20
    # Subnet: 255.255.255.0
    # Gw: 192.168.1.1

    # only APC and OFF supported so far
    def __init__(self, ip='192.168.1.20'):
        hostname = ip
        TCPport = 22
        username = "guest"
        password = 'password'  # sys.argv[2]
        self.command = 'localserial'  # sys.argv[3]
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname, port=TCPport, username=username, password=password)
        self.client.invoke_shell();

        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        self.stdin.write('SL1_DES?\n');  # device description
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        ImportantLine = output.split()[9].decode('utf-8')  # String
        print(ImportantLine)

    def SetMode(self, mode='APC'):
        # APC: automatic power control; ACC: automatic current control; OFF: Pump diodes off
        # 0: OFF; 1: ACC; 2: APC (only between 20 and 30 dBm out)
        # Modes cannot be changed after the key has been turned!
        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        self.stdin.write('SL1_ASS?\n');
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        string = output.split()[9].decode('utf-8')  # String
        string2 = re.split('=', string);
        if (float(string2[1]) == 0):
            print('Mode has been OFF');
        else:
            if (float(string2[1]) == 1):
                print('Mode has been ACC');
            else:
                if (float(string2[1]) == 2):
                    print('Mode has been APC');
        if (mode == 'OFF'):
            self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
            self.stdin.write('SL1_ASS=0\n');
            self.stdin.flush()
            self.stdin.write('exit\n')
            print('Mode is now OFF');
        else:
            if (mode == 'ACC'):
                self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
                self.stdin.write('SL1_ASS=1\n');
                self.stdin.flush()
                self.stdin.write('exit\n')
                print('Mode is now ACC');
            else:
                if (mode == 'APC'):
                    self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
                    self.stdin.write('SL1_ASS=2\n');
                    self.stdin.flush()
                    self.stdin.write('exit\n')
                    print('Mode is now APC');
                else:
                    print('Unrecognized mode; accepted entries are OFF, ACC, and APC.');

    def GetInputPower(self):
        # Reads optical input power, returns float in dBm
        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        self.stdin.write('SL1_IPW?\n');
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        string = output.split()[9].decode('utf-8')  # String
        string2 = re.split('=', string);
        return float(string2[1]) / 10;

    def GetOutputPower(self):
        # Reads optical output power, returns float in dBm
        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        self.stdin.write('SL1_OPW?\n');
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        string = output.split()[9].decode('utf-8')  # String
        string2 = re.split('=', string);
        return float(string2[1]) / 10;

    def GetLaserCurrent(self):
        # Reads optical output power, returns float in mA
        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        self.stdin.write('SL1_ID2?\n');
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        string = output.split()[9].decode('utf-8')  # String
        string2 = re.split('=', string);
        return float(string2[1])

    def GetTemperature(self):
        # Reads case temperature, returns float in degC
        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        self.stdin.write('SL1_CAT?\n');
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        string = output.split()[9].decode('utf-8')  # String
        string2 = re.split('=', string);
        return float(string2[1]) / 100;

    def GetNominalOutputPower(self):
        # Reads nominal output power (maximum power?), returns float in dBm
        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        self.stdin.write('SL1_PON?\n');
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        string = output.split()[9].decode('utf-8')  # String
        string2 = re.split('=', string);
        return float(string2[1]) / 10;

    def GetTargetOutputPower(self):
        # Reads nominal output power (maximum power?), returns float in dBm
        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        self.stdin.write('SL1_SOP?\n');
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        string = output.split()[9].decode('utf-8')  # String
        string2 = re.split('=', string);
        return float(string2[1]) / 10;

    def SetTargetOutputPower(self, power=10):
        # Sets Target Output Power (in dBm); Requires APC mode
        # (The manual states a factor 100 for entering the power,
        # although everything else is using factor 10. I assume a typo)
        # Takes only integer inputs between 20 and 30 (So one decimal is doable if the factor of 10 is moved to the control script)!
        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        powerstring = str(power * 10);
        self.stdin.write('SL1_SOP=' + powerstring + '\n');
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        string = output.split()[9].decode('utf-8')  # String
        string2 = re.split('=', string);

    def SetTargetCurrent(self, current=0.500):
        # Sets Target Current (in A!);
        # Requires ACC mode (Modes cannot be changed after the key has been turned!)
        # Takes only integer inputs!
        # A time delay is needed between setting an input and giving the next commmand.
        self.stdin, self.stdout, self.stderr = self.client.exec_command(self.command)
        currentstring = str(int(current * 1e3));
        self.stdin.write('SL1_IC2=' + currentstring + '\n');
        self.stdin.flush()
        self.stdin.write('exit\n')
        output = self.stdout.read()
        string = output.split()[9].decode('utf-8')  # String
        string2 = re.split('=', string);

    def SetOutputPower(self, power=10):
        self.SetTargetOutputPower(power);

    def CloseConnection(self):
        self.client.close()


class OSCI_SIGLENT:  # developer: Lars Nielsen

    def __init__(self, channel=20, IP_address='192.168.1.52'):
        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'TCPIP0::' + IP_address + '::inst0::INSTR'

        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        self.instr.timeout = 10000
        if alive != 0:
            print('SIGLENT OSCILLOSCOPE is alive')
            print(alive)

        self.ch1_voltage = None
        self.ch1_time = None
        self.ch2_voltage = None
        self.ch2_time = None

    def get_char_bit(char, n):
        return (char >> n) & 1

    def ReadSpectrum(self, channel=1):
        self.instr.clear()

        self.instr.write("chdr off")
        self.instr.write("wfsu sp,0,np,0")
        self.instr.write("msiz 1.4M")
        vdiv = self.instr.query("c%d:vdiv?" % (channel,))
        ofst = self.instr.query("c%d:ofst?" % (channel,))
        tdiv = self.instr.query("tdiv?")
        sara = self.instr.query("sara?")

        sara = float(sara)

        self.instr.timeout = 30000  # default value is 2000(2s)
        self.instr.chunk_size = 20 * 1024 * 1024  # default value is 20*1024(20k bytes)
        self.instr.write("c%d:wf? dat2" % (channel,))
        recv = list(self.instr.read_raw())[15:]

        recv.pop()
        recv.pop()
        self.volt_value = []
        for data in recv:
            if data > 127:
                data = data - 255
            else:
                pass
            self.volt_value.append(data)

        self.time_value = []

        for idx in range(0, len(self.volt_value)):
            self.volt_value[idx] = self.volt_value[idx] / 25 * float(vdiv) - float(ofst)
            time_data = -(float(tdiv) * 14 / 2) + idx * (1 / sara)
            self.time_value.append(time_data)

        if channel == 1:
            self.ch1_voltage = self.volt_value
            self.ch1_time = self.time_value
        elif channel == 2:
            self.ch2_voltage = self.volt_value
            self.ch2_time = self.time_value

        return self.time_value, self.volt_value

    def SaveAllTxt(self, sweepName='SWEEP_NAME', additionalText='*ADDITIONAL INFORMATION*'):

        filenamePREFIX = './' + sweepName + '/' + sweepName

        os.mkdir(sweepName)

        if self.ch1_voltage != None and self.ch1_time != None:
            data_mat = np.column_stack((self.ch1_time, self.ch1_voltage))
            np.savetxt(filenamePREFIX + '_ch1.txt', data_mat[:, :],
                       header=filenamePREFIX + '_ch2.txt\n' + additionalText, delimiter='\t')

        if self.ch2_voltage != None and self.ch2_time != None:
            data_mat = np.column_stack((self.ch2_time, self.ch2_voltage))
            np.savetxt(filenamePREFIX + '_ch2.txt', data_mat[:, :],
                       header=filenamePREFIX + '_ch2.txt\n' + additionalText, delimiter='\t')

        return 1

    def CloseConnection(self):
        self.instr.close()

    # MISC


class DL_ODL_650:  # developer: Lars Nielsen

    def __init__(self, COMport=5):
        rm = visa.ResourceManager()
        resourceName = 'COM' + str(int(COMport))
        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('V1')
        # self.instr.read_termination = '\n'
        # self.instr.write_termination = '\n'
        self.instr.timeout = 10000
        if alive != 0:
            print('DL_ODL_650 is alive')
            print(alive)
            print(self.instr.read())

    # def GetTrace(self):
    #    self.slot = slot;
    #    self.instr.write(':SLOT '+str(int(self.slot)));

    def SetDelayTime(self, delayTime=50):
        messageODL = 'NONE'
        messageODL = self.instr.query('T' + str(delayTime))
        if not ('Done' in messageODL):
            while not ('Done' in messageODL):
                messageODL = messageODL + self.instr.read()
        print(delayTime)
        # print('ERROR WHEN WRITING TO ODL 650')
        # messageODL='NONE'
        # while not('Done' in messageODL):
        #    messageODL = messageODL+self.instr.read()

    def CloseConnection(self):
        self.instr.close()


class PZ_BPC303:  # developer: Lars Nielsen
    """
    - Description:
        Driver for the Thorlabs BPC 303 piezo controller. Read or set the voltage of each channel. Automatic alignment functionality is also included.

        IMPORTANT: Install the BPC 303 as a virtual COM port. See labbook for details.

        EXAMPLE1 (align fiber to chip to fiber with power meter):
            import PIC_lab_control
            #Create instance of components:
            PZ_right = PIC_lab_control.PZ_BPC303(COMport=4)
            PZ_left = PIC_lab_control.PZ_BPC303(COMport=5)
            LMS1=PIC_lab_control.LMS_AGILENT_8164B()
            #Do the alignment (only YZ, i.e. transversal)
            PZ_right.AlignYZ(LMS1.ReadPower0)
            PZ_left.AlignYZ(LMS1.ReadPower0)
            #Close connections:
            PZ_right.CloseConnection()
            PZ_left.CloseConnection()
            LMS1.CloseConnection()
    """

    def __init__(self, COMport=3):
        # self.instr.write_raw(b'\x05\x00\x00\x00\x11\x01') #request
        # self.instr.write_raw(b'\x23\x02\x01\x00\x11\x01') #identify
        self.instr = serial.Serial('COM' + str(int(COMport)), baudrate=115200, bytesize=serial.EIGHTBITS, timeout=1,
                                   stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, rtscts=True)
        self.instr.write(b'\x05\x00\x00\x00\x11\x01')
        self.instr.write(b'\x10\x02\x02\x01\x11\x01')  # Enable channel 2
        self.instr.write(b'\x23\x02\x01\x00\x11\x01')  # Identify ch1
        alive = self.instr.read(100)
        if alive != 0:
            print('PZ controller is alive!')
            print(alive)

    def SetPZVoltageCH1(self, voltage):
        binVoltage = np.binary_repr(int(round((voltage / 75) * 32767)), width=16).encode()
        byte1 = int(binVoltage[0:8], 2).to_bytes(1, byteorder='little')
        byte2 = int(binVoltage[8:], 2).to_bytes(1, byteorder='little')
        self.instr.write(b'\x43\x06\x04\x00\xA1\x01\x01\x00' + byte2 + byte1)  # dest|: A1 for channel 1 (0x21 OR 0x80)
        return 1

    def SetPZVoltageCH2(self, voltage):  # NOT DONE - PROBLEMS WITH CHANNEL SELECT
        binVoltage = np.binary_repr(int(round((voltage / 75) * 32767)), width=16).encode()
        byte1 = int(binVoltage[0:8], 2).to_bytes(1, byteorder='little')
        byte2 = int(binVoltage[8:], 2).to_bytes(1, byteorder='little')
        self.instr.write(b'\x43\x06\x04\x00\xA2\x01\x01\x00' + byte2 + byte1)  # dest|: A2 for channel 2 (0x22 OR 0x80)
        return 1
        # self.instr.write(b'\x43\x06\x04\x00\xD0\x01\x02\x00\x77\x77')

    def SetPZVoltageCH3(self, voltage):  # NOT DONE - PROBLEMS WITH CHANNEL SELECT
        binVoltage = np.binary_repr(int(round((voltage / 75) * 32767)), width=16).encode()
        byte1 = int(binVoltage[0:8], 2).to_bytes(1, byteorder='little')
        byte2 = int(binVoltage[8:], 2).to_bytes(1, byteorder='little')
        # self.instr.write(b'\x43\x06\x04\x00\xD0\x01\x03\x00\x77\x77')
        self.instr.write(b'\x43\x06\x04\x00\xA3\x01\x01\x00' + byte2 + byte1)  # dest|: A3 for channel 3 (0x23 OR 0x80)

    def GetPZVoltageCH1(self):
        self.instr.write(b'\x44\x06\x01\x00\x21\x01')  # dest|: 0x21 for channel 1
        rawMessage = self.instr.read(10)  # receive 10 bytes
        int1 = rawMessage[-1]  # int.from_bytes(rawMessage[-1],byteorder='little')
        int2 = rawMessage[-2]  # int.from_bytes(rawMessage[-2],byteorder='little')
        bin1 = np.binary_repr(int1, width=8)
        bin2 = np.binary_repr(int2, width=8)
        totbin = bin1 + bin2
        intVoltage = int(totbin, 2)
        voltage = (intVoltage / 32767) * 75
        return voltage

    def GetPZVoltageCH2(self):
        self.instr.write(b'\x44\x06\x01\x00\x22\x01')  # dest|: 0x22 for channel 2
        rawMessage = self.instr.read(10)  # receive 10 bytes
        int1 = rawMessage[-1]  # int.from_bytes(rawMessage[-1],byteorder='little')
        int2 = rawMessage[-2]  # int.from_bytes(rawMessage[-2],byteorder='little')
        bin1 = np.binary_repr(int1, width=8)
        bin2 = np.binary_repr(int2, width=8)
        totbin = bin1 + bin2
        intVoltage = int(totbin, 2)
        voltage = (intVoltage / 32767) * 75
        return voltage

    def GetPZVoltageCH3(self):
        self.instr.write(b'\x44\x06\x01\x00\x23\x01')  # dest|: 0x23 for channel 3
        rawMessage = self.instr.read(10)  # receive 10 bytes
        int1 = rawMessage[-1]  # int.from_bytes(rawMessage[-1],byteorder='little')
        int2 = rawMessage[-2]  # int.from_bytes(rawMessage[-2],byteorder='little')
        bin1 = np.binary_repr(int1, width=8)
        bin2 = np.binary_repr(int2, width=8)
        totbin = bin1 + bin2
        intVoltage = int(totbin, 2)
        voltage = (intVoltage / 32767) * 75
        return voltage

    def AlignYZ(self, maximizeFunction):
        # When aligning the settle time in code needs to be equal to or larger than the actual settle time. For Thorlabs piezos a 0V->75V takes 3 ms. Thus 400ms is on the safe side according to this. The tested (by set and get to PZ controller) setteling time is around 400 ms.
        AA = AutomaticAlignment(func_x=[self.SetPZVoltageCH2, self.SetPZVoltageCH3], func_y=maximizeFunction,
                                x_start=[self.GetPZVoltageCH2(), self.GetPZVoltageCH3()], x_minstep=0.005,
                                settleTime=0.5, eps_or_beta=0.06, stopPercentage=0.001, maxIterations=30,
                                optMethod='HookJeeves')
        AA.Align()

    def CloseConnection(self):
        self.instr.close()


class ESA_SIGLENT:  # developer: Lars Nielsen

    def __init__(self, channel=20, IP_address='192.168.1.11', spanFreq=15 * 10 ** 6, centerFreq=120 * 10 ** 6,
                 videoBW=100, resolutionBW=100, dataPointsInSweep=20001):
        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'TCPIP0::' + IP_address + '::inst0::INSTR'

        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('*IDN?')
        # self.instr.read_termination = '\n'
        # self.instr.write_termination = '\n'
        self.instr.timeout = 10000
        if alive != 0:
            print('ESA_SIGLENT is alive')
            print(alive)

        self.instr.write(':INITiate:CONTinuous OFF')
        self.instr.write(':FORMat ASCii')
        self.instr.write(':BWID:AUTO OFF')
        self.instr.write('BWIDth:VIDeo:AUTO OFF')
        self.instr.write(':BWIDth:VIDeo:RATio:CONfig 0')

        self.spanFreq = spanFreq
        self.centerFreq = centerFreq
        self.videoBW = videoBW
        self.resolutionBW = resolutionBW
        self.dataPointsInSweep = dataPointsInSweep
        # self.instr.write('*RST')                                #Reset
        # self.instr.write('SYST:DISP:UPD ON')                    #Show on ESA display as well

    def SetSpectrumParameters(self, spanFreq=1000, centerFreq=15000, videoBW=0.01, resolutionBW=1,
                              dataPointsInSweep=20001):
        self.spanFreq = spanFreq
        self.centerFreq = centerFreq
        self.videoBW = videoBW
        self.resolutionBW = resolutionBW
        self.dataPointsInSweep = dataPointsInSweep

    def ReadSpectrum(self):

        self.instr.write(':FREQuency:CENTer ' + str(self.centerFreq) + ' MHz')
        self.instr.write(':FREQuency:SPAN ' + str(self.spanFreq) + ' MHz')

        self.instr.write(':BWIDth ' + str(self.resolutionBW) + ' MHz')
        self.instr.write(':BWIDth:VIDeo ' + str(round(self.videoBW * 1000)) + ' KHZ')
        self.instr.write(':INITiate:IMMediate')
        self.instr.query('*OPC?')
        dummy = self.instr.query(':TRACe:DATA? 1').split(',')
        dataOut = []
        for i in range(len(dummy) - 1):
            dataOut.append(float(dummy[i]))
        dataOut = np.array(dataOut)
        freqAxis = (10 ** 6) * np.arange(self.centerFreq - self.spanFreq / 2, self.centerFreq + self.spanFreq / 2,
                                         self.spanFreq / len(dataOut))  # Generate corresponding frequency axis

        # dataOut = np.array(self.instr.query_ascii_values(':TRACe:DATA? 1'))
        #        #self.instr.query_ascii_values(':TRACe:DATA? 1')
        # print(self.instr.query_binary_values(':TRACe:DATA? 1'))
        #############
        # self.instr.clear()
        # self.instr.write('FREQ:CENT '+str(self.centerFreq)+' MHz')   #Center frequency
        # self.instr.write('FREQ:SPAN '+str(self.spanFreq)+' MHz')     #Frequency span
        # self.instr.write('BAND '+str(self.resolutionBW)+' MHz')      #Resolution bandwidth
        # self.instr.write('BAND:VID '+str(self.videoBW*1000)+' kHz')  #Video bandwidth
        # self.instr.write('SWE:POIN '+str(int(self.dataPointsInSweep)))                 #Number of data points in sweep

        # self.instr.write('INIT')                                #Start frequency sweep
        # self.instr.query('*OPC?')                               #Wait until

        return [dataOut.tolist(),
                freqAxis.tolist()]  # Return x and y values, corresponding to frequency and power/res respectively

    def ReadPeakPower(self, Nread=5):
        power = []
        for x in range(
                Nread):  # Make "N" sweeps to make sure that no "dead" readouts are happening due to the instability of the heterodyne system.
            time.sleep(0.2)
            self.instr.clear()
            self.instr.write('FREQ:CENT ' + str(self.centerFreq) + ' MHz')  # Center frequency
            self.instr.write('FREQ:SPAN ' + str(self.spanFreq) + ' MHz')  # Frequency span
            self.instr.write('BAND ' + str(self.resolutionBW) + ' MHz')  # Resolution bandwidth
            self.instr.write('BAND:VID ' + str(self.videoBW * 1000) + ' kHz')  # Video bandwidth
            self.instr.write('SWE:POIN ' + str(int(self.dataPointsInSweep)))  # Number of data points in sweep

            self.instr.write('INIT')  # Start frequency sweep
            self.instr.query('*OPC?')  # Wait until

            dataOut = np.array(self.instr.query_binary_values('FORM REAL,32;:TRAC? TRACE1'))
            power.append(np.max(dataOut))  # Record the maximum point on all 5 sweeps
        powermax = np.max(power)  # Only pass on the maximum of the 5 peak values found
        return float(powermax)  # Return only the power value of the maximum within the sweep

    def ReadSpectrumPN(self):
        self.instr.clear()
        self.instr.write('INST:SEL PNO')
        self.instr.write('FREQ:STAR 10kHZ')
        self.instr.write('FREQ:STOP 1GHZ')
        self.instr.write('SWE:MODE NORM')
        self.instr.write('FREQ:TRAC ON')
        # self.instr.query_binary_values('FETC:PNO2:RPM?')

        self.instr.query('INIT;*WAI')  # Start frequency sweep
        # self.instr.query('*OPC?')                               #Wait until

        dataOut = np.array(self.instr.query_binary_values('FORM REAL,32;:TRAC? TRACE1'))
        freqAxis = (10 ** 6) * np.arange(self.centerFreq - self.spanFreq / 2, self.centerFreq + self.spanFreq / 2,
                                         self.spanFreq / len(dataOut))  # Generate corresponding frequency axis

        return [dataOut.tolist(),
                freqAxis.tolist()]  # Return x and y values, corresponding to frequency and power/res respectively

    def CloseConnection(self):
        self.instr.close()


class FILT_WLTF:  # developer: Lars Nielsen

    def __init__(self, COMport=5):
        rm = visa.ResourceManager()
        resourceName = 'COM' + str(int(COMport))
        self.instr = rm.open_resource(resourceName)
        alive = self.instr.query('dev?')
        self.instr.timeout = 10000
        if alive != 0:
            print('FILT_WLTF is alive')
            print(alive)
            # print(self.instr.read())

    def SetCenterWavelength(self, lambda0=1550.000):
        messageODL = 'NONE'
        messageODL = self.instr.query('Set Wavelength: ' + str(lambda0) + 'nm')
        if messageODL == 'OK':
            doNothing = 1
        else:
            print('Did not recieve an OK from FILT_WLTF - filter position could not be set!')
        return 1

    def StepDiscrete(self, steps=1):
        if steps > 0:  # forward
            messageODL = self.instr.query('SF:' + str(int(steps)))
            if messageODL == 'OK':
                doNothing = 1
            else:
                print('Did not recieve an OK from FILT_WLTF - did not step!')
        else:  # backward
            messageODL = self.instr.query('SB:' + str(int(steps)))
            if messageODL == 'OK':
                doNothing = 1
            else:
                print('Did not recieve an OK from FILT_WLTF - did not step!')
        return 1

    def GetCenterWavelength(self):
        messageODL = 'NONE'
        messageODL = self.instr.query('WL?')
        lambda0 = float(messageODL[11:19])
        return lambda0

    def CloseConnection(self):
        self.instr.close()


class TOPTICA_CTL950:  # developer: Fabian Ruf
    """
    - Description:



        EXAMPLE1



    """

    def __init__(self, IP_address='192.168.1.100'):

        nest_asyncio.apply()
        self.dlc = toptica.DLCpro(toptica.NetworkConnection(IP_address))
        self.dlc.open()

    def __enter__(self):
        return self

    def GetEmissionStatus(self):
        return self.dlc.emission.get()

    def GetPower(self):
        return self.dlc.laser1.ctl.power.power_act.get()

    def GetPowerStabilizationStatus(self):
        return self.dlc.laser1.power_stabilization.enabled.get()

    def SetPowerStabilizationStatus(self, enabled=True):
        self.dlc.laser1.power_stabilization.enabled.set(enabled)
        return 1

    def GetPowerStabilizationParameters(self):
        gain = self.dlc.laser1.power_stabilization.gain.all.get()
        p = self.dlc.laser1.power_stabilization.gain.p.get()
        i = self.dlc.laser1.power_stabilization.gain.i.get()
        d = self.dlc.laser1.power_stabilization.gain.d.get()
        return gain, p, i, d

    def SetPowerStabilizationParameters(self, p, i, d=0, gain=1):
        self.dlc.laser1.power_stabilization.gain.all.set(gain)
        self.dlc.laser1.power_stabilization.gain.p.set(p)
        self.dlc.laser1.power_stabilization.gain.i.set(i)
        self.dlc.laser1.power_stabilization.gain.d.set(d)
        return 1

    def SetPower(self, power_mW):
        self.SetPowerStabilizationStatus(True)
        self.dlc.laser1.power_stabilization.setpoint.set(power_mW)
        return 1

    def GetWavelength(self):
        return self.dlc.laser1.ctl.wavelength_act.get()

    def SetWavelength(self, lambda0):

        delta = 0.01
        t = 0
        delta_t = 0.05
        t_wait = delta_t
        t_max = 10

        if lambda0 < 910 or lambda0 > 980:
            print('ERROR in Toptica->SetWavelength: wavelength range exceeded')
            return 1

        self.dlc.laser1.ctl.wavelength_set.set(float(lambda0))

        while abs(self.GetWavelength() - lambda0) > delta:
            time.sleep(delta_t)
            t = t + delta_t;

            if t > t_max:
                print('ERROR in Toptica->SetWavelength: max time exceeded')
                break
        time.sleep(t_wait)
        t = t + t_wait;
        print(lambda0, t, abs(self.GetWavelength() - lambda0), sep=' --- ')

        return 1

    def GetCurrent(self):
        return self.dlc.laser1.dl.cc.current_act.get()

    def SetCurrent(self, current0):

        if current0 > 160:
            print('ERROR in Toptica->SetWavelength: current range exceeded')
            return 1

        self.dlc.laser1.dl.cc.current_set.set(float(current0))
        return 1

    def CloseConnection(self):
        self.dlc.close()


class ANDO_OSA:
    def __init__(self, channel=30, GPIB_interface=0):
        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        self.instr = rm.open_resource(resourceName);
        self.instr.write('ATREF0');
        # self.instr.write('SMPL1001')
        # self.instr.write('SNAT')

        # alive = self.instr.query('*IDN?')
        # self.instr.read_termination = '\n'
        # self.instr.write_termination = '\n'
        # self.instr.timeout = 10000
        # if alive != 0:
        # print('Ando AQ4321A is alive')
        # print(alive)

    def SetLeveldB(self, Level=-65.0):
        self.instr.write('REFL' + str(Level));  # in dBm XXX.X

    def SetLevelnW(self, Level=1.00):
        self.instr.write('REFN' + str(Level));  # in nW X.XX

    def SetLeveluW(self, Level=1.00):
        self.instr.write('REFU' + str(Level));  # in uW X.XX 0.01 --> 1 to 9.99, 0.1-->10 to 99.9,

    def SetLevelmW(self, Level=1.00):
        self.instr.write('REFM' + str(Level));  # in mW X.XX 0.01 --> 1 to 9.99, 0.1-->10 to 99.9

    def CenterWL(self, WL=450.0):
        self.instr.write('CTRWL' + str(WL));

    def SingleSweep(self):
        self.instr.write('SGL');

    def AutoSweep(self):
        self.instr.write('AUTO');

    def ContinousSweep(self):
        self.instr.write('RPT');

    def SetupOSA(self, CenterWL=445, Span=10, Level=0, Resolution=0.05, Sensitivity=0, Preview=0):
        self.instr.write('CTRWL' + str(CenterWL));  # in nm
        self.instr.write('SPAN' + str(Span));  # in nm
        self.instr.write('RESLN' + str(Resolution))  # in nm XX.XX
        if Sensitivity == 0:
            self.instr.write('SNAT');
        else:
            self.instr.write('SHI' + str(Sensitivity))

        if Level == 0:
            self.instr.write('ATREF1');
        else:
            self.instr.write('REFL' + str(Level));  # in dBm XXX.X
        if Preview == 1:
            self.instr.write('SGL');

    def Stop(self):
        self.instr.write('STP');

    def stop(self):
        self.instr.write('STP');

    def StopSweep(self):
        self.instr.write('STP');

    def GetSpectrum(self):
        # time.sleep(5)
        self.instr.write('SGL');
        Status = 1
        StatusOut = []
        while Status == 1:
            Mode = self.instr.query('SWEEP?')  # Something is broken here... Check up on the output of mode
            Status = float(Mode)
            time.sleep(0.2)
            StatusOut.append(Status)

        Power = self.instr.query('LDATAR0001-R1001')

        # Power=Power.replace("−", "-")
        PowerF = [float(value) for value in Power.split(',')]

        WL = self.instr.query('WDATAR0001-R1001')

        WLF = [float(value) for value in WL.split(', ')]
        return [PowerF[1:], WLF[1:]]


# Lab control functionality:#######################

class Sweep2D:  # developer: Lars Nielsen
    """
    - DESCRIPTION:
        This class is for sweeping a number (maximum 2) set of setFunction's while reading a number (unlimited) getFunctions.

        SetFunction : list of functions (maximum 2)
            SetFunction = [SetFunction1,SetFunction2], or as a single function: SetFunction1

        GetFunction : list of functions
            GetFunction = [GetFunction1,GetFunction2, GetFunction3, ....]

        sweepPar: list of lists
            the sweep values are given as [x1,x2] in which x1 is passed as arguments to the first SetFunction: setFunction1, and the values in x2 are passed to SetFunction2.

        setLabels : list of strings
            A list with the labels for the parameter set by the SetFunction's

        getLables : list of strings
            A list with the labels for the output of the GetFunction's

        timeFromSetToGet : float
            Determines the time from setting a value with the SetFunction and to the GetFunction is read. This is to make sure that the system under test has settled

        To run the sweep use Sweep2D.run(). Pass True as an argument to monitor the sweep output while sweeping.
        To save all the data from one sweep use the SaveAllTxt(sweepName='SWEEP_NAME') function.
        The data is organized in multiple files and put into a single folder labelled named after the sweepName, i.e. 'SWEEP_NAME' .
        Those are readable with a simple text editor

    - EXAMPLE OF USE:
        EX1 - define set and get functions. Define sweep values. Setup the sweep by creating an object SWEEP0. Run the sweep defined in SWEEP0 with live plot updates. Save all data to text-files.
            def setter1(inputArg):....
            def setter2(inputArg):....
            def getter1():.....
            def getter2():.....
            x1 = [1,2,3,4,5,6,7,8,9,10]
            x2 = [0,5,10,15]
            SWEEP0 = PIC_lab_control.Sweep2D(sweepPar=[x1,x2],SetFunction =[setter1,setter2],GetFunction = [getter1,getter2],setLabels=['x1','x2'],getLabels=['out1','out2'],timeFromSetToGet=1)
            SWEEP0.Run(plotting = True)
            SWEEP0.SaveAllTxt(sweepName='Test',additionalInformation ='This is a test' )
    """

    def __init__(self, sweepPar=[], SetFunction=[], GetFunction=[], setLabels=[], getLabels=[], timeFromSetToGet=0.01):
        # Define data axis'
        if isinstance(sweepPar, list):  # = Sweep
            if isinstance(sweepPar[0], list) and len(sweepPar) > 1:  # = 2D sweep:
                self.sweepPar = sweepPar
                self.x1_size = len(self.sweepPar[0][:])
                self.x2_size = len(self.sweepPar[1][:])
                self.SetFunction = SetFunction
                self.noSetters = len(self.SetFunction)
            else:  # = 1D sweep   #FIXED THE BUGSYBUG: single list in list, i.e. sweepPar=[x1],SetFunction=[SetFunc1], was not possible - now it is!!!
                if isinstance(sweepPar[0], list):
                    self.x1_size = len(sweepPar[0])
                    self.sweepPar = [sweepPar[0], [0]]
                    self.SetFunction = [SetFunction[0], self.DoNothing()]
                else:
                    self.x1_size = len(sweepPar)
                    self.sweepPar = [sweepPar, [0]]
                    self.SetFunction = [SetFunction, self.DoNothing()]
                self.x2_size = 1
                self.noSetters = 1

        else:  # = One shot (no sweep)
            self.x1_size = 1
            self.sweepPar = [[sweepPar], [0]]
            self.x2_size = 1
            self.noSetters = 1
            self.SetFunction = [SetFunction, self.DoNothing()]

        if not (isinstance(GetFunction, list)):
            self.GetFunction = [GetFunction]
        else:
            self.GetFunction = GetFunction

        self.noGetters = len(self.GetFunction)
        self.FreqAxiss = []
        self.FreqAxisIndices = []
        self.Data = [[[[] for i in range(self.x2_size)] for i in range(self.x1_size)] for i in range(self.noGetters)]

        # Inititalize names:
        if setLabels == []:
            self.parTitle = ['x1', 'x2']
        elif not (isinstance(setLabels, list)):
            self.parTitle = [setLabels, 'x2']
        else:
            if len(setLabels) > 1:
                self.parTitle = setLabels
            else:
                self.parTitle = [setLabels[0], 'x2']

        self.outTitle = ['out' + str(k) for k in range(self.noGetters)]
        if not (getLabels == []):
            if isinstance(getLabels, list):
                for i in range(len(getLabels)):
                    self.outTitle[i] = getLabels[i]
            else:
                self.outTitle[0] = getLabels

        # Dynamic paramters:
        self.timeFromSetToGet = timeFromSetToGet

        # Initialize plots:
        self.figHandle = plt.figure()  # figHandle
        self.axHandle = [0 for i in range(self.noGetters)]
        for i in range(self.noGetters):
            self.axHandle[i] = self.figHandle.add_subplot(self.noGetters, 1, (i + 1))

    def Run(self, plotting=False):
        """
        - DESCRIPTION:
            Start the sweep.

            plotting : boolean
                Set true if the sweep output data is to be monitored while sweeping.
        """
        if plotting:
            plt.show(block=False)

        for l in range(self.noGetters):

            if isinstance(self.GetFunction[l](), list):  # not(int(self.GetFunction[l]())==self.GetFunction[l]()):
                self.FreqAxiss.append(self.GetFunction[l]()[1])  # self.FreqGenerator[countTemp]()
                self.FreqAxisIndices.append(l)

        for i in range(self.x2_size):
            if self.noSetters == 2:
                self.SetFunction[1](self.sweepPar[1][i])

            # if self.noSetters>1:

            for j in range(self.x1_size):
                self.SetFunction[0](self.sweepPar[0][j])

                time.sleep(self.timeFromSetToGet)

                for l in range(self.noGetters):
                    temp = self.GetFunction[l]()
                    if isinstance(temp, list):
                        self.Data[l][j][i] = temp[0]
                    else:
                        self.Data[l][j][i] = temp

                    if l in self.FreqAxisIndices:
                        self.PlotRawDataSingle(self.Data, self.sweepPar, self.FreqAxiss[self.FreqAxisIndices.index(l)],
                                               self.axHandle, self.figHandle, yselect=l, intervalMaxX1=j,
                                               intervalMaxX2=i, parTitle=self.parTitle, outTitle=self.outTitle)
                    else:
                        self.PlotRawDataLive(self.Data, self.sweepPar, self.axHandle, self.figHandle, yselect=l,
                                             intervalMaxX1=j, intervalMaxX2=i, parTitle=self.parTitle,
                                             outTitle=self.outTitle)
                    # if not(l in self.FreqAxisIndices):
                    #    self.PlotRawDataLive(self.Data,self.sweepPar,self.axHandle,self.figHandle,yselect=l,intervalMaxX1=j,intervalMaxX2=i,parTitle=self.parTitle,outTitle=self.outTitle)
        # input('PRESS ENTER TO END SWEEP...')

    def SaveTxt(self, dataSelect=0, x1Select=-1, x2Select=-1, filename='filename.txt',
                additionalText='var1=?, var2=?'):  # -1 => all values

        if self.noSetters == 1:
            x2Select = 0

        dataPick = np.asarray(self.Data[dataSelect][:][:][:])

        if (x2Select == -1) and (x1Select == -1):
            if dataPick.ndim > 2:
                dummy = 1  # print('Data cannot be array/spectrum when sweeping both '+str(self.parTitle[0])+' and '+str(self.parTitle[1]))
                return 0
            else:
                dataPick = self.FormatDataMatrix(dataPick, self.sweepPar[0][:], self.sweepPar[1][:])
                np.savetxt(filename, dataPick[:, :],
                           header=filename + '\n' + additionalText + '\nData: ' + self.outTitle[
                               dataSelect] + '\n' + str(self.parTitle[0]) + ' \ ' + str(self.parTitle[1]) + ' ()',
                           delimiter='\t')
        elif (x2Select == -1):
            if dataPick.ndim > 2:
                dataPick = dataPick[x1Select, :, :]
                dataPick = self.FormatDataMatrix(dataPick, self.sweepPar[1][:],
                                                 self.FreqAxiss[self.FreqAxisIndices.index(dataSelect)])
                np.savetxt(filename, dataPick[:, :].T,
                           header=filename + '\n' + additionalText + '\nData: ' + self.outTitle[
                               dataSelect] + '\nfreq \ ' + str(self.parTitle[1]) + ' (' + str(
                               self.parTitle[0]) + '=' + str(self.sweepPar[0][x1Select]) + ')', delimiter='\t')
            else:
                dataPick = dataPick[x1Select, :]
                dataPick = np.insert(np.vstack(dataPick), [0], np.vstack(np.asarray(self.sweepPar[1][:])), axis=1)
                np.savetxt(filename, dataPick[:, :],
                           header=filename + '\n' + additionalText + '\nData: ' + self.outTitle[
                               dataSelect] + '\n' + str(self.parTitle[1]) + ' \ none (' + str(
                               self.parTitle[0]) + '=' + str(self.sweepPar[0][x1Select]) + ')', delimiter='\t')
        elif (x1Select == -1):
            if dataPick.ndim > 2:
                dataPick = dataPick[:, x2Select, :]
                dataPick = self.FormatDataMatrix(dataPick, self.sweepPar[0][:],
                                                 self.FreqAxiss[self.FreqAxisIndices.index(dataSelect)])
                np.savetxt(filename, dataPick[:, :].T,
                           header=filename + '\n' + additionalText + '\nData: ' + self.outTitle[
                               dataSelect] + '\nfreq \ ' + str(self.parTitle[0]) + ' (' + str(
                               self.parTitle[1]) + '=' + str(self.sweepPar[1][x2Select]) + ')', delimiter='\t')
            else:
                dataPick = dataPick[:, x2Select]
                dataPick = np.insert(np.vstack(dataPick), [0], np.vstack(np.asarray(self.sweepPar[0][:])), axis=1)
                np.savetxt(filename, dataPick[:, :],
                           header=filename + '\n' + additionalText + '\nData: ' + self.outTitle[
                               dataSelect] + '\n' + str(self.parTitle[0]) + ' \ none (' + str(
                               self.parTitle[1]) + '=' + str(self.sweepPar[1][x2Select]) + ')', delimiter='\t')

    def SaveAllTxt(self, sweepName='SWEEP_NAME', additionalText='*ADDITIONAL INFORMATION*'):
        """
        - DESCRIPTION:
            Save all the data into text files. These are put into a folder labelled from the sweepName parameter

            sweepName : string
                Name of the sweep. Used to label the folder for the sweep data, and it is also used for the prefix of all text files.

            additionalText : string
                Additional text that is written to the second line of all the data text files.
        """
        os.mkdir(sweepName)
        filenamePREFIX = './' + sweepName + '/' + sweepName
        for i in range(self.noGetters):
            succes = self.SaveTxt(dataSelect=i, x1Select=-1, x2Select=-1,
                                  filename=filenamePREFIX + '--' + self.outTitle[i] + '.txt',
                                  additionalText=additionalText)
            if succes == 0:
                for m in range(self.x2_size):
                    self.SaveTxt(dataSelect=i, x1Select=-1, x2Select=m,
                                 filename=filenamePREFIX + '--' + self.outTitle[i] + '--' + self.parTitle[
                                     1] + '=' + str(self.sweepPar[1][m]) + '.txt', additionalText=additionalText)

    def FormatDataMatrix(self, dataMatrix, x1Vector, x2Vector):
        dataMatrixOut = np.insert(dataMatrix, [0], np.vstack(x1Vector), axis=1)
        dummyPar = np.zeros((1, 1 + len(x2Vector)))
        dummyPar[0, 1:] = np.asarray(x2Vector)
        dataMatrixOut = np.insert(dataMatrixOut, [0], dummyPar, axis=0)
        return dataMatrixOut

    def DoNothing(self):
        dummy = 1

    def PlotRawDataLive(self, ydata, xdata, ax0, fig0, yselect=0, intervalMaxX1=1, intervalMaxX2=1,
                        parTitle=['x1', 'x2'], outTitle=[]):

        fig0.canvas.flush_events()
        ax0[yselect].clear()
        x1plot = np.asarray(xdata[0][:])
        x2plot = np.asarray(xdata[1][:])
        x1_size = len(xdata[0][:])
        x2_size = len(xdata[1][:])
        dataplot = np.zeros((x1_size, x2_size))

        for n in range(intervalMaxX2):
            for m in range(x1_size):
                if not (ydata[yselect][m][n] == []):
                    dataplot[m, n] = ydata[yselect][m][n]

        for m in range(intervalMaxX1 + 1):
            if not (ydata[yselect][m][intervalMaxX2] == []):
                dataplot[m, intervalMaxX2] = ydata[yselect][m][intervalMaxX2]

        for i in range(x2_size):
            ax0[yselect].plot(x1plot, dataplot[:, i], label=[parTitle[1] + '=' + str(x2plot[i])])
        plt.xlabel(parTitle[0])
        ax0[yselect].set_ylabel(outTitle[yselect])
        if yselect == 0:
            ax0[yselect].set_title('Sweep monitor')
            ax0[yselect].legend()
        plt.draw()

    def PlotRawDataSingle(self, ydata, xdata, freq, ax0, fig0, yselect=0, intervalMaxX1=1, intervalMaxX2=1,
                          parTitle=['x1', 'x2'], outTitle=[]):

        fig0.canvas.flush_events()
        # ax0[yselect].clear()
        ax0[yselect].clear()
        ax0[yselect].plot(freq, ydata[yselect][intervalMaxX1][intervalMaxX2])
        plt.xlabel('freq')
        ax0[yselect].set_ylabel('dBm/res')

        plt.draw()

    def Plot2DRawDataLive(self, ydata, xdata, freq, ax0, fig0, yselect=0, intervalMaxX1=1, intervalMaxX2=1,
                          parTitle=['x1', 'x2'], outTitle=[]):

        fig0.canvas.flush_events()
        # ax0[yselect].clear()
        x1plot = np.asarray(xdata[0][:])
        x1_size = len(xdata[0][:])
        freq_size = len(freq)
        dataplot = np.zeros((x1_size, freq_size))

        for m in range(intervalMaxX1 + 1):
            if not (ydata[yselect][m][intervalMaxX2] == []):
                dataplot[m, :] = ydata[yselect][m][intervalMaxX2]

        ax0[yselect].pcolor(x1plot[0:(intervalMaxX1 + 1)], freq, dataplot[0:(intervalMaxX1 + 1), :].T)
        plt.xlabel(parTitle[0])
        ax0[yselect].set_ylabel('freq \n(color=' + outTitle[yselect] + ')')

        plt.draw()


class Analyze2D:  # developer: Lars Nielsen
    """
    - DESCRIPTION:
        This class is for reading data from Sweep2D.SaveAllTxt(). This class extracts the data and organizes it into numpy arrays of the working memory.

        sweepName : string
            The name of the sweep. Should correspond to the name used as the argument for Sweep2D.SaveAllTxt(), i.e. the folder name of the sweep.

    - EXAMPLE OF USE:
        EX1 - Generate sweep data from computer defined functions and save the data. Afterwards read the sweep and print the content of on variable.
        import numpy as np
        import matplotlib.pyplot as plt
        import math as math
        john = 0
        john1 = 0
        def set1(inp1=1):
        global john
        john = math.sin((1+john1)*inp1)
        def set2(inp1=1):
            global john1
            john1 = inp1
        def get1():
            global john
            return john
        def get2():
            return [[john,2*john,3],[1,2,3]]
        def get3():
            return [[john,2,3,1,2,3,1,2,3,1,2,3,1,2,2*john],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]]

        SETPARS = [i for i in range(10)]
        SETPARS2 = [10*i for i in range(2)]

        SWEEP0 = PIC_lab_control.Sweep2D(sweepPar=[SETPARS,SETPARS2], SetFunction=[set1,set2],GetFunction=[get1,get2,get3], timeFromSetToGet=0.1,setLabels=['set1label','set2label'], getLabels=['getlabel1','getlabel2','getlabel3'])

        SWEEP0.Run(plotting=True)
        SWEEP0.SaveAllTxt(simulationName= 'simtesting')

        ANA0 = PIC_lab_control.Analyze2D(sweepName='simtesting')
        print(ANA0.GetData('freqaxis:getlabel2'))
    """

    def __init__(self, sweepName='None'):
        self.ylabels = []
        self.xlabels = ['x1']
        # self.data = []
        self.xdata = [[]]
        self.ydata = []
        file_w_spec_indx = []
        y_name_log = []
        varNam = []
        varVal = []
        datalog = []
        specsPresentFlag = 0

        dir_ref = os.getcwd()
        directory = dir_ref + '\\' + sweepName
        file_list = os.listdir(
            directory)  # [name for name in os.listdir(dir_ref+'\\'+directory) if os.path.isfile(name)]
        file_nos = len(file_list)
        for i in range(file_nos):
            if file_list[i].find('--', file_list[i].find('--') + 2) == -1:  # Only one '--'
                indexEq = file_list[i].find('--')
                indexTxt = file_list[i].find('.txt')
                self.ylabels.append(file_list[i][indexEq + 2:indexTxt])
                filename = directory + '\\' + file_list[i]
                data_temp = np.loadtxt(filename)
                tempFile = open(filename, 'r')
                arrLines = tempFile.readlines()
                colRowSep = arrLines[3].find('\\')
                x2End = arrLines[3].find(' (')
                if data_temp.shape[1] > 2:
                    if len(self.xdata) < 2:
                        self.xdata.append(0)
                        self.xlabels.append('empty')
                    if arrLines[3].find('freq') > -1:  # Frequency axis is swapped
                        data_temp = np.transpose(data_temp)
                        self.xdata.append(data_temp[0, 1:])
                        self.xlabels.append('freqaxis:' + self.ylabels[-1])
                    else:
                        self.xdata[1] = data_temp[0, 1:]
                        self.xlabels[1] = arrLines[3][colRowSep + 2:x2End]
                    self.xdata[0] = data_temp[1:, 0]
                    self.xlabels[0] = arrLines[3][2:colRowSep - 1]
                    self.ydata.append(data_temp[1:, 1:])

                    if arrLines[3].find('freq') > -1:  # Frequency axis is swapped
                        self.xlabels[0] = arrLines[3][colRowSep + 2:x2End]
                else:
                    self.xdata[0] = data_temp[:, 0]
                    self.xlabels[0] = arrLines[3][1:colRowSep]
                    self.ydata.append(data_temp[:, 1])
            else:  # Two '--' !!! ----> x1, x2 and spectrums are present at the same time
                file_w_spec_indx.append(i)
                y_name_log.append(
                    file_list[i][file_list[i].find('--') + 2:file_list[i].find('--', file_list[i].find('--') + 2)])
                varNam.append(
                    file_list[i][file_list[i].find('--', file_list[i].find('--') + 2) + 2:file_list[i].find('=')])
                varVal.append(float(file_list[i][file_list[i].find('=') + 1:file_list[i].find('.txt')]))
                filename = directory + '\\' + file_list[i]
                datalog.append(np.transpose(np.loadtxt(filename)))
                specsPresentFlag = 1
                self.xdata[0] = datalog[0][1:, 0]
                # READ x1 label:
                tempFile = open(filename, 'r')
                arrLines = tempFile.readlines()
                colRowSep = arrLines[3].find('\\')
                x2End = arrLines[3].find(' (')
                self.xlabels[0] = arrLines[3][colRowSep + 2:x2End]

        if specsPresentFlag == 1:  # Post processing when x1, x2 and spectrums are present at the same time
            unique = []
            for ele in y_name_log:
                if ele not in unique:
                    unique.append(ele)  # Log each y name only once

            for i in range(len(unique)):
                indexingC = 0
                datatemp = []
                x2temp = []
                x2nametemp = []
                for ww in y_name_log:

                    if ww == unique[i]:
                        datatemp.append(datalog[indexingC][1:, 1:])
                        freqtemp = datalog[indexingC][0, 1:]
                        x2temp.append(varVal[indexingC])
                        x2nametemp = varNam[indexingC]
                    indexingC = indexingC + 1
                if len(self.xdata) > 1:
                    self.xdata[1] = np.asarray(x2temp)
                    self.xlabels[1] = x2nametemp
                else:
                    self.xdata.append(np.asarray(x2temp))
                    self.xlabels.append(x2nametemp)

                self.ydata.append(np.stack(datatemp, axis=1))
                self.xdata.append(freqtemp)
                self.xlabels.append('freqaxis:' + unique[i])
                self.ylabels.append(unique[i])

    def LoadDataTxt(self, filename='None'):
        self.data = np.loadtxt(filename)
        self.x1Label = 'john'
        self.yLabel = 'John1'

        return 1

    def GetXLabels(self):
        return self.xlabels

    def GetYLabels(self):
        return self.ylabels

    def PlotData(self, slice=[-1, -1, -1]):
        Ncol = self.data.shape[1]

        if Ncol == 2:
            fig0 = plt.figure()
            ax0 = fig0.add_subplot(111)
            ax0.plot(self.data[:, 0], self.data[:, 1])
            ax0.set_xlabel(self.x1Label)
            ax0.set_ylabel(self.yLabel)
            return ax0

        elif Ncol > 2:

            print('image plots not accesible yet... to be made')
        else:
            print('No valid data accesible')

        return 1

    def GetData(self, variable='y', index=-1):
        """
        - DESCRIPTION:
            Get the data. This might be either 1D, 2D or 3D, depending on the number of sweep parameters and the nature of the data.
            A single sweep parameter (a single SetFunction) and a single output value from GetFunction will results in 1D.
            Two sweep parameter (two SetFunction's) and a single output value from GetFunction will results in 2D.
            A single sweep parameter (two SetFunction's) and a vector (typically a spectrum) output value from GetFunction will results in 2D.
            Two sweep parameter (two SetFunction's) and a vector (typically a spectrum) output value from GetFunction will results in 3D.

            variable : string
                Label of the variable to extract. Can also be used in combination with the index argument. In this case 'y' refers to output data (GetFunction) and 'x' refers to input data (SetFunction).

            index : integer
                Refers to the index of the variable. i.e. the first sweep parameter x1 will always correspond to GetData(variable='x',index=0). Keep the value at -1 if variable labels are used.

            TIP: the values for the wavelength/frequency axis of an output variable (GetFunction) are stored as 'freqaxis:<getlabel>'
        """
        if index == -1:
            xind = -1
            yind = -1
            for i in range(len(self.GetXLabels())):
                if self.GetXLabels()[i] == variable:
                    xind = i
            for i in range(len(self.GetYLabels())):
                if self.GetYLabels()[i] == variable:
                    yind = i

            if xind > -1:
                variable = 'x'
                index = xind
            elif yind > -1:
                variable = 'y'
                index = yind

        if variable == 'y':
            temp = self.ydata[index]
        elif variable == 'x':
            temp = self.xdata[index]
        else:
            print('ERROR: variable name not recognized')

        return temp

    def GetX1Data(self):
        return self.data[:, 0]

    def GetYData(self):
        return self.data[:, 1:]


class AutomaticAlignment:

    def __init__(self, func_x=[], func_y=[], x_start=[], x_minstep=0.01, settleTime=0.1, eps_or_beta=0.01,
                 stopPercentage=0.001, maxIterations=55, optMethod='SteepestDwBT'):
        # Make sure that x is a list:
        if isinstance(func_x, list):
            self.func_x = func_x
            self.x0 = x_start
        else:
            self.func_x = [func_x]
            self.x0 = [x_start]
        # Give a warning if func_y is a list
        if isinstance(func_y, list):
            print('y_func cannot be a list. Can only optimize to one output')

        for i in range(len(self.func_x)):
            self.func_x[i](self.x0[i])
        self.eps_or_beta = eps_or_beta
        self.func_y = func_y
        self.y0 = self.func_y()
        self.x_minstep = x_minstep
        self.settleTime = settleTime
        self.y1 = [self.y0 for i in range(len(self.func_x))]

        self.stopPercentage = stopPercentage
        self.maxIterations = maxIterations
        self.optMethod = optMethod
        self.stepSizeMem = 1

    def StepSteepestDescent(self):
        for i in range(len(self.func_x)):
            self.func_x[i](self.x0[i] + self.x_minstep)
            time.sleep(self.settleTime)  # Wait for x set function to settle
            self.y1[i] = self.func_y()

        # print(self.y0)
        grady = [(self.y1[i] - self.y0) / self.x_minstep for i in range(len(self.y1))]
        normgrady = math.sqrt(sum([grady[i] ** 2 for i in range(len(grady))]))
        xtemp = [self.x0[i] + (self.eps_or_beta / normgrady) * grady[i] for i in range(len(grady))]
        self.x0 = xtemp
        for i in range(len(self.func_x)):
            self.func_x[i](self.x0[i])
        time.sleep(self.settleTime)
        self.y0 = self.func_y()

        return grady

    def StepSteepestDescentwBacktracking(self):

        for i in range(len(self.func_x)):
            self.func_x[i](self.x0[i] + self.x_minstep)
            time.sleep(self.settleTime)  # Wait for x set function to settle
            self.y1[i] = self.func_y()

        # print(self.y0)
        grady = [(self.y1[i] - self.y0) / self.x_minstep for i in range(len(self.y1))]

        normgrady = math.sqrt(sum([grady[i] ** 2 for i in range(len(grady))]))
        adaptY0 = -1
        adaptY0old = -1
        xtemp = self.x0
        t = 1
        counter = 0
        percY = 1
        breakNext = 0
        while (adaptY0 < (self.y0 + t * 0.5 * (normgrady ** 2))) and percY > self.stopPercentage:
            xtemp = [self.x0[i] + t * (grady[i] / normgrady) for i in range(len(grady))]

            for i in range(len(self.func_x)):
                self.func_x[i](xtemp[i])
            time.sleep(self.settleTime)
            adaptY0 = self.func_y()
            t = t * self.eps_or_beta
            if t < 0.0025:  # minimum resoltion of PZs
                t = 0.0025
                if breakNext == 1:
                    break
                breakNext = 1

            counter = counter + 1
            deltaYadapt = adaptY0 - adaptY0old
            percY = abs(deltaYadapt / adaptY0old)
            adaptY0old = adaptY0
            print(xtemp)
        self.x0 = xtemp
        self.y0 = adaptY0

        return grady

    def HookJeeves(self):
        # Explore
        stepLength = self.stepSizeMem * self.eps_or_beta
        xtemp = self.x0
        changeFlag = 0
        ytemp = 0

        for i in range(len(self.func_x)):
            for m in range(2):  # plus minus check
                if m < 1:
                    self.func_x[i](self.x0[i] + stepLength)
                    time.sleep(self.settleTime)
                    ytemp = self.func_y()
                    if ytemp > self.y0:
                        xtemp[i] = xtemp[i] + stepLength
                        changeFlag = 1
                        break
                else:
                    self.func_x[i](self.x0[i] - stepLength)
                    time.sleep(self.settleTime)
                    ytemp = self.func_y()
                    if ytemp > self.y0:
                        xtemp[i] = xtemp[i] - stepLength
                        changeFlag = 1

        if changeFlag == 1:
            # Pattern move:
            for i in range(len(self.func_x)):
                self.func_x[i](self.x0[i] + 2 * (xtemp[i] - self.x0[i]))
            time.sleep(self.settleTime)  # Wait for x set function to settle
            ytempp = self.func_y()
            if ytempp > ytemp:
                for i in range(len(self.func_x)):
                    self.x0[i] = self.x0[i] + 2 * (xtemp[i] - self.x0[i])
                    self.y0 = ytempp
                else:
                    self.x0 = xtemp
                    self.y0 = ytemp

        print(self.x0)

        if changeFlag == 0:
            for i in range(len(self.func_x)):
                self.func_x[i](self.x0[i])
            self.stepSizeMem = self.stepSizeMem * (1 / 10)
            print('StepReduced:', str(self.stepSizeMem))

        if self.stepSizeMem < self.x_minstep:
            return 2

        return changeFlag

    def Align(self):
        # Variables for algorithm:
        counter = 0
        percY = 1
        Yold = -10
        updatePerc = 0
        # Do the alignment until the change in percentage is too small or maximum iterations have been reached
        while (counter < self.maxIterations) and (
                percY > self.stopPercentage):  # (monitorGrad*self.eps>self.x_minstep) and (counter<100):
            if updatePerc == 1:
                Yold = self.y0  # Save old value for objective function
            updatePerc = 1
            if self.optMethod == 'SteepestDwBT':
                self.StepSteepestDescentwBacktracking()  # Do the
            elif self.optMethod == 'SteepestD':
                self.StepSteepestDescent()
            elif self.optMethod == 'HookJeeves':
                ret0 = self.HookJeeves()
                if ret0 == 0:
                    updatePerc = 0
                elif ret0 == 2:
                    # step size is the smallest - can do nothing more
                    break
            percY = abs((self.y0 - Yold) / Yold)
            counter = counter + 1

        print('Finished in ' + str(counter) + ' steps')
        return self.x0  # return the x0 value at the optimized position


# Classes for the communication layer:#######################
class socketInstrument:  # developer: Lars Nielsen
    def __init__(self, ip_address='192.168.1.3', tcp_port=5025, timeoutVal=120):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip_address, tcp_port))
        self.s.settimeout(timeoutVal)

    def write(self, command='*IDN?'):
        self.s.send((command + "\r\n").encode())

    def read(self):
        endFlag = 0
        data = ''
        while endFlag == 0:
            data = data + self.s.recv(1).decode()
            if data[-1] == '\n':
                break

        return data[:(len(data) - 1)]

    def query(self, command):
        self.write(command)

        return self.read()

    def query_ascii_values(self, command):
        self.write(command)

        return np.array(self.read().split(',')).astype(np.float).tolist()

    def close(self):
        self.s.close()


# %% Email Class
class Email():  # also need to include imghdr
    '''    Developed by Mircea Balauroiu for v1.08.
    Please include the receiver e-mail address in the constructor.
    Use the sendMail method to send an email to the receiver.'''
    __senderMail = "saduohgnr2u4we32@gmail.com"  # Sender email (random gmail account)
    __senderPwd = "awsre3245trfevd cz"  # Sender email password

    def __init__(self, receiver):  # in the contructor we only need the receiver address
        self.receiver = receiver

    def sendMail(self, subject, body,
                 *picturePath):  # Specify a Title, a body, and optional the absolute path of pictures<-- ALL AS STRINGS
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.__senderMail, self.__senderPwd)
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.__senderMail
            msg['To'] = self.receiver
            msg.set_content(body)
            if picturePath:
                for files in picturePath:
                    with open(files, 'rb') as picture:
                        fileType = imghdr.what(picture.name)
                        fileName = picture.name
                        fileData = picture.read()
                        msg.add_attachment(fileData, maintype='image', subtype=fileType, filename=fileName)
            smtp.send_message(msg)


# %%GPIB sniffer
def showResources():  # Just call the function and you should get the devices connected over GPIB
    resources = pyvisa.ResourceManager().list_resources()  # get a list of all the connected devices
    resources = sorted(resources)  # sort the list
    print("\nConnected Devices_________________________________")
    print("[ASRL DEVICES]....................................")
    for i in resources:
        if str(i).find("ASRL") > -1:
            print(" -->|ASRL| {ADR:" + i[0:i.find("::")] + "}")
    print("[GPIB DEVICES]....................................")
    for i in resources:
        if i.find("GPIB") > -1:
            print(" -->|GPIB| [Port:" + i[4:i.find("::")] + "] {ADR:" + i[i.find("::") + 2:i.find("::", i.find(
                "::") + 1)] + "}")
    print("[TCPIP DEVICES]...................................")
    for i in resources:
        if i.find("TCP") > -1:
            print(" -->|TCP| {ADR:" + i[i.find("::") + 2:i.find("::", i.find("::") + 2)] + "}")
    print("[Other DEVICES]...................................")
    for i in resources:
        if i.find("TCP") == -1 and i.find("GPIB") == -1 and i.find("ASRL") == -1:
            print(" -->", i)
    print("__________________________________________________")


# %%Quick 1D live plotting
def livePlotting(x, y, name="Dynamic plot", xLabel="Input", yLabel="Output", pause=0.001):
    # One has to input the x and y arrays
    # Also optionally, one can define the name of the plot,xlable,ylabel and pause time
    plt.ion()
    plt.figure(name)
    plt.clf()
    plt.axis((min(x), max(x), min(y), max(y)))
    plt.plot(x, y)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()
    plt.pause(pause)
    return plt


# Third party classes and functions:

# TLPM class which is needed by the PM100USB class

class TLPM:  # Added by Lars

    def __init__(self):
        if sizeof(c_voidp) == 4:
            self.dll = cdll.LoadLibrary("TLPM_32.dll")
        else:
            self.dll = cdll.LoadLibrary("TLPM_64.dll")

        self.devSession = c_long()
        self.devSession.value = 0

    def __testForError(self, status):
        if status < 0:
            self.__throwError(status)
        return status

    def __throwError(self, code):
        msg = create_string_buffer(1024)
        self.dll.TLPM_errorMessage(self.devSession, c_int(code), msg)
        raise NameError(c_char_p(msg.raw).value)

    def open(self, resourceName, IDQuery, resetDevice):
        """
        This function initializes the instrument driver session and performs the following initialization actions:



        (1) Opens a session to the Default Resource Manager resource and a session to the specified device using the Resource Name.

        (2) Performs an identification query on the instrument.

        (3) Resets the instrument to a known state.

        (4) Sends initialization commands to the instrument.

        (5) Returns an instrument handle which is used to distinguish between different sessions of this instrument driver.



        Notes:

        (1) Each time this function is invoked a unique session is opened.

        Args:
            resourceName (create_string_buffer)
            IDQuery (c_bool):This parameter specifies whether an identification query is performed during the initialization process.



            VI_OFF (0): Skip query.

            VI_ON  (1): Do query (default).


            resetDevice (c_bool):This parameter specifies whether the instrument is reset during the initialization process.



            VI_OFF (0) - no reset

            VI_ON  (1) - instrument is reset (default)


        Returns:
            int: The return value, 0 is for success
        """
        self.dll.TLPM_close(self.devSession)
        self.devSession.value = 0
        pInvokeResult = self.dll.TLPM_init(resourceName, IDQuery, resetDevice, byref(self.devSession))
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def close(self):
        """
        This function closes the instrument driver session.



        Note: The instrument must be reinitialized to use it again.

        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_close(self.devSession)
        return pInvokeResult

    def findRsrc(self, resourceCount):
        """
        This function finds all driver compatible devices attached to the PC and returns the number of found devices.



        Note:

        (1) The function additionally stores information like system name about the found resources internally. This information can be retrieved with further functions from the class, e.g. <Get Resource Description> and <Get Resource Information>.



        Args:
            resourceCount(c_int use with byref) : The number of connected devices that are supported by this driver.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_findRsrc(self.devSession, resourceCount)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getRsrcName(self, index, resourceName):
        """
        This function gets the resource name string needed to open a device with <Initialize>.



        Notes:

        (1) The data provided by this function was updated at the last call of <Find Resources>.

        Args:
            index(c_int) : This parameter accepts the index of the device to get the resource descriptor from.



            Notes:

            (1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.


            resourceName(create_string_buffer) : This parameter returns the resource descriptor. Use this descriptor to specify the device in <Initialize>.



            Notes:

            (1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getRsrcName(self.devSession, index, resourceName)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getRsrcInfo(self, index, modelName, serialNumber, manufacturer, deviceAvailable):
        """
        This function gets information about a connected resource.



        Notes:

        (1) The data provided by this function was updated at the last call of <Find Resources>.

        Args:
            index(c_int) : This parameter accepts the index of the device to get the resource descriptor from.



            Notes:

            (1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.


            modelName(create_string_buffer) : This parameter returns the model name of the device.



            Notes:

            (1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].

            (2) You may pass VI_NULL if you do not need this parameter.

            (3) Serial interfaces over Bluetooth will return the interface name instead of the device model name.
            serialNumber(create_string_buffer) : This parameter returns the serial number of the device.



            Notes:

            (1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].

            (2) You may pass VI_NULL if you do not need this parameter.

            (3) The serial number is not available for serial interfaces over Bluetooth.
            manufacturer(create_string_buffer) : This parameter returns the manufacturer name of the device.



            Notes:

            (1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].

            (2) You may pass VI_NULL if you do not need this parameter.

            (3) The manufacturer name is not available for serial interfaces over Bluetooth.
            deviceAvailable(c_int16 use with byref) : Returns the information if the device is available.

            Devices that are not available are used by other applications.



            Notes:

            (1) You may pass VI_NULL if you do not need this parameter.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getRsrcInfo(self.devSession, index, modelName, serialNumber, manufacturer,
                                                  deviceAvailable)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def writeRegister(self, reg, value):
        """
        This function writes the content of any writable instrument register. Refer to your instrument's user's manual for more details on status structure registers.



        Args:
            reg(c_int16) : Specifies the register to be used for operation. This parameter can be any of the following constants:



              TLPM_REG_SRE         (1): Service Request Enable

              TLPM_REG_ESE         (3): Standard Event Enable

              TLPM_REG_OPER_ENAB   (6): Operation Event Enable Register

              TLPM_REG_OPER_PTR    (7): Operation Positive Transition

              TLPM_REG_OPER_NTR    (8): Operation Negative Transition

              TLPM_REG_QUES_ENAB  (11): Questionable Event Enable Reg.

              TLPM_REG_QUES_PTR   (12): Questionable Positive Transition

              TLPM_REG_QUES_NTR   (13): Questionable Negative Transition

              TLPM_REG_MEAS_ENAB  (16): Measurement Event Enable Register

              TLPM_REG_MEAS_PTR   (17): Measurement Positive Transition

              TLPM_REG_MEAS_NTR   (18): Measurement Negative Transition

              TLPM_REG_AUX_ENAB   (21): Auxiliary Event Enable Register

              TLPM_REG_AUX_PTR    (22): Auxiliary Positive Transition

              TLPM_REG_AUX_NTR    (23): Auxiliary Negative Transition


            value(c_int16) : This parameter specifies the new value of the selected register.



            These register bits are defined:



            STATUS BYTE bits (see IEEE488.2-1992 §11.2)

            TLPM_STATBIT_STB_AUX        (0x01): Auxiliary summary

            TLPM_STATBIT_STB_MEAS       (0x02): Device Measurement Summary

            TLPM_STATBIT_STB_EAV        (0x04): Error available

            TLPM_STATBIT_STB_QUES       (0x08): Questionable Status Summary

            TLPM_STATBIT_STB_MAV        (0x10): Message available

            TLPM_STATBIT_STB_ESB        (0x20): Event Status Bit

            TLPM_STATBIT_STB_MSS        (0x40): Master summary status

            TLPM_STATBIT_STB_OPER       (0x80): Operation Status Summary



            STANDARD EVENT STATUS REGISTER bits (see IEEE488.2-1992 §11.5.1)

            TLPM_STATBIT_ESR_OPC        (0x01): Operation complete

            TLPM_STATBIT_ESR_RQC        (0x02): Request control

            TLPM_STATBIT_ESR_QYE        (0x04): Query error

            TLPM_STATBIT_ESR_DDE        (0x08): Device-Specific error

            TLPM_STATBIT_ESR_EXE        (0x10): Execution error

            TLPM_STATBIT_ESR_CME        (0x20): Command error

            TLPM_STATBIT_ESR_URQ        (0x40): User request

            TLPM_STATBIT_ESR_PON        (0x80): Power on



            QUESTIONABLE STATUS REGISTER bits (see SCPI 99.0 §9)

            TLPM_STATBIT_QUES_VOLT      (0x0001): Questionable voltage measurement

            TLPM_STATBIT_QUES_CURR      (0x0002): Questionable current measurement

            TLPM_STATBIT_QUES_TIME      (0x0004): Questionable time measurement

            TLPM_STATBIT_QUES_POW       (0x0008): Questionable power measurement

            TLPM_STATBIT_QUES_TEMP      (0x0010): Questionable temperature measurement

            TLPM_STATBIT_QUES_FREQ      (0x0020): Questionable frequency measurement

            TLPM_STATBIT_QUES_PHAS      (0x0040): Questionable phase measurement

            TLPM_STATBIT_QUES_MOD       (0x0080): Questionable modulation measurement

            TLPM_STATBIT_QUES_CAL       (0x0100): Questionable calibration

            TLPM_STATBIT_QUES_ENER      (0x0200): Questionable energy measurement

            TLPM_STATBIT_QUES_10        (0x0400): Reserved

            TLPM_STATBIT_QUES_11        (0x0800): Reserved

            TLPM_STATBIT_QUES_12        (0x1000): Reserved

            TLPM_STATBIT_QUES_INST      (0x2000): Instrument summary

            TLPM_STATBIT_QUES_WARN      (0x4000): Command warning

            TLPM_STATBIT_QUES_15        (0x8000): Reserved



            OPERATION STATUS REGISTER bits (see SCPI 99.0 §9)

            TLPM_STATBIT_OPER_CAL       (0x0001): The instrument is currently performing a calibration.

            TLPM_STATBIT_OPER_SETT      (0x0002): The instrument is waiting for signals to stabilize for measurements.

            TLPM_STATBIT_OPER_RANG      (0x0004): The instrument is currently changing its range.

            TLPM_STATBIT_OPER_SWE       (0x0008): A sweep is in progress.

            TLPM_STATBIT_OPER_MEAS      (0x0010): The instrument is actively measuring.

            TLPM_STATBIT_OPER_TRIG      (0x0020): The instrument is in a “wait for trigger” state of the trigger model.

            TLPM_STATBIT_OPER_ARM       (0x0040): The instrument is in a “wait for arm” state of the trigger model.

            TLPM_STATBIT_OPER_CORR      (0x0080): The instrument is currently performing a correction (Auto-PID tune).

            TLPM_STATBIT_OPER_SENS      (0x0100): Optical powermeter sensor connected and operable.

            TLPM_STATBIT_OPER_DATA      (0x0200): Measurement data ready for fetch.

            TLPM_STATBIT_OPER_THAC      (0x0400): Thermopile accelerator active.

            TLPM_STATBIT_OPER_11        (0x0800): Reserved

            TLPM_STATBIT_OPER_12        (0x1000): Reserved

            TLPM_STATBIT_OPER_INST      (0x2000): One of n multiple logical instruments is reporting OPERational status.

            TLPM_STATBIT_OPER_PROG      (0x4000): A user-defined programming is currently in the run state.

            TLPM_STATBIT_OPER_15        (0x8000): Reserved



            Thorlabs defined MEASRUEMENT STATUS REGISTER bits

            TLPM_STATBIT_MEAS_0         (0x0001): Reserved

            TLPM_STATBIT_MEAS_1         (0x0002): Reserved

            TLPM_STATBIT_MEAS_2         (0x0004): Reserved

            TLPM_STATBIT_MEAS_3         (0x0008): Reserved

            TLPM_STATBIT_MEAS_4         (0x0010): Reserved

            TLPM_STATBIT_MEAS_5         (0x0020): Reserved

            TLPM_STATBIT_MEAS_6         (0x0040): Reserved

            TLPM_STATBIT_MEAS_7         (0x0080): Reserved

            TLPM_STATBIT_MEAS_8         (0x0100): Reserved

            TLPM_STATBIT_MEAS_9         (0x0200): Reserved

            TLPM_STATBIT_MEAS_10        (0x0400): Reserved

            TLPM_STATBIT_MEAS_11        (0x0800): Reserved

            TLPM_STATBIT_MEAS_12        (0x1000): Reserved

            TLPM_STATBIT_MEAS_13        (0x2000): Reserved

            TLPM_STATBIT_MEAS_14        (0x4000): Reserved

            TLPM_STATBIT_MEAS_15        (0x8000): Reserved



            Thorlabs defined Auxiliary STATUS REGISTER bits

            TLPM_STATBIT_AUX_NTC        (0x0001): Auxiliary NTC temperature sensor connected.

            TLPM_STATBIT_AUX_EMM        (0x0002): External measurement module connected.

            TLPM_STATBIT_AUX_2          (0x0004): Reserved

            TLPM_STATBIT_AUX_3          (0x0008): Reserved

            TLPM_STATBIT_AUX_EXPS       (0x0010): External power supply connected

            TLPM_STATBIT_AUX_BATC       (0x0020): Battery charging

            TLPM_STATBIT_AUX_BATL       (0x0040): Battery low

            TLPM_STATBIT_AUX_IPS        (0x0080): Apple(tm) authentification supported.

            TLPM_STATBIT_AUX_IPF        (0x0100): Apple(tm) authentification failed.

            TLPM_STATBIT_AUX_9          (0x0200): Reserved

            TLPM_STATBIT_AUX_10         (0x0400): Reserved

            TLPM_STATBIT_AUX_11         (0x0800): Reserved

            TLPM_STATBIT_AUX_12         (0x1000): Reserved

            TLPM_STATBIT_AUX_13         (0x2000): Reserved

            TLPM_STATBIT_AUX_14         (0x4000): Reserved

            TLPM_STATBIT_AUX_15         (0x8000): Reserved


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_writeRegister(self.devSession, reg, value)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def readRegister(self, reg, value):
        """
        This function reads the content of any readable instrument register. Refer to your instrument's user's manual for more details on status structure registers.



        Args:
            reg(c_int16) : Specifies the register to be used for operation. This parameter can be any of the following constants:



              TLPM_REG_STB         (0): Status Byte Register

              TLPM_REG_SRE         (1): Service Request Enable

              TLPM_REG_ESB         (2): Standard Event Status Register

              TLPM_REG_ESE         (3): Standard Event Enable

              TLPM_REG_OPER_COND   (4): Operation Condition Register

              TLPM_REG_OPER_EVENT  (5): Operation Event Register

              TLPM_REG_OPER_ENAB   (6): Operation Event Enable Register

              TLPM_REG_OPER_PTR    (7): Operation Positive Transition

              TLPM_REG_OPER_NTR    (8): Operation Negative Transition

              TLPM_REG_QUES_COND   (9): Questionable Condition Register

              TLPM_REG_QUES_EVENT (10): Questionable Event Register

              TLPM_REG_QUES_ENAB  (11): Questionable Event Enable Reg.

              TLPM_REG_QUES_PTR   (12): Questionable Positive Transition

              TLPM_REG_QUES_NTR   (13): Questionable Negative Transition

              TLPM_REG_MEAS_COND  (14): Measurement Condition Register

              TLPM_REG_MEAS_EVENT (15): Measurement Event Register

              TLPM_REG_MEAS_ENAB  (16): Measurement Event Enable Register

              TLPM_REG_MEAS_PTR   (17): Measurement Positive Transition

              TLPM_REG_MEAS_NTR   (18): Measurement Negative Transition

              TLPM_REG_AUX_COND   (19): Auxiliary Condition Register

              TLPM_REG_AUX_EVENT  (20): Auxiliary Event Register

              TLPM_REG_AUX_ENAB   (21): Auxiliary Event Enable Register

              TLPM_REG_AUX_PTR    (22): Auxiliary Positive Transition

              TLPM_REG_AUX_NTR    (23): Auxiliary Negative Transition


            value(c_int16 use with byref) : This parameter returns the value of the selected register.



            These register bits are defined:



            STATUS BYTE bits (see IEEE488.2-1992 §11.2)

            TLPM_STATBIT_STB_AUX        (0x01): Auxiliary summary

            TLPM_STATBIT_STB_MEAS       (0x02): Device Measurement Summary

            TLPM_STATBIT_STB_EAV        (0x04): Error available

            TLPM_STATBIT_STB_QUES       (0x08): Questionable Status Summary

            TLPM_STATBIT_STB_MAV        (0x10): Message available

            TLPM_STATBIT_STB_ESB        (0x20): Event Status Bit

            TLPM_STATBIT_STB_MSS        (0x40): Master summary status

            TLPM_STATBIT_STB_OPER       (0x80): Operation Status Summary



            STANDARD EVENT STATUS REGISTER bits (see IEEE488.2-1992 §11.5.1)

            TLPM_STATBIT_ESR_OPC        (0x01): Operation complete

            TLPM_STATBIT_ESR_RQC        (0x02): Request control

            TLPM_STATBIT_ESR_QYE        (0x04): Query error

            TLPM_STATBIT_ESR_DDE        (0x08): Device-Specific error

            TLPM_STATBIT_ESR_EXE        (0x10): Execution error

            TLPM_STATBIT_ESR_CME        (0x20): Command error

            TLPM_STATBIT_ESR_URQ        (0x40): User request

            TLPM_STATBIT_ESR_PON        (0x80): Power on



            QUESTIONABLE STATUS REGISTER bits (see SCPI 99.0 §9)

            TLPM_STATBIT_QUES_VOLT      (0x0001): Questionable voltage measurement

            TLPM_STATBIT_QUES_CURR      (0x0002): Questionable current measurement

            TLPM_STATBIT_QUES_TIME      (0x0004): Questionable time measurement

            TLPM_STATBIT_QUES_POW       (0x0008): Questionable power measurement

            TLPM_STATBIT_QUES_TEMP      (0x0010): Questionable temperature measurement

            TLPM_STATBIT_QUES_FREQ      (0x0020): Questionable frequency measurement

            TLPM_STATBIT_QUES_PHAS      (0x0040): Questionable phase measurement

            TLPM_STATBIT_QUES_MOD       (0x0080): Questionable modulation measurement

            TLPM_STATBIT_QUES_CAL       (0x0100): Questionable calibration

            TLPM_STATBIT_QUES_ENER      (0x0200): Questionable energy measurement

            TLPM_STATBIT_QUES_10        (0x0400): Reserved

            TLPM_STATBIT_QUES_11        (0x0800): Reserved

            TLPM_STATBIT_QUES_12        (0x1000): Reserved

            TLPM_STATBIT_QUES_INST      (0x2000): Instrument summary

            TLPM_STATBIT_QUES_WARN      (0x4000): Command warning

            TLPM_STATBIT_QUES_15        (0x8000): Reserved



            OPERATION STATUS REGISTER bits (see SCPI 99.0 §9)

            TLPM_STATBIT_OPER_CAL       (0x0001): The instrument is currently performing a calibration.

            TLPM_STATBIT_OPER_SETT      (0x0002): The instrument is waiting for signals to stabilize for measurements.

            TLPM_STATBIT_OPER_RANG      (0x0004): The instrument is currently changing its range.

            TLPM_STATBIT_OPER_SWE       (0x0008): A sweep is in progress.

            TLPM_STATBIT_OPER_MEAS      (0x0010): The instrument is actively measuring.

            TLPM_STATBIT_OPER_TRIG      (0x0020): The instrument is in a “wait for trigger” state of the trigger model.

            TLPM_STATBIT_OPER_ARM       (0x0040): The instrument is in a “wait for arm” state of the trigger model.

            TLPM_STATBIT_OPER_CORR      (0x0080): The instrument is currently performing a correction (Auto-PID tune).

            TLPM_STATBIT_OPER_SENS      (0x0100): Optical powermeter sensor connected and operable.

            TLPM_STATBIT_OPER_DATA      (0x0200): Measurement data ready for fetch.

            TLPM_STATBIT_OPER_THAC      (0x0400): Thermopile accelerator active.

            TLPM_STATBIT_OPER_11        (0x0800): Reserved

            TLPM_STATBIT_OPER_12        (0x1000): Reserved

            TLPM_STATBIT_OPER_INST      (0x2000): One of n multiple logical instruments is reporting OPERational status.

            TLPM_STATBIT_OPER_PROG      (0x4000): A user-defined programming is currently in the run state.

            TLPM_STATBIT_OPER_15        (0x8000): Reserved



            Thorlabs defined MEASRUEMENT STATUS REGISTER bits

            TLPM_STATBIT_MEAS_0         (0x0001): Reserved

            TLPM_STATBIT_MEAS_1         (0x0002): Reserved

            TLPM_STATBIT_MEAS_2         (0x0004): Reserved

            TLPM_STATBIT_MEAS_3         (0x0008): Reserved

            TLPM_STATBIT_MEAS_4         (0x0010): Reserved

            TLPM_STATBIT_MEAS_5         (0x0020): Reserved

            TLPM_STATBIT_MEAS_6         (0x0040): Reserved

            TLPM_STATBIT_MEAS_7         (0x0080): Reserved

            TLPM_STATBIT_MEAS_8         (0x0100): Reserved

            TLPM_STATBIT_MEAS_9         (0x0200): Reserved

            TLPM_STATBIT_MEAS_10        (0x0400): Reserved

            TLPM_STATBIT_MEAS_11        (0x0800): Reserved

            TLPM_STATBIT_MEAS_12        (0x1000): Reserved

            TLPM_STATBIT_MEAS_13        (0x2000): Reserved

            TLPM_STATBIT_MEAS_14        (0x4000): Reserved

            TLPM_STATBIT_MEAS_15        (0x8000): Reserved



            Thorlabs defined Auxiliary STATUS REGISTER bits

            TLPM_STATBIT_AUX_NTC        (0x0001): Auxiliary NTC temperature sensor connected.

            TLPM_STATBIT_AUX_EMM        (0x0002): External measurement module connected.

            TLPM_STATBIT_AUX_2          (0x0004): Reserved

            TLPM_STATBIT_AUX_3          (0x0008): Reserved

            TLPM_STATBIT_AUX_EXPS       (0x0010): External power supply connected

            TLPM_STATBIT_AUX_BATC       (0x0020): Battery charging

            TLPM_STATBIT_AUX_BATL       (0x0040): Battery low

            TLPM_STATBIT_AUX_IPS        (0x0080): Apple(tm) authentification supported.

            TLPM_STATBIT_AUX_IPF        (0x0100): Apple(tm) authentification failed.

            TLPM_STATBIT_AUX_9          (0x0200): Reserved

            TLPM_STATBIT_AUX_10         (0x0400): Reserved

            TLPM_STATBIT_AUX_11         (0x0800): Reserved

            TLPM_STATBIT_AUX_12         (0x1000): Reserved

            TLPM_STATBIT_AUX_13         (0x2000): Reserved

            TLPM_STATBIT_AUX_14         (0x4000): Reserved

            TLPM_STATBIT_AUX_15         (0x8000): Reserved


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_readRegister(self.devSession, reg, value)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def presetRegister(self):
        """
        This function presets all status registers to default.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_presetRegister(self.devSession)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setTime(self, year, month, day, hour, minute, second):
        """
        This function sets the system date and time of the powermeter.



        Notes:

        (1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.

        (2) The function is only available on PM100D, PM200, PM400.

        Args:
            year(c_int16) : This parameter specifies the actual year in the format yyyy e.g. 2009.
            month(c_int16) : This parameter specifies the actual month in the format mm e.g. 01.
            day(c_int16) : This parameter specifies the actual day in the format dd e.g. 15.


            hour(c_int16) : This parameter specifies the actual hour in the format hh e.g. 14.


            minute(c_int16) : This parameter specifies the actual minute in the format mm e.g. 43.


            second(c_int16) : This parameter specifies the actual second in the format ss e.g. 50.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setTime(self.devSession, year, month, day, hour, minute, second)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getTime(self, year, month, day, hour, minute, second):
        """
        This function returns the system date and time of the powermeter.



        Notes:

        (1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.

        (2) The function is only available on PM100D, PM200, PM400.

        Args:
            year(c_int16 use with byref) : This parameter specifies the actual year in the format yyyy.
            month(c_int16 use with byref) : This parameter specifies the actual month in the format mm.
            day(c_int16 use with byref) : This parameter specifies the actual day in the format dd.
            hour(c_int16 use with byref) : This parameter specifies the actual hour in the format hh.
            minute(c_int16 use with byref) : This parameter specifies the actual minute in the format mm.
            second(c_int16 use with byref) : This parameter specifies the actual second in the format ss.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getTime(self.devSession, year, month, day, hour, minute, second)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setLineFrequency(self, lineFrequency):
        """
        This function selects the line frequency.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200.



        Args:
            lineFrequency(c_int16) : This parameter specifies the line frequency.



            Accepted values:

              TLPM_LINE_FREQ_50 (50): 50Hz

              TLPM_LINE_FREQ_60 (60): 60Hz




        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setLineFrequency(self.devSession, lineFrequency)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getLineFrequency(self, lineFrequency):
        """
        This function returns the selected line frequency.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200.



        Args:
            lineFrequency(c_int16 use with byref) : This parameter returns the selected line frequency in Hz.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getLineFrequency(self.devSession, lineFrequency)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getBatteryVoltage(self, voltage):
        """
        This function is used to obtain the battery voltage readings from the instrument.



        Remark:

        (1) This function is only supported with the PM160 and PM160T.

        (2) This function obtains the latest battery voltage measurement result.

        (3) With the USB cable connected this function will obtain the loading voltage. Only with USB cable disconnected (Bluetooth connection) the actual battery voltage can be read.

        Args:
            voltage(c_double use with byref) : This parameter returns the battery voltage in volts [V].
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getBatteryVoltage(self.devSession, voltage)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setDispBrightness(self, val):
        """
        This function sets the display brightness.

        Args:
            val(c_double) : This parameter specifies the display brightness.



            Range   : 0.0 .. 1.0

            Default : 1.0


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setDispBrightness(self.devSession, val)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getDispBrightness(self, pVal):
        """
        This function returns the display brightness.



        Args:
            pVal(c_double use with byref) : This parameter returns the display brightness. Value range is 0.0 to 1.0.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getDispBrightness(self.devSession, pVal)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setDispContrast(self, val):
        """
        This function sets the display contrast of a PM100D.



        Note: The function is available on PM100D only.

        Args:
            val(c_double) : This parameter specifies the display contrast.



            Range   : 0.0 .. 1.0

            Default : 0.5


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setDispContrast(self.devSession, val)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getDispContrast(self, pVal):
        """
        This function returns the display contrast of a PM100D.



        Note: This function is available on PM100D only

        Args:
            pVal(c_double use with byref) : This parameter returns the display contrast (0..1).
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getDispContrast(self.devSession, pVal)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setInputFilterState(self, inputFilterState):
        """
        This function sets the instrument's photodiode input filter state.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.



        Args:
            inputFilterState(c_int16) : This parameter specifies the input filter mode.



            Acceptable values:

              TLPM_INPUT_FILTER_STATE_OFF (0) input filter off

              TLPM_INPUT_FILTER_STATE_ON  (1) input filter on
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setInputFilterState(self.devSession, inputFilterState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getInputFilterState(self, inputFilterState):
        """
        This function returns the instrument's photodiode input filter state.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.



        Args:
            inputFilterState(c_int16 use with byref) : This parameter returns the input filter state.



            Return values:

              TLPM_INPUT_FILTER_STATE_OFF (0) input filter off

              TLPM_INPUT_FILTER_STATE_ON  (1) input filter on


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getInputFilterState(self.devSession, inputFilterState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setAccelState(self, accelState):
        """
        This function sets the thermopile acceleration state.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200.



        Args:
            accelState(c_int16) : This parameter specifies the thermopile acceleration mode.



            Acceptable values:

              TLPM_ACCELERATION_STATE_OFF (0): thermopile acceleration off

              TLPM_ACCELERATION_STATE_ON  (1): thermopile acceleration on


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setAccelState(self.devSession, accelState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAccelState(self, accelState):
        """
        This function returns the thermopile acceleration state.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            accelState(c_int16 use with byref) : This parameter returns the thermopile acceleration mode.



            Return values:

              TLPM_ACCELERATION_STATE_OFF (0): thermopile acceleration off

              TLPM_ACCELERATION_STATE_ON  (1): thermopile acceleration on


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAccelState(self.devSession, accelState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setAccelMode(self, accelMode):
        """
        This function sets the thermopile acceleration auto mode.



        While thermopile acceleration improves displaying changing measurement values it unfortunately adds extra noise which can become noticeable on constant values measurements. With acceleration mode set to AUTO the instrument enables the acceleration circuitry after big measurement value changes for five times of "Tau". See also functions <Set Thermopile Accelerator Tau> and <Set Thermopile Accelerator State>.



        With calling <Set Thermopile Accelerator State> the accelerator mode will always be reset to MANUAL.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            accelMode(c_int16) : This parameter specifies the thermopile acceleration mode.



            Acceptable values:

              TLPM_ACCELERATION_MANUAL (0): auto acceleration off

              TLPM_ACCELERATION_AUTO   (1): auto acceleration on


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setAccelMode(self.devSession, accelMode)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAccelMode(self, accelMode):
        """
        This function returns the thermopile acceleration mode.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            accelMode(c_int16 use with byref) : This parameter returns the thermopile acceleration mode.



            Return values:

              TLPM_ACCELERATION_MANUAL (0): auto acceleration off

              TLPM_ACCELERATION_AUTO   (1): auto acceleration on


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAccelMode(self.devSession, accelMode)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setAccelTau(self, accelTau):
        """
        This function sets the thermopile acceleration time constant in seconds [s].



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.



        Args:
            accelTau(c_double) : This parameter specifies the thermopile acceleration time constant in seconds [s].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setAccelTau(self.devSession, accelTau)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAccelTau(self, attribute, accelTau):
        """
        This function returns the thermopile acceleration time constant in seconds [s].



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            accelTau(c_double use with byref) : This parameter returns the thermopile acceleration time constant in seconds [s].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAccelTau(self.devSession, attribute, accelTau)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setInputAdapterType(self, type):
        """
        This function sets the sensor type to assume for custom sensors without calibration data memory connected to the instrument.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.



        Args:
            type(c_int16) : This parameter specifies the custom sensor type.



            Acceptable values:

             SENSOR_TYPE_PD_SINGLE (1): Photodiode sensor

             SENSOR_TYPE_THERMO    (2): Thermopile sensor

             SENSOR_TYPE_PYRO      (3): Pyroelectric sensor



            Value SENSOR_TYPE_PYRO is only available for energy meter instruments.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setInputAdapterType(self.devSession, type)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getInputAdapterType(self, type):
        """
        This function returns the assumed sensor type for custom sensors without calibration data memory connected to the instrument.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.



        Args:
            type(c_int16 use with byref) : This parameter returns the custom sensor type.



            Remark:

            The meanings of the obtained sensor type are:



            Sensor Types:

             SENSOR_TYPE_PD_SINGLE (1): Photodiode sensor

             SENSOR_TYPE_THERMO    (2): Thermopile sensor

             SENSOR_TYPE_PYRO      (3): Pyroelectric sensor

             SENSOR_TYPE_4Q        (4): 4 Quadrant sensor
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getInputAdapterType(self.devSession, type)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setAvgTime(self, avgTime):
        """
        This function sets the average time for measurement value generation.

        Args:
            avgTime(c_double) : This parameter specifies the average time in seconds.



            The value will be rounded to the closest multiple of the device's internal sampling rate.



            Remark:

            To get an measurement value from the device the timeout in your application has to be longer than the average time.




        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setAvgTime(self.devSession, avgTime)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAvgTime(self, attribute, avgTime):
        """
        This function returns the average time for measurement value generation.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            avgTime(c_double use with byref) : This parameter returns the specified average time in seconds.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAvgTime(self.devSession, attribute, avgTime)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setAvgCnt(self, averageCount):
        """
        This function sets the average count for measurement value generation.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.

        (2) The function is deprecated and kept for legacy reasons. Its recommended to use TLPM_setAvgTime() instead.



        Args:
            averageCount(c_int16) : This parameter specifies the average count.

            The default value is 1.



            Remark:

            Depending on the powermeter model internal there are taken up to 3000 measurements per second.

            In this example   Average Time = Average Count / 3000 [s].

            To get an measurement value from the device the timeout in your application has to be longer than the calculated average time.




        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setAvgCnt(self.devSession, averageCount)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAvgCnt(self, averageCount):
        """
        This function returns the average count for measurement value generation.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.

        (2) The function is deprecated and kept for legacy reasons. Its recommended to use TLPM_getAvgTime() instead.



        Args:
            averageCount(c_int16 use with byref) : This parameter returns the actual Average Count.



            Remark:

            Depending on the powermeter model internal there are taken up to 3000 measurements per second.

            In this example   Average Time = Average Count / 3000 [s].

            To get an measurement value from the device the timeout in your application has to be longer than the calculated average time.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAvgCnt(self.devSession, averageCount)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setAttenuation(self, attenuation):
        """
        This function sets the input attenuation.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.



        Args:
            attenuation(c_double) : This parameter specifies the input attenuation in dezibel [dB].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setAttenuation(self.devSession, attenuation)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAttenuation(self, attribute, attenuation):
        """
        This function returns the input attenuation.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            attenuation(c_double use with byref) : This parameter returns the specified input attenuation in dezibel [dB].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAttenuation(self.devSession, attribute, attenuation)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def startDarkAdjust(self):
        """
        This function starts the dark current/zero offset adjustment procedure.



        Remark:

        (1) You have to darken the input before starting dark/zero adjustment.

        (2) You can get the state of dark/zero adjustment with <Get Dark Adjustment State>

        (3) You can stop dark/zero adjustment with <Cancel Dark Adjustment>

        (4) You get the dark/zero value with <Get Dark Offset>

        (5) Energy sensors do not support this function
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_startDarkAdjust(self.devSession)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def cancelDarkAdjust(self):
        """
        This function cancels a running dark current/zero offset adjustment procedure.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_cancelDarkAdjust(self.devSession)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getDarkAdjustState(self, state):
        """
        This function returns the state of a dark current/zero offset adjustment procedure previously initiated by <Start Dark Adjust>.



        Args:
            state(c_int16 use with byref) : This parameter returns the dark adjustment state.



            Possible return values are:

            TLPM_STAT_DARK_ADJUST_FINISHED (0) : no dark adjustment running

            TLPM_STAT_DARK_ADJUST_RUNNING  (1) : dark adjustment is running
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getDarkAdjustState(self.devSession, state)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getDarkOffset(self, darkOffset):
        """
        This function returns the dark/zero offset.



        The function is not supported with energy sensors.

        Args:
            darkOffset(c_double use with byref) : This parameter returns the dark/zero offset.



            The unit of the returned offset value depends on the sensor type. Photodiodes return the dark offset in ampere [A]. Thermal sensors return the dark offset in volt [V].
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getDarkOffset(self.devSession, darkOffset)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setBeamDia(self, beamDiameter):
        """
        This function sets the users beam diameter in millimeter [mm].



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.

        (2) Beam diameter set value is used for calculating power and energy density.



        Args:
            beamDiameter(c_double) : This parameter specifies the users beam diameter in millimeter [mm].



            Remark:

            Beam diameter set value is used for calculating power and energy density.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setBeamDia(self.devSession, beamDiameter)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getBeamDia(self, attribute, beamDiameter):
        """
        This function returns the users beam diameter in millimeter [mm].



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM101, PM102, PM400.

        (2) Beam diameter set value is used for calculating power and energy density.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value


            beamDiameter(c_double use with byref) : This parameter returns the specified beam diameter in millimeter [mm].



            Remark:

            Beam diameter set value is used for calculating power and energy density.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getBeamDia(self.devSession, attribute, beamDiameter)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setWavelength(self, wavelength):
        """
        This function sets the users wavelength in nanometer [nm].



        Remark:

        Wavelength set value is used for calculating power.



        Args:
            wavelength(c_double) : This parameter specifies the users wavelength in nanometer [nm].



            Remark:

            Wavelength set value is used for calculating power.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setWavelength(self.devSession, wavelength)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getWavelength(self, attribute, wavelength):
        """
        This function returns the users wavelength in nanometer [nm].



        Remark:

        Wavelength set value is used for calculating power.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value


            wavelength(c_double use with byref) : This parameter returns the specified wavelength in nanometer [nm].



            Remark:

            Wavelength set value is used for calculating power.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getWavelength(self.devSession, attribute, wavelength)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPhotodiodeResponsivity(self, response):
        """
        This function sets the photodiode responsivity in ampere per watt [A/W].



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.



        Args:
            response(c_double) : This parameter specifies the photodiode responsivity in ampere per watt [A/W].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPhotodiodeResponsivity(self.devSession, response)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPhotodiodeResponsivity(self, attribute, responsivity):
        """
        This function returns the photodiode responsivity in ampere per watt [A/W].



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            responsivity(c_double use with byref) : This parameter returns the specified photodiode responsivity in ampere per watt [A/W].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPhotodiodeResponsivity(self.devSession, attribute, responsivity)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setThermopileResponsivity(self, response):
        """
        This function sets the thermopile responsivity in volt per watt [V/W]



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.



        Args:
            response(c_double) : This parameter specifies the thermopile responsivity in volt per watt [V/W]


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setThermopileResponsivity(self.devSession, response)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getThermopileResponsivity(self, attribute, responsivity):
        """
        This function returns the thermopile responsivity in volt per watt [V/W]



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM160T, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            responsivity(c_double use with byref) : This parameter returns the specified thermopile responsivity in volt per watt [V/W]


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getThermopileResponsivity(self.devSession, attribute, responsivity)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPyrosensorResponsivity(self, response):
        """
        This function sets the pyrosensor responsivity in volt per joule [V/J]



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.



        Args:
            response(c_double) : This parameter specifies the pyrosensor responsivity in volt per joule [V/J]


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPyrosensorResponsivity(self.devSession, response)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPyrosensorResponsivity(self, attribute, responsivity):
        """
        This function returns the pyrosensor responsivity in volt per joule [V/J]



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            responsivity(c_double use with byref) : This parameter returns the specified pyrosensor responsivity in volt per joule [V/J]


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPyrosensorResponsivity(self.devSession, attribute, responsivity)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setCurrentAutoRange(self, currentAutorangeMode):
        """
        This function sets the current auto range mode.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.



        Args:
            currentAutorangeMode(c_int16) : This parameter specifies the current auto range mode.



            Acceptable values:

              TLPM_AUTORANGE_CURRENT_OFF (0): current auto range disabled

              TLPM_AUTORANGE_CURRENT_ON  (1): current auto range enabled


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setCurrentAutoRange(self.devSession, currentAutorangeMode)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getCurrentAutorange(self, currentAutorangeMode):
        """
        This function returns the current auto range mode.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.



        Args:
            currentAutorangeMode(c_int16 use with byref) : This parameter returns the current auto range mode.



            Return values:

              TLPM_AUTORANGE_CURRENT_OFF (0): current auto range disabled

              TLPM_AUTORANGE_CURRENT_ON  (1): current auto range enabled


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getCurrentAutorange(self.devSession, currentAutorangeMode)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setCurrentRange(self, current_to_Measure):
        """
        This function sets the sensor's current range.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.



        Args:
            current_to_Measure(c_double) : This parameter specifies the current value to be measured in ampere [A].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setCurrentRange(self.devSession, current_to_Measure)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getCurrentRange(self, attribute, currentValue):
        """
        This function returns the actual current range value.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value


            currentValue(c_double use with byref) : This parameter returns the specified current range value in ampere [A].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getCurrentRange(self.devSession, attribute, currentValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setCurrentRef(self, currentReferenceValue):
        """
        This function sets the current reference value.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.



        Args:
            currentReferenceValue(c_double) : This parameter specifies the current reference value in amperes [A].



            Remark:

            This value is used for calculating differences between the actual current value and this current reference value if Current Reference State is ON.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setCurrentRef(self.devSession, currentReferenceValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getCurrentRef(self, attribute, currentReferenceValue):
        """
        This function returns the current reference value.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            currentReferenceValue(c_double use with byref) : This parameter returns the specified current reference value in amperes [A].



            Remark:

            This value is used for calculating differences between the actual current value and this current reference value if Current Reference State is ON.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getCurrentRef(self.devSession, attribute, currentReferenceValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setCurrentRefState(self, currentReferenceState):
        """
        This function sets the current reference state.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.



        Args:
            currentReferenceState(c_int16) : This parameter specifies the current reference state.



            Acceptable values:

              TLPM_CURRENT_REF_OFF (0): Current reference disabled. Absolute measurement.

              TLPM_CURRENT_REF_ON  (1): Current reference enabled. Relative measurement.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setCurrentRefState(self.devSession, currentReferenceState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getCurrentRefState(self, currentReferenceState):
        """
        This function returns the current reference state.



        Notes:

        (1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.



        Args:
            currentReferenceState(c_int16 use with byref) : This parameter returns the current reference state.



            Return values:

              TLPM_CURRENT_REF_OFF (0): Current reference disabled. Absolute measurement.

              TLPM_CURRENT_REF_ON  (1): Current reference enabled. Relative measurement.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getCurrentRefState(self.devSession, currentReferenceState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setEnergyRange(self, energyToMeasure):
        """
        This function sets the pyro sensor's energy range.



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.



        Args:
            energyToMeasure(c_double) : This parameter specifies the energy value in joule [J] to be measured.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setEnergyRange(self.devSession, energyToMeasure)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getEnergyRange(self, attribute, energyValue):
        """
        This function returns the pyro sensor's energy range.



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value


            energyValue(c_double use with byref) : This parameter returns the specified pyro sensor's energy value in joule [J].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getEnergyRange(self.devSession, attribute, energyValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setEnergyRef(self, energyReferenceValue):
        """
        This function sets the pyro sensor's energy reference value



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.

        (2) This value is used for calculating differences between the actual energy value and this energy reference value.



        Args:
            energyReferenceValue(c_double) : This parameter specifies the pyro sensor's energy reference value in joule [J].



            Remark:

            This value is used for calculating differences between the actual energy value and this energy reference value if Energy Reference State is ON.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setEnergyRef(self.devSession, energyReferenceValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getEnergyRef(self, attribute, energyReferenceValue):
        """
        This function returns the specified pyro sensor's energy reference value.



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.

        (2) The set value is used for calculating differences between the actual energy value and this energy reference value.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            energyReferenceValue(c_double use with byref) : This parameter returns the specified pyro sensor's energy reference value in joule [J].



            Remark:

            The set value is used for calculating differences between the actual energy value and this energy reference value if Energy Reference State is ON.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getEnergyRef(self.devSession, attribute, energyReferenceValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setEnergyRefState(self, energyReferenceState):
        """
        This function sets the instrument's energy reference state.



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.



        Args:
            energyReferenceState(c_int16) : This parameter specifies the energy reference state.



            Acceptable values:

              TLPM_ENERGY_REF_OFF (0): Energy reference disabled. Absolute measurement.

              TLPM_ENERGY_REF_ON  (1): Energy reference enabled. Relative measurement.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setEnergyRefState(self.devSession, energyReferenceState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getEnergyRefState(self, energyReferenceState):
        """
        This function returns the instrument's energy reference state.



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.



        Args:
            energyReferenceState(c_int16 use with byref) : This parameter returns the energy reference state.



            Return values:

              TLPM_ENERGY_REF_OFF (0): Energy reference disabled. Absolute measurement.

              TLPM_ENERGY_REF_ON  (1): Energy reference enabled. Relative measurement.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getEnergyRefState(self.devSession, energyReferenceState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getFreqRange(self, lowerFrequency, upperFrequency):
        """
        This function returns the instruments frequency measurement range.



        Remark:

        The frequency of the input signal is calculated over at least 0.3s. So it takes at least 0.3s to get a new frequency value from the instrument.



        Notes:

        (1) The function is only available on PM100D, PM100A, and PM100USB.



        Args:
            lowerFrequency(c_double use with byref) : This parameter returns the lower instruments frequency in [Hz].


            upperFrequency(c_double use with byref) : This parameter returns the upper instruments frequency in [Hz].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getFreqRange(self.devSession, lowerFrequency, upperFrequency)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPowerAutoRange(self, powerAutorangeMode):
        """
        This function sets the power auto range mode.



        Args:
            powerAutorangeMode(c_int16) : This parameter specifies the power auto range mode.



            Acceptable values:

              TLPM_AUTORANGE_POWER_OFF (0): power auto range disabled

              TLPM_AUTORANGE_POWER_ON  (1): power auto range enabled


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPowerAutoRange(self.devSession, powerAutorangeMode)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerAutorange(self, powerAutorangeMode):
        """
        This function returns the power auto range mode.



        Args:
            powerAutorangeMode(c_int16 use with byref) : This parameter returns the power auto range mode.



            Return values:

              TLPM_AUTORANGE_POWER_OFF (0): power auto range disabled

              TLPM_AUTORANGE_POWER_ON  (0): power auto range enabled


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerAutorange(self.devSession, powerAutorangeMode)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPowerRange(self, power_to_Measure):
        """
        This function sets the sensor's power range.



        Args:
            power_to_Measure(c_double) : This parameter specifies the most positive signal level expected for the sensor input in watt [W].
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPowerRange(self.devSession, power_to_Measure)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerRange(self, attribute, powerValue):
        """
        This function returns the actual power range value.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value


            powerValue(c_double use with byref) : This parameter returns the specified power range value in watt [W].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerRange(self.devSession, attribute, powerValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPowerRef(self, powerReferenceValue):
        """
        This function sets the power reference value.



        Args:
            powerReferenceValue(c_double) : This parameter specifies the power reference value.



            Remark:

            (1) The power reference value has the unit specified with <Set Power Unit>.

            (2) This value is used for calculating differences between the actual power value and this power reference value if Power Reference State is ON.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPowerRef(self.devSession, powerReferenceValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerRef(self, attribute, powerReferenceValue):
        """
        This function returns the power reference value.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            powerReferenceValue(c_double use with byref) : This parameter returns the specified power reference value.



            Remark:

            (1) The power reference value has the unit specified with <Set Power Unit>.

            (2) This value is used for calculating differences between the actual power value and this power reference value if Power Reference State is ON.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerRef(self.devSession, attribute, powerReferenceValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPowerRefState(self, powerReferenceState):
        """
        This function sets the power reference state.



        Args:
            powerReferenceState(c_int16) : This parameter specifies the power reference state.



            Acceptable values:

              TLPM_POWER_REF_OFF (0): Power reference disabled. Absolute measurement.

              TLPM_POWER_REF_ON  (1): Power reference enabled. Relative measurement.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPowerRefState(self.devSession, powerReferenceState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerRefState(self, powerReferenceState):
        """
        This function returns the power reference state.



        Args:
            powerReferenceState(c_int16 use with byref) : This parameter returns the power reference state.



            Return values:

              TLPM_POWER_REF_OFF (0): Power reference disabled. Absolute measurement.

              TLPM_POWER_REF_ON  (1): Power reference enabled. Relative measurement.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerRefState(self.devSession, powerReferenceState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPowerUnit(self, powerUnit):
        """
        This function sets the unit of the power value.



        Args:
            powerUnit(c_int16) : This parameter specifies the unit of the pover value.



            Acceptable values:

              TLPM_POWER_UNIT_WATT (0): power in Watt

              TLPM_POWER_UNIT_DBM  (1): power in dBm


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPowerUnit(self.devSession, powerUnit)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerUnit(self, powerUnit):
        """
        This function returns the unit of the power value.



        Args:
            powerUnit(c_int16 use with byref) : This parameter returns the unit of the power value.



            Return values:

              TLPM_POWER_UNIT_WATT (0): power in Watt

              TLPM_POWER_UNIT_DBM  (1): power in dBm
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerUnit(self.devSession, powerUnit)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerCalibrationPointsInformation(self, index, serialNumber, calibrationDate, calibrationPointsCount, author,
                                             sensorPosition):
        """
        Queries the customer adjustment header like serial nr, cal date, nr of points at given index



        Args:
            index(c_uint)
            serialNumber(create_string_buffer) : Serial Number of the sensor.

            Please provide a buffer of 256 characters.
            calibrationDate(create_string_buffer) : Last calibration date of this sensor

            Please provide a buffer of 256 characters.
            calibrationPointsCount(c_uint use with byref) : Number of calibration points of the power calibration with this sensor
            author(create_string_buffer)
            sensorPosition(c_uint use with byref) : The position of the sencor switch of a Thorlabs S130C

            1 = 5mW

            2 = 500mW
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerCalibrationPointsInformation(self.devSession, index, serialNumber,
                                                                           calibrationDate, calibrationPointsCount,
                                                                           author, sensorPosition)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerCalibrationPointsState(self, index, state):
        """
        Queries the state if the power calibration of this sensor is activated.



        Args:
            index(c_uint)
            state(c_int16 use with byref) : State if the user power calibration is activated and used for the power measurements.



            VI_ON: The user power calibration is used

            VI_OFF: The user power calibration is ignored in the power measurements
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerCalibrationPointsState(self.devSession, index, state)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPowerCalibrationPointsState(self, index, state):
        """
        This function activates/inactivates the power calibration of this sensor.



        Args:
            index(c_uint)
            state(c_int16) : State if the user power calibration is activated and used for the power measurements.



            VI_ON: The user power calibration is used

            VI_OFF: The user power calibration is ignored in the power measurements
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPowerCalibrationPointsState(self.devSession, index, state)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerCalibrationPoints(self, index, pointCounts, wavelengths, powers):
        """
        Returns a list of wavelength and the corresponding power correction factor.



        Args:
            index(c_uint)
            pointCounts(c_uint) : Number of points that are submitted in the wavelength and power correction factors arrays.

            Maximum of 10 wavelength - power correction factors pairs can be calibrated for each sensor.
            wavelengths( (c_double * arrayLength)()) : Array of wavelengths in nm. Requires ascending wavelength order.

            The array must contain <points counts> entries.
            powers( (c_double * arrayLength)()) : Array of power correction factorw that correspond to the wavelength array.

            The array must contain <points counts> entries, same as wavelenght to build wavelength - power correction factors pairs.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerCalibrationPoints(self.devSession, index, pointCounts, wavelengths,
                                                                powers)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPowerCalibrationPoints(self, index, pointCounts, wavelengths, powers, author, sensorPosition):
        """
        Sumbits a list of wavelength and the corresponding measured power correction factors to calibrate the power measurement.



        Args:
            index(c_uint)
            pointCounts(c_uint) : Number of points that are submitted in the wavelength and power correction factors arrays.

            Maximum of 10 wavelength - power correction factors  pairs can be calibrated for each sensor.
            wavelengths( (c_double * arrayLength)()) : Array of wavelengths in nm. Requires ascending wavelength order.

            The array must contain <points counts> entries.
            powers( (c_double * arrayLength)()) : Array of powers correction factors that correspond to the wavelength array.

            The array must contain <points counts> entries, same as wavelenght to build wavelength - power correction factors  pairs.
            author(create_string_buffer)
            sensorPosition(c_uint) : The position of the sencor switch of a Thorlabs S130C

            1 = 5mW

            2 = 500mW
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPowerCalibrationPoints(self.devSession, index, pointCounts, wavelengths,
                                                                powers, author, sensorPosition)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def reinitSensor(self):
        """
        To use the user power calibration, the sensor has to be reconnected.

        Either manually remove and reconnect the sensor to the instrument or use this funtion.



        This function will wait 2 seconds until the sensor has been reinitialized.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_reinitSensor(self.devSession)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setVoltageAutoRange(self, voltageAutorangeMode):
        """
        This function sets the voltage auto range mode.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            voltageAutorangeMode(c_int16) : This parameter specifies the voltage auto range mode.



            Acceptable values:

              TLPM_AUTORANGE_VOLTAGE_OFF (0): voltage auto range disabled

              TLPM_AUTORANGE_VOLTAGE_ON  (1): voltage auto range enabled


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setVoltageAutoRange(self.devSession, voltageAutorangeMode)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getVoltageAutorange(self, voltageAutorangeMode):
        """
        This function returns the voltage auto range mode.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            voltageAutorangeMode(c_int16 use with byref) : This parameter returns the voltage auto range mode.



            Return values:

              TLPM_AUTORANGE_VOLTAGE_OFF (0): voltage auto range disabled

              TLPM_AUTORANGE_VOLTAGE_ON  (1): voltage auto range enabled


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getVoltageAutorange(self.devSession, voltageAutorangeMode)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setVoltageRange(self, voltage_to_Measure):
        """
        This function sets the sensor's voltage range.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            voltage_to_Measure(c_double) : This parameter specifies the voltage value to be measured in volts [V].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setVoltageRange(self.devSession, voltage_to_Measure)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getVoltageRange(self, attribute, voltageValue):
        """
        This function returns the actual voltage range value.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value


            voltageValue(c_double use with byref) : This parameter returns the specified voltage range value in volts [V].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getVoltageRange(self.devSession, attribute, voltageValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getVoltageRanges(self, voltageValues, rangeCount):
        """
        This function returns the actual voltage range value.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            voltageValues( (c_double * arrayLength)()) : This parameter returns the specified voltage range value in volts [V].


            rangeCount(c_uint use with byref)
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getVoltageRanges(self.devSession, voltageValues, rangeCount)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setVoltageRef(self, voltageReferenceValue):
        """
        This function sets the voltage reference value.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            voltageReferenceValue(c_double) : This parameter specifies the voltage reference value in volts [V].



            Remark:

            This value is used for calculating differences between the actual voltage value and this voltage reference value if Voltage Reference State is ON.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setVoltageRef(self.devSession, voltageReferenceValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getVoltageRef(self, attribute, voltageReferenceValue):
        """
        This function returns the voltage reference value.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            voltageReferenceValue(c_double use with byref) : This parameter returns the specified voltage reference value in volts [V].



            Remark:

            This value is used for calculating differences between the actual voltage value and this voltage reference value if Voltage Reference State is ON.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getVoltageRef(self.devSession, attribute, voltageReferenceValue)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setVoltageRefState(self, voltageReferenceState):
        """
        This function sets the voltage reference state.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            voltageReferenceState(c_int16) : This parameter specifies the voltage reference state.



            Acceptable values:

              TLPM_VOLTAGE_REF_OFF (0): Voltage reference disabled. Absolute measurement.

              TLPM_VOLTAGE_REF_ON  (1): Voltage reference enabled. Relative measurement.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setVoltageRefState(self.devSession, voltageReferenceState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getVoltageRefState(self, voltageReferenceState):
        """
        This function returns the voltage reference state.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            voltageReferenceState(c_int16 use with byref) : This parameter returns the voltage reference state.



            Return values:

              TLPM_VOLTAGE_REF_OFF (0): Voltage reference disabled. Absolute measurement.

              TLPM_VOLTAGE_REF_ON  (1): Voltage reference enabled. Relative measurement.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getVoltageRefState(self.devSession, voltageReferenceState)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPeakThreshold(self, peakThreshold):
        """
        This function sets the peak detector threshold.



        Remark:

        Peak detector threshold is in percent [%] of the maximum from the actual measurements range.



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.



        Args:
            peakThreshold(c_double) : This parameter specifies the peak detector threshold.



            Remark:

            Peak detector threshold is in percent [%] of the maximum from the actual measurements range.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPeakThreshold(self.devSession, peakThreshold)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPeakThreshold(self, attribute, peakThreshold):
        """
        This function returns the peak detector threshold.



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.



        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            peakThreshold(c_double use with byref) : This parameter returns the peak detector threshold.



            Remark:

            Peak detector threshold is in percent [%] of the maximum from the actual measurements range.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPeakThreshold(self.devSession, attribute, peakThreshold)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setExtNtcParameter(self, r0Coefficient, betaCoefficient):
        """
        This function sets the temperature calculation coefficients for the NTC sensor externally connected to the instrument (NTC IN).



        Notes:

        (1) The function is only available on PM400.



        Args:
            r0Coefficient(c_double) : This parameter specifies the R0 coefficient in [Ohm] for calculating the temperature from the sensor's resistance by the beta parameter equation. R0 is the NTC's resistance at T0 (25 °C = 298.15 K).
            betaCoefficient(c_double) : This parameter specifies the B coefficient in [K] for calculating the temperature from the sensor's resistance by the beta parameter equation.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setExtNtcParameter(self.devSession, r0Coefficient, betaCoefficient)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getExtNtcParameter(self, attribute, r0Coefficient, betaCoefficient):
        """
        This function gets the temperature calculation coefficients for the NTC sensor externally connected to the instrument (NTC IN).



        Notes:

        (1) The function is only available on PM400.



        Args:
            attribute(c_int16) : This parameter specifies the values to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            r0Coefficient(c_double use with byref) : This parameter returns the specified R0 coefficient in [Ohm].
            betaCoefficient(c_double use with byref) : This parameter returns the specified B coefficient in [K].
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getExtNtcParameter(self.devSession, attribute, r0Coefficient, betaCoefficient)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setFilterPosition(self, filterPosition):
        """
        This function sets the current filter position



        Notes:

        (1) The function is only available on PM160 with firmware version 1.5.4 and higher



        Args:
            filterPosition(c_int16) : This parameter specifies the current filter position



            Acceptable values:

              VI_OFF (0): Filter position OFF. The filter value will not be used in the power calculation

              VI_ON  (1): Filter position ON, The filter value will be used in the power correction


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setFilterPosition(self.devSession, filterPosition)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getFilterPosition(self, filterPosition):
        """
        This function returns the current filter position



        Notes:

        (1) The function is only available on PM160 with firmware version 1.5.4 and higher



        Args:
            filterPosition(c_int16 use with byref) : This parameter returns the current filter position



            Acceptable values:

              VI_OFF (0): Filter position OFF. The filter value will not be used in the power calculation

              VI_ON  (1): Filter position ON, The filter value will be used in the power correction


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getFilterPosition(self.devSession, filterPosition)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setFilterAutoMode(self, filterAutoPositionDetection):
        """
        This function enables / disables the automatic filter position detection



        Notes:

        (1) The function is only available on PM160 with firmware version 1.5.4 and higher



        Args:
            filterAutoPositionDetection(c_int16) : This parameter specifies if the automatic filter position detection is enabled/disabled



            Acceptable values:

              VI_OFF (0): Filter position detection is OFF. The manual set fitler position is used

              VI_ON  (1): Filter position detection is ON, The filter position will be automatically detected


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setFilterAutoMode(self.devSession, filterAutoPositionDetection)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getFilterAutoMode(self, filterAutoPositionDetection):
        """
        This function returns if the automatic filter position detection is used



        Notes:

        (1) The function is only available on PM160 with firmware version 1.5.4 and higher



        Args:
            filterAutoPositionDetection(c_int16 use with byref) : This parameter returns if the automatic filter position detection is enabled/disabled



            Acceptable values:

              VI_OFF (0): Filter position detection is OFF. The manual set fitler position is used

              VI_ON  (1): Filter position detection is ON, The filter position will be automatically detected


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getFilterAutoMode(self.devSession, filterAutoPositionDetection)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAnalogOutputSlopeRange(self, minSlope, maxSlope):
        """
        This function returns range of the responsivity in volts per watt [V/W] for the analog output.



        Notes:

        (1) The function is only available on PM101 and PM102





        Args:
            minSlope(c_double use with byref) : This parameter returns the minimum voltage in Volt [V/W] of the analog output.

            Lower voltage is clipped to the minimum.


            maxSlope(c_double use with byref) : This parameter returns the maximum voltage in Volt [V/W] of the analog output.

            Higher voltage values are clipped to the maximum.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAnalogOutputSlopeRange(self.devSession, minSlope, maxSlope)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setAnalogOutputSlope(self, slope):
        """
        This function sets the responsivity in volts per watt [V/W] for the analog output.



        Notes:

        (1) The function is only available on PM101 and PM102



        Args:
            slope(c_double) : This parameter specifies the responsivity in volts per watt [V/W].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setAnalogOutputSlope(self.devSession, slope)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAnalogOutputSlope(self, attribute, slope):
        """
        This function returns the responsivity in volts per watt [V/W] for the analog output.



        Notes:

        (1) The function is only available on PM101





        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            slope(c_double use with byref) : This parameter returns the specified responsivity in volts per watt [V/W].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAnalogOutputSlope(self.devSession, attribute, slope)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAnalogOutputVoltageRange(self, minVoltage, maxVoltage):
        """
        This function returns the range in Volt [V] of the analog output.



        Notes:

        (1) The function is only available on PM101





        Args:
            minVoltage(c_double use with byref) : This parameter returns the minimum voltage in Volt [V] of the analog output.

            Lower voltage is clipped to the minimum.


            maxVoltage(c_double use with byref) : This parameter returns the maximum voltage in Volt [V] of the analog output.

            Higher voltage values are clipped to the maximum.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAnalogOutputVoltageRange(self.devSession, minVoltage, maxVoltage)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getAnalogOutputVoltage(self, attribute, voltage):
        """
        This function returns the analog output in Volt [V].



        Notes:

        (1) The function is only available on PM101





        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            voltage(c_double use with byref) : This parameter returns the analog output in Volt [V].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getAnalogOutputVoltage(self.devSession, attribute, voltage)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPositionAnalogOutputSlopeRange(self, minSlope, maxSlope):
        """
        This function returns range of the responsivity in volts per µm [V/µm] for the analog output.



        Notes:

        (1) The function is only available on PM102





        Args:
            minSlope(c_double use with byref) : This parameter returns the minimum slope in [V/µm] of the analog output.


            maxSlope(c_double use with byref) : This parameter returns the maximum slope in [V/µm] of the analog output.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPositionAnalogOutputSlopeRange(self.devSession, minSlope, maxSlope)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setPositionAnalogOutputSlope(self, slope):
        """
        This function sets the responsivity in volts per µm [V/µm] for the analog output.



        Notes:

        (1) The function is only available on PM102



        Args:
            slope(c_double) : This parameter specifies the responsivity in volts per µm [V/µm] for the AO2 and AO3 channel


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setPositionAnalogOutputSlope(self.devSession, slope)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPositionAnalogOutputSlope(self, attribute, slope):
        """
        This function returns the responsivity in volts per µm [V/µm] for the analog output channels.



        Notes:

        (1) The function is only available on PM102





        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            slope(c_double use with byref) : This parameter returns the specified responsivity in volts per µm [V/µm] for the AO2 and AO3 channel


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPositionAnalogOutputSlope(self.devSession, attribute, slope)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPositionAnalogOutputVoltageRange(self, minVoltage, maxVoltage):
        """
        This function returns the range in Volt [V] of the analog output.



        Notes:

        (1) The function is only available on PM102





        Args:
            minVoltage(c_double use with byref) : This parameter returns the minimum voltage in Volt [V] of the analog output.

            Lower voltage is clipped to the minimum.


            maxVoltage(c_double use with byref) : This parameter returns the maximum voltage in Volt [V] of the analog output.

            Higher voltage values are clipped to the maximum.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPositionAnalogOutputVoltageRange(self.devSession, minVoltage, maxVoltage)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPositionAnalogOutputVoltage(self, attribute, voltageX, voltageY):
        """
        This function returns the analog output in Volt [V].



        Notes:

        (1) The function is only available on PM102





        Args:
            attribute(c_int16) : This parameter specifies the value to be queried.



            Acceptable values:

              TLPM_ATTR_SET_VAL  (0): Set value

              TLPM_ATTR_MIN_VAL  (1): Minimum value

              TLPM_ATTR_MAX_VAL  (2): Maximum value

              TLPM_ATTR_DFLT_VAL (3): Default value


            voltageX(c_double use with byref) : This parameter returns the analog output in Volt [V] for the AO2 channel ( x direction)


            voltageY(c_double use with byref) : This parameter returns the analog output in Volt [V] for the AO3 channel ( y direction)


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPositionAnalogOutputVoltage(self.devSession, attribute, voltageX, voltageY)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measCurrent(self, current):
        """
        This function is used to obtain current readings from the instrument.



        Remark:

        This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160, PM200, PM400.



        Args:
            current(c_double use with byref) : This parameter returns the current in amperes [A].



            Remark:

            This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measCurrent(self.devSession, current)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measVoltage(self, voltage):
        """
        This function is used to obtain voltage readings from the instrument.



        Remark:

        This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.



        Args:
            voltage(c_double use with byref) : This parameter returns the voltage in volts [V].



            Remark:

            This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measVoltage(self.devSession, voltage)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measPower(self, power):
        """
        This function is used to obtain power readings from the instrument.



        Remark:

        This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.

        Args:
            power(c_double use with byref) : This parameter returns the power in the selected unit.



            Remark:

            (1) This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.

            (2) Select the unit with <Set Power Unit>.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measPower(self.devSession, power)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measEnergy(self, energy):
        """
        This function is used to obtain energy readings from the instrument.



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.



        Args:
            energy(c_double use with byref) : This parameter returns the actual measured energy value in joule [J].



            Remark:

            This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measEnergy(self.devSession, energy)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measFreq(self, frequency):
        """
        This function is used to obtain frequency readings from the instrument.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.



        Args:
            frequency(c_double use with byref) : This parameter returns the actual measured frequency of the input signal.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measFreq(self.devSession, frequency)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measPowerDens(self, powerDensity):
        """
        This function is used to obtain power density readings from the instrument.



        Notes:

        (1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.



        Args:
            powerDensity(c_double use with byref) : This parameter returns the actual measured power density in watt per square centimeter [W/cm²].



            Remark:

            This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measPowerDens(self.devSession, powerDensity)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measEnergyDens(self, energyDensity):
        """
        This function is used to obtain energy density readings from the instrument.



        Notes:

        (1) The function is only available on PM100D, PM100USB, PM200, PM400.



        Args:
            energyDensity(c_double use with byref) : This parameter returns the actual measured energy in joule per square centimeter [J/cm²].



            Remark:

            This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measEnergyDens(self.devSession, energyDensity)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measAuxAD0(self, voltage):
        """
        This function is used to obtain voltage readings from the instrument's auxiliary AD0 input.



        Notes:

        (1) The function is only available on PM200, PM400.



        Args:
            voltage(c_double use with byref) : This parameter returns the voltage in volt.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measAuxAD0(self.devSession, voltage)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measAuxAD1(self, voltage):
        """
        This function is used to obtain voltage readings from the instrument's auxiliary AD1 input.



        Notes:

        (1) The function is only available on PM200, PM400.



        Args:
            voltage(c_double use with byref) : This parameter returns the voltage in volt.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measAuxAD1(self.devSession, voltage)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measEmmHumidity(self, humidity):
        """
        This function is used to obtain relative humidity readings from the Environment Monitor Module (EMM) connected to the instrument.



        Notes:

        (1) The function is only available on PM200, PM400.

        (2) The function will return an error when no EMM is connected.

        Args:
            humidity(c_double use with byref) : This parameter returns the relative humidity in %.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measEmmHumidity(self.devSession, humidity)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measEmmTemperature(self, temperature):
        """
        This function is used to obtain temperature readings from the Environment Monitor Module (EMM) connected to the instrument.



        Notes:

        (1) The function is only available on PM200, PM400.

        (2) The function will return an error when no EMM is connected.

        Args:
            temperature(c_double use with byref) : This parameter returns the temperature in °C
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measEmmTemperature(self.devSession, temperature)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measExtNtcTemperature(self, temperature):
        """
        This function gets temperature readings from the external thermistor sensor connected to the instrument (NTC IN).



        Notes:

        (1) The function is only available on PM400.

        (2) The function will return an error when no external sensor is connected.



        Args:
            temperature(c_double use with byref) : This parameter returns the temperature in °C
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measExtNtcTemperature(self.devSession, temperature)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def measExtNtcResistance(self, resistance):
        """
        This function gets resistance readings from the external thermistor sensor connected to the instrument (NTC IN).



        Notes:

        (1) The function is only available on PM400.

        (2) The function will return an error when no external sensor is connected.



        Args:
            resistance(c_double use with byref) : This parameter returns the resistance in Ohm
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_measExtNtcResistance(self.devSession, resistance)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def meas4QPositions(self, xPosition, yPosition):
        """
        This function returns the x and position of a 4q sensor



        Notes:

        (1) The function is only available on PM101, PM102, PM400.



        Args:
            xPosition(c_double use with byref) : This parameter returns the actual measured x position in µm
            yPosition(c_double use with byref) : This parameter returns the actual measured y position in µm
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_meas4QPositions(self.devSession, xPosition, yPosition)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def meas4QVoltages(self, voltage1, voltage2, voltage3, voltage4):
        """
        This function returns the voltage of each sector of a 4q sensor



        Notes:

        (1) The function is only available on PM101, PM102, PM400.



        Args:
            voltage1(c_double use with byref) : This parameter returns the actual measured voltage of the upper left sector of a 4q sensor.
            voltage2(c_double use with byref)
            voltage3(c_double use with byref)
            voltage4(c_double use with byref)
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_meas4QVoltages(self.devSession, voltage1, voltage2, voltage3, voltage4)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setArrMeasurement(self, enableArrayMeasurement):
        """
        This function enables the array measurement.

        The functions measArrPower can be used.



        Args:
            enableArrayMeasurement(c_uint)
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setArrMeasurement(self.devSession, enableArrayMeasurement)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getArrMeasurement(self, enableArrayMeasurement):
        """
        This function returns of the array measurement is active.

        The functions measArrPower can be used.



        Args:
            enableArrayMeasurement(c_uint use with byref) : Array Measurement activated:



            VI_ON: array measurement is active. The funtion "getPowerArrayMeasurement" returns more than one value

            VI_OFF: array measurement is disabled. The funtion "getPowerArrayMeasurement" only returns one value
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getArrMeasurement(self.devSession, enableArrayMeasurement)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerArrayMeasurement(self, count, timestamps, powerValues):
        """
        This function is used to obtain power readings from the instrument.

        The result are timestamp - power value pairs.





        Remark:

        This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.

        Args:
            count(c_uint use with byref) : The count of timestamp - measurement value pairs
            timestamps( (c_uint * arrayLength)())
            powerValues( (c_double * arrayLength)())
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerArrayMeasurement(self.devSession, count, timestamps, powerValues)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerMeasurementSequence(self, count, interval, powerValues):
        """
        This function filles the given array with measurements from the device.



        Duration of measurement in µsec = Count * Interval

        The maximum capture time is 1 sec regardless of the used inteval



        Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging ( setPowerAutoRange to OFF)



        Args:
            count(c_int) : Count of measurements in the array.
            interval(c_int) : interval between two measurements in the array in µsec.

            The maximum resolution is 100µsec without averaging
            powerValues( (c_double * arrayLength)()) : Array of power measurements with the given count and interval
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerMeasurementSequence(self.devSession, count, interval, powerValues)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getCurrentMeasurementSequence(self, count, interval, currentValues):
        """
        This function filles the given array with measurements from the device.



        Duration of measurement in µsec = Count * Interval

        The maximum capture time is 1 sec regardless of the used inteval



        Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging ( setPowerAutoRange to OFF)



        Args:
            count(c_int) : Count of measurements in the array.
            interval(c_int) : interval between two measurements in the array in µsec.

            The maximum resolution is 100µsec without averaging
            currentValues( (c_double * arrayLength)()) : Array of power measurements with the given count and interval
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getCurrentMeasurementSequence(self.devSession, count, interval, currentValues)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getPowerDensityMeasurementSequence(self, count, interval, powerDensityValues):
        """
        This function filles the given array with measurements from the device.



        Duration of measurement in µsec = Count * Interval

        The maximum capture time is 1 sec regardless of the used inteval



        Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging ( setPowerAutoRange to OFF)

        Args:
            count(c_int) : Count of measurements in the array.
            interval(c_int) : interval between two measurements in the array in µsec.

            The maximum resolution is 100µsec without averaging
            powerDensityValues( (c_double * arrayLength)()) : Array of power measurements with the given count and interval
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getPowerDensityMeasurementSequence(self.devSession, count, interval,
                                                                         powerDensityValues)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setDigIoDirection(self, IO0, IO1, IO2, IO3):
        """
        This function sets the digital I/O port direction.



        Note: The function is only available on PM200 and PM400.

        Args:
            IO0(c_int16) : This parameter specifies the I/O port #0 direction.



            Input:  VI_OFF (0)

            Output: VI_ON  (1)


            IO1(c_int16) : This parameter specifies the I/O port #1 direction.



            Input:  VI_OFF (0)

            Output: VI_ON  (1)


            IO2(c_int16) : This parameter specifies the I/O port #2 direction.



            Input:  VI_OFF (0)

            Output: VI_ON  (1)


            IO3(c_int16) : This parameter specifies the I/O port #3 direction.



            Input:  VI_OFF (0)

            Output: VI_ON  (1)


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setDigIoDirection(self.devSession, IO0, IO1, IO2, IO3)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getDigIoDirection(self, IO0, IO1, IO2, IO3):
        """
        This function returns the digital I/O port direction.



        Note: The function is only available on PM200 and PM400.

        Args:
            IO0(c_int16 use with byref) : This parameter returns the I/O port #0 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.



            Note: You may pass VI_NULL if you don't need this value.


            IO1(c_int16 use with byref) : This parameter returns the I/O port #1 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.



            Note: You may pass VI_NULL if you don't need this value.


            IO2(c_int16 use with byref) : This parameter returns the I/O port #2 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.



            Note: You may pass VI_NULL if you don't need this value.


            IO3(c_int16 use with byref) : This parameter returns the I/O port #3 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.



            Note: You may pass VI_NULL if you don't need this value.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getDigIoDirection(self.devSession, IO0, IO1, IO2, IO3)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setDigIoOutput(self, IO0, IO1, IO2, IO3):
        """
        This function sets the digital I/O outputs.



        Notes:

        (1) Only ports configured as outputs are affected by this function. Use <Set Digital I/O Direction> to configure ports as outputs.

        (2) The function is only available on PM200 and PM400.

        Args:
            IO0(c_int16) : This parameter specifies the I/O port #0 output.



            Low level:  VI_OFF (0)

            High level: VI_ON  (1)


            IO1(c_int16) : This parameter specifies the I/O port #1 output.



            Low level:  VI_OFF (0)

            High level: VI_ON  (1)


            IO2(c_int16) : This parameter specifies the I/O port #2 output.



            Low level:  VI_OFF (0)

            High level: VI_ON  (1)


            IO3(c_int16) : This parameter specifies the I/O port #3 output.



            Low level:  VI_OFF (0)

            High level: VI_ON  (1)


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setDigIoOutput(self.devSession, IO0, IO1, IO2, IO3)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getDigIoOutput(self, IO0, IO1, IO2, IO3):
        """
        This function returns the digital I/O output settings.



        Note: The function is only available on PM200 and PM400.

        Args:
            IO0(c_int16 use with byref) : This parameter returns the I/O port #0 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.



            Note: You may pass VI_NULL if you don't need this value.


            IO1(c_int16 use with byref) : This parameter returns the I/O port #1 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.



            Note: You may pass VI_NULL if you don't need this value.


            IO2(c_int16 use with byref) : This parameter returns the I/O port #2 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.



            Note: You may pass VI_NULL if you don't need this value.


            IO3(c_int16 use with byref) : This parameter returns the I/O port #3 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.



            Note: You may pass VI_NULL if you don't need this value.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getDigIoOutput(self.devSession, IO0, IO1, IO2, IO3)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getDigIoPort(self, IO0, IO1, IO2, IO3):
        """
        This function returns the actual digital I/O port level.



        Note: The function is only available on PM200 and PM400.

        Args:
            IO0(c_int16 use with byref) : This parameter returns the I/O port #0 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.



            Note: You may pass VI_NULL if you don't need this value.


            IO1(c_int16 use with byref) : This parameter returns the I/O port #1 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.



            Note: You may pass VI_NULL if you don't need this value.


            IO2(c_int16 use with byref) : This parameter returns the I/O port #2 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.



            Note: You may pass VI_NULL if you don't need this value.


            IO3(c_int16 use with byref) : This parameter returns the I/O port #3 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.



            Note: You may pass VI_NULL if you don't need this value.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getDigIoPort(self.devSession, IO0, IO1, IO2, IO3)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def errorMessage(self, statusCode, description):
        """
        This function takes the error code returned by the instrument driver functions interprets it and returns it as an user readable string.



        Status/error codes and description:



        --- Instrument Driver Errors and Warnings ---

        Status      Description

        -------------------------------------------------

                 0  No error (the call was successful).

        0x3FFF0085  Unknown Status Code     - VI_WARN_UNKNOWN_STATUS

        0x3FFC0901  WARNING: Value overflow - VI_INSTR_WARN_OVERFLOW

        0x3FFC0902  WARNING: Value underrun - VI_INSTR_WARN_UNDERRUN

        0x3FFC0903  WARNING: Value is NaN   - VI_INSTR_WARN_NAN

        0xBFFC0001  Parameter 1 out of range.

        0xBFFC0002  Parameter 2 out of range.

        0xBFFC0003  Parameter 3 out of range.

        0xBFFC0004  Parameter 4 out of range.

        0xBFFC0005  Parameter 5 out of range.

        0xBFFC0006  Parameter 6 out of range.

        0xBFFC0007  Parameter 7 out of range.

        0xBFFC0008  Parameter 8 out of range.

        0xBFFC0012  Error Interpreting instrument response.



        --- Instrument Errors ---

        Range: 0xBFFC0700 .. 0xBFFC0CFF.

        Calculation: Device error code + 0xBFFC0900.

        Please see your device documentation for details.



        --- VISA Errors ---

        Please see your VISA documentation for details.



        Args:
            statusCode(ViStatus) : This parameter accepts the error codes returned from the instrument driver functions.



            Default Value: 0 - VI_SUCCESS
            description(create_string_buffer) : This parameter returns the interpreted code as an user readable message string.



            Notes:

            (1) The array must contain at least 512 elements ViChar[512].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_errorMessage(self.devSession, statusCode, description)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def errorQuery(self, errorNumber, errorMessage):
        """
        This function queries the instrument's error queue manually.

        Use this function to query the instrument's error queue if the driver's error query mode is set to manual query.



        Notes:

        (1) The returned values are stored in the drivers error store. You may use <Error Message> to get a descriptive text at a later point of time.

        Args:
            errorNumber(c_int use with byref) : This parameter returns the instrument error number.



            Notes:

            (1) You may pass VI_NULL if you don't need this value.


            errorMessage(create_string_buffer) : This parameter returns the instrument error message.



            Notes:

            (1) The array must contain at least TLPM_ERR_DESCR_BUFFER_SIZE (512) elements ViChar[512].

            (2) You may pass VI_NULL if you do not need this value.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_errorQuery(self.devSession, errorNumber, errorMessage)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def errorQueryMode(self, mode):
        """
        This function selects the driver's error query mode.

        Args:
            mode(c_int16) : This parameter specifies the driver's error query mode.



            If set to Automatic each driver function queries the instrument's error queue and in case an error occured returns the error number.



            If set to Manual the driver does not query the instrument for errors and therefore a driver function does not return instrument errors. You should use <Error Query> to manually query the instrument's error queue.



            VI_OFF (0): Manual error query.

            VI_ON  (1): Automatic error query (default).


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_errorQueryMode(self.devSession, mode)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def reset(self):
        """
        This function resets the device.
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_reset(self.devSession)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def selfTest(self, selfTestResult, description):
        """
        This function runs the device self test routine and returns the test result.

        Args:
            selfTestResult(c_int16 use with byref) : This parameter contains the value returned from the device self test routine. A retured zero value indicates a successful run, a value other than zero indicates failure.
            description(create_string_buffer) : This parameter returns the interpreted code as an user readable message string.



            Notes:

            (1) The array must contain at least 256 elements ViChar[256].


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_selfTest(self.devSession, selfTestResult, description)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def revisionQuery(self, instrumentDriverRevision, firmwareRevision):
        """
        This function returns the revision numbers of the instrument driver and the device firmware.

        Args:
            instrumentDriverRevision(create_string_buffer) : This parameter returns the Instrument Driver revision.



            Notes:

            (1) The array must contain at least 256 elements ViChar[256].

            (2) You may pass VI_NULL if you do not need this value.


            firmwareRevision(create_string_buffer) : This parameter returns the device firmware revision.



            Notes:

            (1) The array must contain at least 256 elements ViChar[256].

            (2) You may pass VI_NULL if you do not need this value.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_revisionQuery(self.devSession, instrumentDriverRevision, firmwareRevision)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def identificationQuery(self, manufacturerName, deviceName, serialNumber, firmwareRevision):
        """
        This function returns the device identification information.

        Args:
            manufacturerName(create_string_buffer) : This parameter returns the manufacturer name.



            Notes:

            (1) The array must contain at least 256 elements ViChar[256].

            (2) You may pass VI_NULL if you do not need this value.


            deviceName(create_string_buffer) : This parameter returns the device name.



            Notes:

            (1) The array must contain at least 256 elements ViChar[256].

            (2) You may pass VI_NULL if you do not need this value.


            serialNumber(create_string_buffer) : This parameter returns the device serial number.



            Notes:

            (1) The array must contain at least 256 elements ViChar[256].

            (2) You may pass VI_NULL if you do not need this value.


            firmwareRevision(create_string_buffer) : This parameter returns the device firmware revision.



            Notes:

            (1) The array must contain at least 256 elements ViChar[256].

            (2) You may pass VI_NULL if you do not need this value.


        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_identificationQuery(self.devSession, manufacturerName, deviceName, serialNumber,
                                                          firmwareRevision)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getCalibrationMsg(self, message):
        """
        This function returns a human readable calibration message.

        

        Args:
            message(create_string_buffer) : This parameter returns the calibration message.

            

            Notes:

            (1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getCalibrationMsg(self.devSession, message)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getSensorInfo(self, name, snr, message, pType, pStype, pFlags):
        """
        This function is used to obtain informations from the connected sensor like sensor name, serial number, calibration message, sensor type, sensor subtype and sensor flags.  

        

        Remark:

        The meanings of the obtained sensor type, subtype and flags are:

        

        Sensor Types:

         SENSOR_TYPE_NONE               0x00 // No sensor

         SENSOR_TYPE_PD_SINGLE          0x01 // Photodiode sensor

         SENSOR_TYPE_THERMO             0x02 // Thermopile sensor

         SENSOR_TYPE_PYRO               0x03 // Pyroelectric sensor

        

        Sensor Subtypes:

         SENSOR_SUBTYPE_NONE            0x00 // No sensor

         

        Sensor Subtypes Photodiode:

         SENSOR_SUBTYPE_PD_ADAPTER      0x01 // Photodiode adapter

         SENSOR_SUBTYPE_PD_SINGLE_STD   0x02 // Photodiode sensor

         SENSOR_SUBTYPE_PD_SINGLE_FSR   0x03 // Photodiode sensor with 

                                                integrated filter

                                                identified by position 

         SENSOR_SUBTYPE_PD_SINGLE_STD_T 0x12 // Photodiode sensor with

                                                temperature sensor

        Sensor Subtypes Thermopile:

         SENSOR_SUBTYPE_THERMO_ADAPTER  0x01 // Thermopile adapter

         SENSOR_SUBTYPE_THERMO_STD      0x02 // Thermopile sensor

         SENSOR_SUBTYPE_THERMO_STD_T    0x12 // Thermopile sensor with 

                                                temperature sensor

        Sensor Subtypes Pyroelectric Sensor:

         SENSOR_SUBTYPE_PYRO_ADAPTER    0x01 // Pyroelectric adapter

         SENSOR_SUBTYPE_PYRO_STD        0x02 // Pyroelectric sensor

         SENSOR_SUBTYPE_PYRO_STD_T      0x12 // Pyroelectric sensor with

                                                temperature sensor

        Sensor Flags:

         TLPM_SENS_FLAG_IS_POWER     0x0001 // Power sensor

         TLPM_SENS_FLAG_IS_ENERGY    0x0002 // Energy sensor

         TLPM_SENS_FLAG_IS_RESP_SET  0x0010 // Responsivity settable

         TLPM_SENS_FLAG_IS_WAVEL_SET 0x0020 // Wavelength settable

         TLPM_SENS_FLAG_IS_TAU_SET   0x0040 // Time constant settable

         TLPM_SENS_FLAG_HAS_TEMP     0x0100 // With Temperature sensor 

        Args:
            name(create_string_buffer) : This parameter returns the name of the connected sensor.

            
            snr(create_string_buffer) : This parameter returns the serial number of the connected sensor.
            message(create_string_buffer) : This parameter returns the calibration message of the connected sensor.

            
            pType(c_int16 use with byref) : This parameter returns the sensor type of the connected sensor.

            

            Remark:

            The meanings of the obtained sensor type are:

            

            Sensor Types:

             SENSOR_TYPE_NONE               0x00 // No sensor

             SENSOR_TYPE_PD_SINGLE          0x01 // Photodiode sensor

             SENSOR_TYPE_THERMO             0x02 // Thermopile sensor

             SENSOR_TYPE_PYRO               0x03 // Pyroelectric sensor
            pStype(c_int16 use with byref) : This parameter returns the subtype of the connected sensor.

            

            Remark:

            The meanings of the obtained sensor subtype are:

            

            Sensor Subtypes:

             SENSOR_SUBTYPE_NONE            0x00 // No sensor

             

            Sensor Subtypes Photodiode:

             SENSOR_SUBTYPE_PD_ADAPTER      0x01 // Photodiode adapter

             SENSOR_SUBTYPE_PD_SINGLE_STD   0x02 // Photodiode sensor

             SENSOR_SUBTYPE_PD_SINGLE_FSR   0x03 // Photodiode sensor with 

                                                    integrated filter

                                                    identified by position 

             SENSOR_SUBTYPE_PD_SINGLE_STD_T 0x12 // Photodiode sensor with

                                                    temperature sensor

            Sensor Subtypes Thermopile:

             SENSOR_SUBTYPE_THERMO_ADAPTER  0x01 // Thermopile adapter

             SENSOR_SUBTYPE_THERMO_STD      0x02 // Thermopile sensor

             SENSOR_SUBTYPE_THERMO_STD_T    0x12 // Thermopile sensor with 

                                                    temperature sensor

            Sensor Subtypes Pyroelectric Sensor:

             SENSOR_SUBTYPE_PYRO_ADAPTER    0x01 // Pyroelectric adapter

             SENSOR_SUBTYPE_PYRO_STD        0x02 // Pyroelectric sensor

             SENSOR_SUBTYPE_PYRO_STD_T      0x12 // Pyroelectric sensor with

                                                    temperature sensor
            pFlags(c_int16 use with byref) : This parameter returns the flags of the connected sensor.

            

            Remark:

            The meanings of the obtained sensor flags are:

            

            Sensor Flags:

             TLPM_SENS_FLAG_IS_POWER     0x0001 // Power sensor

             TLPM_SENS_FLAG_IS_ENERGY    0x0002 // Energy sensor

             TLPM_SENS_FLAG_IS_RESP_SET  0x0010 // Responsivity settable

             TLPM_SENS_FLAG_IS_WAVEL_SET 0x0020 // Wavelength settable

             TLPM_SENS_FLAG_IS_TAU_SET   0x0040 // Time constant settable

             TLPM_SENS_FLAG_HAS_TEMP     0x0100 // With Temperature sensor
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getSensorInfo(self.devSession, name, snr, message, pType, pStype, pFlags)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def writeRaw(self, command):
        """
        This function writes directly to the instrument.

        Args:
            command(ViString) : Null terminated command string to send to the instrument.

            
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_writeRaw(self.devSession, command)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def readRaw(self, buffer, size, returnCount):
        """
        This function reads directly from the instrument.

        

        Args:
            buffer(create_string_buffer) : Byte buffer that receives the data read from the instrument.

            

            Notes:

            (1) If received data is less than buffer size, the buffer is additionaly terminated with a '\0' character.

            (2) If received data is same as buffer size no '\0' character is appended. Its the caller's responsibility to make sure a buffer is '\0' terminated if the caller wants to interprete the buffer as string.
            size(c_int) : This parameter specifies the buffer size.

            
            returnCount(c_int use with byref) : Number of bytes actually transferred and filled into Buffer. This number doesn't count the additional termination '\0' character. If Return Count == size the buffer content will not be '\0' terminated.

            

            Notes:

            (1) You may pass VI_NULL if you don't need this value.

            
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_readRaw(self.devSession, buffer, size, returnCount)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setTimeoutValue(self, value):
        """
        This function sets the interface communication timeout value.

        Args:
            value(c_int) : This parameter specifies the communication timeout value in ms.

            
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setTimeoutValue(self.devSession, value)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getTimeoutValue(self, value):
        """
        This function gets the interface communication timeout value.

        

        Args:
            value(c_int use with byref) : This parameter returns the communication timeout value in ms.

            
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getTimeoutValue(self.devSession, value)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setDeviceBaudrate(self, baudrate):
        """
        Tell the instrument which baudrate has to be used for the serial communication.

        This value is stored inside the instrument. 

        

        If the RS232 interface is currently used for the communication, call the function setDriverBaudrate to adapt to the new baudrate.

        Args:
            baudrate(c_int) : This parameter specifies the baudrate in bits/sec.

            
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setDeviceBaudrate(self.devSession, baudrate)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getDeviceBaudrate(self, baudrate):
        """
        This function returns the baudrate that is used for the serial communication inside the instrument

        

        Args:
            baudrate(c_int use with byref) : This parameter returns the baudrate in bist/sec.

            
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getDeviceBaudrate(self.devSession, baudrate)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def setDriverBaudrate(self, baudrate):
        """
        This function sets the baudrate for the serial interface on the PC side

        Args:
            baudrate(c_int) : This parameter specifies the baudrate in bits/sec.

            

     Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_setDriverBaudrate(self.devSession, baudrate)
        self.__testForError(pInvokeResult)
        return pInvokeResult

    def getDriverBaudrate(self, baudrate):
        """
        This function returns the baudrate that is used for the serial communication on the PC side

        

        Args:
            baudrate(c_int use with byref) : This parameter returns the baudrate in bist/sec.

            
        Returns:
            int: The return value, 0 is for success
        """
        pInvokeResult = self.dll.TLPM_getDriverBaudrate(self.devSession, baudrate)
        self.__testForError(pInvokeResult)
        return pInvokeResult

