# -*- coding: utf-8 -*-.
"""
Created on Wed May 12 10:29:17 2021
@author: Peter Tønning
"""

import pyvisa as visa
import time


class ANDO_OSA:
    def __init__(self, channel=30, GPIB_interface=1):
        self.channel = channel
        rm = visa.ResourceManager()
        resourceName = 'GPIB' + str(int(GPIB_interface)) + '::' + str(channel) + '::INSTR'
        # print(rm.list_resources())
        self.instr = rm.open_resource(resourceName);
        self.instr.write('ATREF0');
        #self.instr.write('SMPL1001')
        #self.instr.write('SNAT')

        # alive = self.instr.query('*IDN?')
        # self.instr.read_termination = '\n'
        # self.instr.write_termination = '\n'
        # self.instr.timeout = 10000
        # if alive != 0:
        #    print('Ando AQ4321A is alive')
        #    # print(alive)

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

    def SetupOSA(self, CenterWL=950, Span=10, Level=0, Resolution=0.05, Sensitivity=0, Preview=0):
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
        self.instr.write('SD0')
        Status = 1
        StatusOut = []


        while Status == 1:
            Mode = self.instr.query('SWEEP?')[0:-2]  # Something is broken here... Check up on the output of mode
            Status = float(Mode)
            time.sleep(0.2)
            StatusOut.append(Status)

        Power = self.instr.query('LDATAR0001-R1001')

        # Power=Power.replace("−", "-")
        print(Power)
        PowerF = [float(value) for value in Power.split(',')]

        WL = self.instr.query('WDATAR0001-R1001')

        WLF = [float(value) for value in WL.split(', ')]
        return [PowerF[1:], WLF[1:]]
