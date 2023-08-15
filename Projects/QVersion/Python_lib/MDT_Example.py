# This is a sample Python script.
from MDT_COMMAND_LIB import mdtListDevices
from MDT_COMMAND_LIB_TEST import MDT693BExample, MDT694BExample


def main():
    print("*** MDT device python example ***")
    try:
        devs = mdtListDevices()
        print(devs)
        if len(devs) <= 0:
            print('There is no devices connected')
            exit()

        for mdt in devs:
            if mdt[1] == "MDT693B":
                MDT693BExample(mdt[0])
            elif mdt[1] == "MDT694B":
                MDT694BExample(mdt[0])
    except Exception as ex:
        print("Warning:", ex)
    print("*** End ***")
    input()


main()
