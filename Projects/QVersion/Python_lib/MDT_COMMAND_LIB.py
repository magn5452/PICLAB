from ctypes import *

# region import dll functions

mdtLib = cdll.LoadLibrary("C:/Users/shd-PhotonicLab/Documents/Python Scripts/Qversion_exp/Python_lib/MDT_COMMAND_LIB_x64.dll")
cmdOpen = mdtLib.Open
cmdOpen.restype = c_int
cmdOpen.argtypes = [c_char_p, c_int, c_int]

cmdIsOpen = mdtLib.IsOpen
cmdOpen.restype = c_int
cmdOpen.argtypes = [c_char_p]

cmdList = mdtLib.List
cmdList.argtypes = [c_char_p, c_int]
cmdList.restype = c_int

cmdGetId = mdtLib.GetId
cmdGetId.restype = c_int
cmdGetId.argtypes = [c_int, c_char_p]

cmdGetLimtVoltage = mdtLib.GetLimitVoltage
cmdGetLimtVoltage.restype = c_int
cmdGetLimtVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetAllVoltage = mdtLib.SetAllVoltage
cmdSetAllVoltage.restype = c_int
cmdSetAllVoltage.argtypes = [c_int, c_double]

cmdGetMasterScanEnable = mdtLib.GetMasterScanEnable
cmdGetMasterScanEnable.restype = c_int
cmdGetMasterScanEnable.argtypes = [c_int, POINTER(c_int)]

cmdSetMasterScanEnable = mdtLib.SetMasterScanEnable
cmdSetMasterScanEnable.restype = c_int
cmdSetMasterScanEnable.argtypes = [c_int, c_int]

cmdGetMasterScanVoltage = mdtLib.GetMasterScanVoltage
cmdGetMasterScanVoltage.restype = c_int
cmdGetMasterScanVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetMasterScanVoltage = mdtLib.SetMasterScanVoltage
cmdSetMasterScanVoltage.restype = c_int
cmdSetMasterScanVoltage.argtypes = [c_int, c_double]

cmdGetXAxisVoltage = mdtLib.GetXAxisVoltage
cmdGetXAxisVoltage.restype = c_int
cmdGetXAxisVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetXAxisVoltage = mdtLib.SetXAxisVoltage
cmdSetXAxisVoltage.restype = c_int
cmdSetXAxisVoltage.argtypes = [c_int, c_double]

cmdGetYAxisVoltage = mdtLib.GetYAxisVoltage
cmdGetYAxisVoltage.restype = c_int
cmdGetYAxisVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetYAxisVoltage = mdtLib.SetYAxisVoltage
cmdSetYAxisVoltage.restype = c_int
cmdSetYAxisVoltage.argtypes = [c_int, c_double]

cmdGetZAxisVoltage = mdtLib.GetZAxisVoltage
cmdGetZAxisVoltage.restype = c_int
cmdGetZAxisVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetZAxisVoltage = mdtLib.SetZAxisVoltage
cmdSetZAxisVoltage.restype = c_int
cmdSetZAxisVoltage.argtypes = [c_int, c_double]

cmdGetXAxisMinVoltage = mdtLib.GetXAxisMinVoltage
cmdGetXAxisMinVoltage.restype = c_int
cmdGetXAxisMinVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetXAxisMinVoltage = mdtLib.SetXAxisMinVoltage
cmdSetXAxisMinVoltage.restype = c_int
cmdSetXAxisMinVoltage.argtypes = [c_int, c_double]

cmdGetYAxisMinVoltage = mdtLib.GetYAxisMinVoltage
cmdGetYAxisMinVoltage.restype = c_int
cmdGetYAxisMinVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetYAxisMinVoltage = mdtLib.SetYAxisMinVoltage
cmdSetYAxisMinVoltage.restype = c_int
cmdSetYAxisMinVoltage.argtypes = [c_int, c_double]

cmdGetZAxisMinVoltage = mdtLib.GetZAxisMinVoltage
cmdGetZAxisMinVoltage.restype = c_int
cmdGetZAxisMinVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetZAxisMinVoltage = mdtLib.SetZAxisMinVoltage
cmdSetZAxisMinVoltage.restype = c_int
cmdSetZAxisMinVoltage.argtypes = [c_int, c_double]

cmdGetXAxisMaxVoltage = mdtLib.GetXAxisMaxVoltage
cmdGetXAxisMaxVoltage.restype = c_int
cmdGetXAxisMaxVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetXAxisMaxVoltage = mdtLib.SetXAxisMaxVoltage
cmdSetXAxisMaxVoltage.restype = c_int
cmdSetXAxisMaxVoltage.argtypes = [c_int, c_double]

cmdGetYAxisMaxVoltage = mdtLib.GetYAxisMaxVoltage
cmdGetYAxisMaxVoltage.restype = c_int
cmdGetYAxisMaxVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetYAxisMaxVoltage = mdtLib.SetYAxisMaxVoltage
cmdSetYAxisMaxVoltage.restype = c_int
cmdSetYAxisMaxVoltage.argtypes = [c_int, c_double]

