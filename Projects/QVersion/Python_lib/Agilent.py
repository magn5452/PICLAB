import pyvisa as visa
import time
import numpy as np
from tqdm import tqdm
import sys  # allows stopping the entire runtime


class Agilent:  # developer: Lars Nielsen, Mads Larsen, Andreas Hänsel, Magnus Madsen

    def __init__(self, resource_manager, channel=18, slot=[3, 4], channelInSlot=1, GPIB_interface=0, SourceSlot=2):
        self.channel = channel
        # resourceName = 'GPIB'+str(int(GPIB_interface))+'::'+str(channel)+'::INSTR'
        resourceName = 'GPIB0' + '::' + str(int(GPIB_interface)) + '::INSTR'

        # resourceName = "GPIB0::18::INSTR"
        self.agilent = resource_manager.open_resource(resourceName)
        is_alive = self.agilent.query('*IDN?')
        self.agilent.read_termination = '\n'
        self.agilent.write_termination = '\n'
        self.agilent.timeout = 60000
        self.is_alive()
        self.slot = slot
        self.channelInSlot = channelInSlot
        self.SourceSlot = SourceSlot

        self.lambdaArr = []

    def is_alive(self):
        is_alive = self.agilent.write('*IDN?')
        if is_alive != 0:
            print("Agilent is alive")

    def set_wavelength(self, wavelength_nm):  # nm
        self.agilent.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV ' + str(wavelength_nm) + 'NM')

    def set_power(self, power_mW):  # mW
        self.agilent.write('SOUR' + str(int(self.SourceSlot)) + ':POW ' + str(power_mW) + 'MW')  # Set Laser Power  [mW]

    def get_wavelength(self):  # nm
        wavelength_nm = self.agilent.write(':SOUR' + str(int(self.SourceSlot)) + ':WAV ' + 'NM?')
        print(wavelength_nm)
        return wavelength_nm

    def get_power(self):
        if isinstance(self.slot, list):
            slotTemp = self.slot[0]
        else:
            slotTemp = self.slot

        self.agilent.write('trig3:inp ign')  # Set power meter 3 to act on trigger

        self.agilent.write('init' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':imm')
        powerOut = self.agilent.query_ascii_values('fetc' + str(slotTemp) + ':chan' + str(self.channelInSlot) + ':pow?')
        return float(powerOut[0])

    def get_name(self):
        return "Agilent laser"

    def close(self):
        self.agilent.close()

    def get_min_wavelength(self):
        return 1520

    def get_max_wavelength(self):
        return 1630

    def laser_on(self):
        self.agilent.write('SOUR' + str(int(self.SourceSlot)) + ':POWer:STATe 1')

    def laser_off(self):
        self.agilent.write('SOUR' + str(int(self.SourceSlot)) + ':POWer:STATe 0')

    def is_laser_on(self):
        LaserState = self.agilent.query('SOUR' + str(int(self.SourceSlot)) + ':POWer:STATe?')
        LaserState = int(LaserState)
        if LaserState == 1:
            print('Agilent Laser: ON')
            return 1
        elif LaserState == 0:
            print('Agilent Laser: OFF')
            return 0
        else:
            print('Agilent Laser state unknown')

    def toggle_laser(self):
        if self.is_laser_on():
            self.laser_off()
        else:
            self.laser_on()