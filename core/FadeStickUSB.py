#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations

import usb
from typing import Optional, List, Any
from multipledispatch import dispatch
from constants.FadeStickConsts import FS_VENDOR_ID, FS_PRODUCT_ID, FS_MESSAGE_ID, \
    FS_SERIAL_INDEX, FS_MANUFACTURER_INDEX, FS_DESCRIPTION_INDEX
from exceptions.FadeStickUSBException import FadeStickUSBException
from utils.Types import USBDevice

from core.FadeStick import FadeStick


def setUSBUDevRule():
    try:
        filename = "/etc/udev/rules.d/85-fadestick.rules"
        file = open(filename, 'w')
        file.write('SUBSYSTEM=="usb", ATTR{idVendor}=="20a0", ATTR{idProduct}=="41e5", MODE:="0666"')
        file.close()
        print(f"Rule added to {filename}")
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
    device: USBDevice = next(_findFadeSticksAsGenerator())
    if device:
        return FadeStick(device=device)

    raise FadeStickUSBException("No FadeSticks found")

def findFadeStickBySerial(serial: str) -> FadeStick:
    devices: List[USBDevice] = []
    for d in _findFadeSticksAsGenerator():
        try:
            if usb.util.get_string(d, FS_SERIAL_INDEX, FS_MESSAGE_ID) == serial:
                devices = [d]
                break
        except Exception as e:
            print("{0}".format(e))

    if devices:
        return FadeStick(device=devices[0])

def _findFadeSticksAsGenerator() -> Optional[USBDevice]:
    return usb.core.find(find_all=True, idVendor=FS_VENDOR_ID, idProduct=FS_PRODUCT_ID)

@dispatch(FadeStick, int)
def getUSBString(fs: FadeStick, index: int) -> str:
    return getUSBString(fs.device, index, "")

@dispatch(USBDevice, int)
def getUSBString(device: USBDevice, index: int) -> str:
    return getUSBString(device, index, "")

@dispatch(USBDevice, int, str)
def getUSBString(fs: FadeStick, index: int, serial: str) -> str:
    return getUSBString(fs.device, index, serial)

@dispatch(USBDevice, int, str)
def getUSBString(device: USBDevice, index: int, serial: str) -> str:
    """
    Returns the serial number of device.::
        FSnnnnnn-1.5
        ||  |    | |- Software minor version
        ||  |    |--- Software major version
        ||  |-------- Denotes sequential number
        ||----------- Denotes FadeStick device
    """
    try:
        return usb.util.get_string(device, index, FS_MESSAGE_ID)
    except usb.USBError:
        if serial and len(serial):
            # Could not communicate with FadeStick device
            # attempt to find it again based on serial
            device = findFadeStickBySerial(serial)
            if device:
                return usb.util.get_string(device, index, FS_MESSAGE_ID)
            else:
                raise FadeStickUSBException(f"Could not communicate with FadeStick {serial} - it may have been removed")
        else:
            raise FadeStickUSBException(f"Could not communicate with FadeStick {device} - it may have been removed")

def getManufacturer(fs: FadeStick):
    return getUSBString(fs.device, FS_MANUFACTURER_INDEX)

def getDescription(fs: FadeStick):
    return getUSBString(fs.device, FS_DESCRIPTION_INDEX)

def openUSBDevice(device: USBDevice):
    if device is None:
        raise FadeStickUSBException("USB device not supplied or is None")

    if device.is_kernel_driver_active(0):
        try:
            device.detach_kernel_driver(0)
        except usb.core.USBError as e:
            raise FadeStickUSBException(f"Could not detach USB kernel driver: {str(e)}")

    return True

def sendControlTransfer(fs: FadeStick, requestType: int,
                        request: int, value: Any, index: int,
                        dataOrLength: Any = None, timeout: int = 5000):
    try:
        return fs.device.ctrl_transfer(requestType, request, value, index, dataOrLength, timeout)
    except usb.USBError:
        # Could not communicate with FadeStick device
        # attempt to find it again based on serial
        if findFadeStickBySerial(fs.serial):
            return fs.device.ctrl_transfer(requestType, request, value, index, dataOrLength, timeout)
        else:
            raise FadeStickUSBException(f"Could not communicate with FadeStick {fs.serial} - it may have been removed")