cmdGetZAxisMaxVoltage = mdtLib.GetZAxisMaxVoltage
cmdGetZAxisMaxVoltage.restype = c_int
cmdGetZAxisMaxVoltage.argtypes = [c_int, POINTER(c_double)]

cmdSetZAxisMaxVoltage = mdtLib.SetZAxisMaxVoltage
cmdSetZAxisMaxVoltage.restype = c_int
cmdSetZAxisMaxVoltage.argtypes = [c_int, c_double]

cmdGetVoltageAdjustmentResolutione = mdtLib.GetVoltageAdjustmentResolution
cmdGetVoltageAdjustmentResolutione.restype = c_int
cmdGetVoltageAdjustmentResolutione.argtypes = [c_int, POINTER(c_int)]

cmdSetVoltageAdjustmentResolution = mdtLib.SetVoltageAdjustmentResolution
cmdSetVoltageAdjustmentResolution.restype = c_int
cmdSetVoltageAdjustmentResolution.argtypes = [c_int, c_int]

cmdGetXYZAxisVoltage = mdtLib.GetXYZAxisVoltage
cmdGetXYZAxisVoltage.restype = c_int
cmdGetXYZAxisVoltage.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]

cmdSetXYZAxisVoltage = mdtLib.SetXYZAxisVoltage
cmdSetXYZAxisVoltage.restype = c_int
cmdSetXYZAxisVoltage.argtypes = [c_int, c_double, c_double, c_double]


# endregion

# region command for MDT694B(X-AXIS) and MDT693B(X-AXIS, Y-AXIS, Z-AXIS)
def mdtListDevices():
    """ List all connected MDT devices
    Returns: 
       The mdt device list, each deice item is [serialNumber, mdtType]
    """
    str = create_string_buffer(10240, '\0')
    result = cmdList(str, 10240)
    devicesStr = str.raw.decode("utf-8").rstrip('\x00').split(',')
    length = len(devicesStr)
    i = 0
    devices = []
    devInfo = ["", ""]
    MDTTypeList = ["MDT693B", "MDT694B"]
    while (i < length):
        str = devicesStr[i]
        if (i % 2 == 0):
            if str != '':
                devInfo[0] = str
            else:
                i += 1
        else:
            isFind = False
            for mt in MDTTypeList:
                if (str.find(mt) >= 0):
                    str = mt
                    isFind = True;
                    break
            if (isFind):
                devInfo[1] = str
                devices.append(devInfo.copy())
        i += 1
    return devices


def mdtOpen(serialNo, nBaud, timeout):
    """ Open MDT device
    Args:
        serialNo: serial number of MDT device
        nBaud: bit per second of port
        timeout: set timeout value in (s)
    Returns: 
        non-negative number: hdl number returned Successful; negative number: failed.
    """
    return cmdOpen(serialNo.encode('utf-8'), nBaud, timeout)


def mdtIsOpen(serialNo):
    """ Check opened status of MDT device
    Args:
        serialNo: serial number of MDT device
    Returns: 
        0: MDT device is not opened; 1: MDT device is opened.
    """
    return cmdIsOpen(serialNo.encode('utf-8'))


def mdtClose(hdl):
    """ Close opened MDT device
    Args:
        hdl: the handle of opened MDT device
    Returns: 
        0: Success; negative number: failed.
    """
    return mdtLib.Close(hdl)


def mdtGetId(hdl, id):
    """ Get the product header and firmware version
    Args:
        hdl: the handle of opened MDT device
        id: the output id string
    Returns: 
        0: Success; negative number: failed.
    """
    idStr = create_string_buffer(1024, '\0')
    ret = cmdGetId(hdl, idStr)
    id.append(idStr.raw.decode("utf-8").rstrip('\x00'))
    return ret


def mdtGetLimtVoltage(hdl, voltage):
    """ Get output voltage limit setting.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetLimtVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtGetXAxisVoltage(hdl, voltage):
    """ Get the X axis output voltage.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetXAxisVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetXAxisVoltage(hdl, voltage):
    """ Set the output voltage for the X axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetXAxisVoltage(hdl, voltage)


def mdtGetXAxisMinVoltage(hdl, voltage):
    """ Get the minimum output voltage limit for X axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetXAxisMinVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetXAxisMinVoltage(hdl, voltage):
    """ Set the minimum output voltage limit for X axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetXAxisMinVoltage(hdl, voltage)


def mdtGetXAxisMaxVoltage(hdl, voltage):
    """ Get the maximum output voltage limit for X axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetXAxisMaxVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetXAxisMaxVoltage(hdl, voltage):
    """ Set the maximum output voltage limit for X axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetXAxisMaxVoltage(hdl, voltage)


def mdtGetVoltageAdjustmentResolution(hdl, step):
    """ Get the current step resolution.
    Args:
        hdl: the handle of opened MDT device
        step: current step solution
    Returns: 
        0: Success; negative number: failed.
    """
    sa = c_int(0)
    ret = cmdGetVoltageAdjustmentResolutione(hdl, sa)
    step[0] = sa.value
    return ret


def mdtSetVoltageAdjustmentResolution(hdl, step):
    """ Set the step resolution when using up/down arrow keys.
    Args:
        hdl: the handle of opened MDT device
        step: target step range:(1 ~ 1000)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetVoltageAdjustmentResolution(hdl, step)


