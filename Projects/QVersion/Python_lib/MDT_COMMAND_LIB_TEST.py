import matplotlib.pyplot as plt

try:
    from Python_lib.MDT_COMMAND_LIB import *
except OSError as ex:
    print("Warning:", ex)


def CommonFunc(serialNumber):
    hdl = mdtOpen(serialNumber, 115200, 3)
    print(hdl)
    # or check by "mdtIsOpen(devs[0])"
    if (hdl < 0):
        print("Connect ", serialNumber, "fail")
        return -1;
    else:
        print("Connect ", serialNumber, "successful")

    result = mdtIsOpen(serialNumber)
    print("mdtIsOpen ", result)

    id = []
    result = mdtGetId(hdl, id)
    if (result < 0):
        print("mdtGetId fail ", result)
    else:
        print(id)

    limitVoltage = [0]
    result = mdtGetLimtVoltage(hdl, limitVoltage)
    if (result < 0):
        print("mdtGetLimtVoltage fail ", result)
    else:
        print("mdtGetLimtVoltage ", limitVoltage)
    return hdl


def Check_X_AXiS(hdl):
    voltage = [0]
    result = mdtGetXAxisVoltage(hdl, voltage)
    if (result < 0):
        print("mdtGetXAxisVoltage fail ", result)
    else:
        print("mdtGetXAxisVoltage ", voltage)

    result = mdtSetXAxisVoltage(hdl, 40)
    if (result < 0):
        print("mdtSetXAxisVoltage fail ", result)
    else:
        print("mdtSetXAxisVoltage ", 40)

    minVoltage = [0]
    result = mdtGetXAxisMinVoltage(hdl, minVoltage)
    if (result < 0):
        print("mdtGetXAxisMinVoltage fail ", result)
    else:
        print("mdtGetXAxisMinVoltage ", minVoltage)

    result = mdtSetXAxisMinVoltage(hdl, 50)
    if (result < 0):
        print("mdtSetXAxisMinVoltage fail ", result)
    else:
        print("mdtSetXAxisMinVoltage ", 50)
    # reset back
    mdtSetXAxisMinVoltage(hdl, minVoltage[0])
    print("mdtSetXAxisMinVoltage ", minVoltage[0])

    maxVoltage = [0]
    result = mdtGetXAxisMaxVoltage(hdl, maxVoltage)
    if (result < 0):
        print("mdtGetXAxisMaxVoltage fail ", result)
    else:
        print("mdtGetXAxisMaxVoltage ", maxVoltage)

    result = mdtSetXAxisMaxVoltage(hdl, 60)
    if (result < 0):
        print("mdtSetXAxisMaxVoltage fail ", result)
    else:
        print("mdtSetXAxisMaxVoltage ", 60)
    # reset back
    mdtSetXAxisMaxVoltage(hdl, maxVoltage[0])
    print("mdtSetXAxisMaxVoltage ", maxVoltage[0])


def Check_Y_AXiS(hdl):
    voltage = [0]
    result = mdtGetYAxisVoltage(hdl, voltage)
    if (result < 0):
        print("mdtGetYAxisVoltage fail ", result)
    else:
        print("mdtGetYAxisVoltage ", voltage)

    result = mdtSetYAxisVoltage(hdl, 40)
    if (result < 0):
        print("mdtSetYAxisVoltage fail ", result)
    else:
        print("mdtSetYAxisVoltage ", 40)

    minVoltage = [0]
    result = mdtGetYAxisMinVoltage(hdl, minVoltage)
    if (result < 0):
        print("mdtGetYAxisMinVoltage fail ", result)
    else:
        print("mdtGetYAxisMinVoltage ", minVoltage)

    result = mdtSetYAxisMinVoltage(hdl, 50)
    if (result < 0):
        print("mdtSetYAxisMinVoltage fail ", result)
    else:
        print("mdtSetYAxisMinVoltage ", 50)
    # reset back
    mdtSetYAxisMinVoltage(hdl, minVoltage[0])
    print("mdtSetYAxisMinVoltage ", minVoltage[0])

    maxVoltage = [0]
    result = mdtGetYAxisMaxVoltage(hdl, maxVoltage)
    if (result < 0):
        print("mdtGetYAxisMaxVoltage fail ", result)
    else:
        print("mdtGetYAxisMaxVoltage ", maxVoltage)

    result = mdtSetYAxisMaxVoltage(hdl, 40)
    if (result < 0):
        print("mdtSetYAxisMaxVoltage fail ", result)
    else:
        print("mdtSetYAxisMaxVoltage ", 40)
    # reset back
    mdtSetYAxisMaxVoltage(hdl, maxVoltage[0])
    print("mdtSetYAxisMaxVoltage ", maxVoltage[0])


