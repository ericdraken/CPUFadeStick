#  Copyright (c) Eric Draken, 2021.
from multimethod import isa, overload
from typing import Optional, List

import usb
from usb.core import Device

from constants.FadeStickConsts import FS_VENDOR_ID, FS_PRODUCT_ID, FS_MESSAGE_ID, FS_BYTE_INDEX
from core.FadeStick import FadeStick
from exceptions.FadeStickUSBException import FadeStickUSBException

def setUSBUDevRule():
    try:
        filename = "/etc/udev/rules.d/85-blinkstick.rules"
        file = open(filename, 'w')
        file.write('SUBSYSTEM=="usb", ATTR{idVendor}=="20a0", ATTR{idProduct}=="41e5", MODE:="0666"')
        file.close()
        print("Rule added to {0}".format(filename))
    except IOError as e:
        print(str(e))
        print("Make sure you run this script as root: sudo fadestick --add-udev-rule")
        return 64

    print("Reboot your computer for changes to take effect, or run "
          "udevadm control --reload-rules && udevadm trigger")
    return 0

def findAllFadeSticks() -> List[FadeStick]:
    results: List[FadeStick] = []
    for d in _findFadeSticksAsGenerator():
        results.extend([FadeStick(device=d)])
    return results

def findFirstFadeStick() -> FadeStick:
    device: Device = next(_findFadeSticksAsGenerator())
    if device:
        return FadeStick(device=device)

    raise FadeStickUSBException("No FadeSticks found")

def findFadeStickBySerial(serial=None) -> FadeStick:
    devices: List[Device] = []
    for d in _findFadeSticksAsGenerator():
        try:
            if usb.util.get_string(d, FS_BYTE_INDEX, FS_MESSAGE_ID) == serial:
                devices = [d]
                break
        except Exception as e:
            print("{0}".format(e))

    if devices:
        return FadeStick(device=devices[0])

def _findFadeSticksAsGenerator() -> Optional[Device]:
    return usb.core.find(find_all=True, idVendor=FS_VENDOR_ID, idProduct=FS_PRODUCT_ID)

@overload
def getUSBString(device: isa(FadeStick), index=FS_BYTE_INDEX, serial=None):
    return getUSBString(device.device, index, serial)

@overload
def getUSBString(device: isa(Device), index=FS_BYTE_INDEX, serial=None):
    try:
        return usb.util.get_string(device, index, FS_MESSAGE_ID)
    except usb.USBError:
        # Could not communicate with FadeStick device
        # attempt to find it again based on serial
        device = findFadeStickBySerial(serial)
        if device:
            return usb.util.get_string(device, index, FS_MESSAGE_ID)
        else:
            raise FadeStickUSBException(f"Could not communicate with FadeStick {serial} - it may have been removed")

def openUSBDevice(device: Device):
    if device is None:
        raise FadeStickUSBException("FadeStick device not supplied or is None")

    if device.is_kernel_driver_active(0):
        try:
            device.detach_kernel_driver(0)
        except usb.core.USBError as e:
            raise FadeStickUSBException(f"Could not detach USB kernel driver: {str(e)}")

    return True