# endregion

# region only for MDT693B(X-AXIS, Y-AXIS, Z-AXIS)
def mdtSetAllVoltage(hdl, voltage):
    """ Set all outputs to desired voltage.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetAllVoltage(hdl, voltage)


def mdtGetMasterScanEnable(hdl, state):
    """ Get the state of the Master Scan enable.
    Args:
        hdl: the handle of opened MDT device
        state: current master scan state.(1-enable,0-disable)
    Returns: 
        0: Success; negative number: failed.
    """
    sa = c_int(0)
    ret = cmdGetMasterScanEnable(hdl, sa)
    state[0] = sa.value
    return ret


def mdtSetMasterScanEnable(hdl, state):
    """ Set Master Scan mode.
    Args:
        hdl: the handle of opened MDT device
        state: current master scan state.(1-enable,0-disable)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetMasterScanEnable(hdl, state)


def mdtGetMasterScanVoltage(hdl, voltage):
    """ Get the master scan voltage.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetMasterScanVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetMasterScanVoltage(hdl, voltage):
    """ Set a master scan voltage that adds to the x, y, and z axis voltages.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetMasterScanVoltage(hdl, voltage)


def mdtGetYAxisVoltage(hdl, voltage):
    """ Get the Y axis output voltage.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetYAxisVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetYAxisVoltage(hdl, voltage):
    """ Set the output voltage for the Y axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetYAxisVoltage(hdl, voltage)


def mdtGetZAxisVoltage(hdl, voltage):
    """ Get the Z axis output voltage.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetZAxisVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetZAxisVoltage(hdl, voltage):
    """ Set the output voltage for the Z axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetZAxisVoltage(hdl, voltage)


def mdtGetYAxisMinVoltage(hdl, voltage):
    """ Get the minimum output voltage limit for Y axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetYAxisMinVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetYAxisMinVoltage(hdl, voltage):
    """ Set the minimum output voltage limit for Y axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetYAxisMinVoltage(hdl, voltage)


def mdtGetZAxisMinVoltage(hdl, voltage):
    """ Get the minimum output voltage limit for Z axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetZAxisMinVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetZAxisMinVoltage(hdl, voltage):
    """ Set the minimum output voltage limit for Z axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetZAxisMinVoltage(hdl, voltage)


def mdtGetYAxisMaxVoltage(hdl, voltage):
    """ Get the maximum output voltage limit for Y axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetYAxisMaxVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetYAxisMaxVoltage(hdl, voltage):
    """ Set the maximum output voltage limit for Y axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetYAxisMaxVoltage(hdl, voltage)


def mdtGetZAxisMaxVoltage(hdl, voltage):
    """ Get the maximum output voltage limit for Z axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the output voltage
    Returns: 
        0: Success; negative number: failed.
    """
    vol = c_double(0)
    ret = cmdGetZAxisMaxVoltage(hdl, vol)
    voltage[0] = vol.value
    return ret


def mdtSetZAxisMaxVoltage(hdl, voltage):
    """ Set the maximum output voltage limit for Z axis.
    Args:
        hdl: the handle of opened MDT device
        voltage: the input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetZAxisMaxVoltage(hdl, voltage)


def mdtGetXYZAxisVoltage(hdl, xyzVoltage):
    """ Get the x,y,z axis output voltages.
    Args:
        hdl: the handle of opened MDT device
        xyzVoltage: the output x,y,z axis voltage
    Returns: 
        0: Success; negative number: failed.
    """
    volX = c_double(0)
    volY = c_double(0)
    volZ = c_double(0)
    ret = cmdGetXYZAxisVoltage(hdl, volX, volY, volZ)
    xyzVoltage[0] = volX.value
    xyzVoltage[1] = volY.value
    xyzVoltage[2] = volZ.value
    return ret


def mdtSetXYZAxisVoltage(hdl, xVoltage, yVoltage, zVoltage):
    """ Set the x,y,z axis output voltages.
    Args:
        hdl: the handle of opened MDT device
        xVoltage: the x axis input voltage range:(0 ~ limit voltage)
        yVoltage: the y axis input voltage range:(0 ~ limit voltage)
        zVoltage: the z axis input voltage range:(0 ~ limit voltage)
    Returns: 
        0: Success; negative number: failed.
    """
    return cmdSetXYZAxisVoltage(hdl, xVoltage, yVoltage, zVoltage)

# endregion