def Check_Z_AXiS(hdl):
    voltage = [0]
    result = mdtGetZAxisVoltage(hdl, voltage)
    if (result < 0):
        print("mdtGetZAxisVoltage fail ", result)
    else:
        print("mdtGetZAxisVoltage ", voltage)

    result = mdtSetZAxisVoltage(hdl, 40)
    if (result < 0):
        print("mdtSetZAxisVoltage fail ", result)
    else:
        print("mdtSetZAxisVoltage ", 40)

    minVoltage = [0]
    result = mdtGetZAxisMinVoltage(hdl, minVoltage)
    if (result < 0):
        print("mdtGetZAxisMinVoltage fail ", result)
    else:
        print("mdtGetZAxisMinVoltage ", minVoltage)

    result = mdtSetZAxisMinVoltage(hdl, 50)
    if (result < 0):
        print("mdtSetZAxisMinVoltage fail ", result)
    else:
        print("mdtSetZAxisMinVoltage ", 50)
    # reset back
    mdtSetZAxisMinVoltage(hdl, minVoltage[0])
    print("mdtSetZAxisMinVoltage ", minVoltage[0])

    maxVoltage = [0]
    result = mdtGetZAxisMaxVoltage(hdl, maxVoltage)
    if (result < 0):
        print("mdtGetZAxisMaxVoltage fail ", result)
    else:
        print("mdtGetZAxisMaxVoltage ", maxVoltage)

    result = mdtSetZAxisMaxVoltage(hdl, 60)
    if (result < 0):
        print("mdtSetZAxisMaxVoltage fail ", result)
    else:
        print("mdtSetZAxisMaxVoltage ", 60)
    # reset back
    mdtSetZAxisMaxVoltage(hdl, maxVoltage[0])
    print("mdtSetZAxisMaxVoltage ", maxVoltage[0])


def MDT694BExample(serialNumber):
    hdl = CommonFunc(serialNumber)
    if (hdl < 0):
        return
    Check_X_AXiS(hdl)
    result = mdtClose(hdl)
    if (result == 0):
        print("mdtClose ", serialNumber)
    else:
        print("mdtClose fail", result)
    result = mdtIsOpen(serialNumber)
    print("mdtIsOpen ", result)


def MDT693BExample(serialNumber):
    hdl = CommonFunc(serialNumber)
    if (hdl < 0):
        return
    Check_X_AXiS(hdl)
    Check_Y_AXiS(hdl)
    Check_Z_AXiS(hdl)

    result = mdtSetMasterScanEnable(hdl, 0)
    if (result < 0):
        print("mdtSetMasterScanEnable fail ", result)
    else:
        print("mdtSetMasterScanEnable ", 0)

    result = mdtSetAllVoltage(hdl, 5)
    if (result < 0):
        print("mdtSetAllVoltage fail ", result)
    else:
        print("mdtSetAllVoltage ", 5)

    xVoltage = 10
    yVoltage = 20
    zVoltage = 30
    result = mdtSetXYZAxisVoltage(hdl, xVoltage, yVoltage, zVoltage)
    if (result < 0):
        print("mdtSetXYZAxisVoltage fail ", result)
    else:
        print("mdtSetXYZAxisVoltage ", xVoltage, yVoltage, zVoltage)
    plt.pause(2)
    xyzVoltage = [0, 0, 0]
    result = mdtGetXYZAxisVoltage(hdl, xyzVoltage)
    if (result < 0):
        print("mdtGetXYZAxisVoltage fail ", result)
    else:
        print("mdtGetXYZAxisVoltage ", xyzVoltage)

    state = [0]
    result = mdtGetMasterScanEnable(hdl, state)
    if (result < 0):
        print("mdtGetMasterScanEnable fail ", result)
    else:
        print("mdtGetMasterScanEnable ", state)

    result = mdtSetMasterScanEnable(hdl, 1)
    if (result < 0):
        print("mdtSetMasterScanEnable fail ", result)
    else:
        print("mdtSetMasterScanEnable ", 1)

    result = mdtSetMasterScanVoltage(hdl, 5)
    if (result < 0):
        print("mdtSetMasterScanVoltage fail ", result)
    else:
        print("mdtSetMasterScanVoltage ", 5)

    masterVoltage = [0]
    result = mdtGetMasterScanVoltage(hdl, masterVoltage)
    if (result < 0):
        print("mdtGetMasterScanVoltage fail ", result)
    else:
        print("mdtGetMasterScanVoltage ", masterVoltage)
    result = mdtClose(hdl)
    if (result == 0):
        print("mdtClose ", serialNumber)
    else:
        print("mdtClose fail", result)
    result = mdtIsOpen(serialNumber)
    print("mdtIsOpen ", result)

