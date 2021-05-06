#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations

from typing import Optional, List, Final, Union

import usb
from multipledispatch import dispatch

from constants.FadeStickConsts import FS_VENDOR_ID, FS_PRODUCT_ID, FS_MESSAGE_ID, \
    FS_SERIAL_INDEX, FS_MANUFACTURER_INDEX, FS_DESCRIPTION_INDEX
from core.FadeStickBase import FadeStickBase
from exceptions.FadeStickUSBException import FadeStickUSBException
from utils.Types import USBDevice

# REF: https://www.beyondlogic.org/usbnutshell/usb6.shtml
# mRequestType
RT_HOST_TO_DEVICE: Final = 0x0  # Send
RT_DEVICE_TO_HOST: Final = 0x80  # Receive
RT_TYPE_VENDOR: Final = 0x20  # Vendor
R_USB_SEND: Final = RT_HOST_TO_DEVICE | RT_TYPE_VENDOR
R_USB_RECV: Final = RT_DEVICE_TO_HOST | RT_TYPE_VENDOR

# mRequest
R_SET_CONFIG: Final = 0x9
R_CLEAR_FEATURE: Final = 0x1


def setUSBUDevRule():
    try:
        filename = "/etc/udev/rules.d/85-fadestick.rules"
        file = open(filename, 'w')
        file.write(
            'SUBSYSTEM=="usb", ATTR{idVendor}=="20a0", ATTR{idProduct}=="41e5", MODE:="0666"')
        file.close()
        print(f"Rule added to {filename}")
    except IOError as e:
        print(str(e))
        print("Make sure you run this script as root: sudo fadestick --add-udev-rule")
        return 64

    print("Reboot your computer for changes to take effect, or run "
          "udevadm control --reload-rules && udevadm trigger")
    return 0


def findAllFadeSticks() -> List[FadeStickBase]:
    results: List[FadeStickBase] = []
    for d in _findFadeSticksAsGenerator():
        results.extend([FadeStickBase(device=d)])
    return results


def findFirstFadeStick() -> FadeStickBase:
    for d in _findFadeSticksAsGenerator():
        return FadeStickBase(device=d)

    raise FadeStickUSBException("No FadeSticks found")


def findFadeStickBySerial(serial: str) -> FadeStickBase:
    devices: List[USBDevice] = []
    for d in _findFadeSticksAsGenerator():
        try:
            if usb.util.get_string(d, FS_SERIAL_INDEX, FS_MESSAGE_ID) == serial:
                devices = [d]
                break
        except Exception as e:
            print("{0}".format(e))

    if devices:
        return FadeStickBase(device=devices[0])


def _findFadeSticksAsGenerator() -> Optional[USBDevice]:
    return usb.core.find(find_all=True, idVendor=FS_VENDOR_ID, idProduct=FS_PRODUCT_ID)


@dispatch(FadeStickBase, int)
def getUSBString(fs: FadeStickBase, index: int) -> str:
    return getUSBString(fs.device, index, "")


@dispatch(USBDevice, int)
def getUSBString(device: USBDevice, index: int) -> str:
    return getUSBString(device, index, "")


@dispatch(USBDevice, int, str)
def getUSBString(fs: FadeStickBase, index: int, serial: str) -> str:
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
                raise FadeStickUSBException(
                    f"Could not communicate with FadeStick {serial} - it may have been removed")
        else:
            raise FadeStickUSBException(
                f"Could not communicate with FadeStick {device} - it may have been removed")


def getManufacturer(fs: FadeStickBase):
    return getUSBString(fs.device, FS_MANUFACTURER_INDEX)


def getDescription(fs: FadeStickBase):
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


def sendControlTransfer(fs: FadeStickBase,
                        requestType: int,
                        request: int,
                        valueOrMode: int,
                        dataOrLength: Union[bytes, int],
                        timeout: int = 5000):
    # Widen the data and add the value
    if type(dataOrLength) is bytes:
        dataOrLength = bytes([valueOrMode]) + dataOrLength

    try:
        return fs.device.ctrl_transfer(requestType, request, valueOrMode, 0,
                                       dataOrLength, timeout)
    except usb.USBError:
        # Could not communicate with FadeStick device
        # attempt to find it again based on serial
        if findFadeStickBySerial(fs.serial):
            return fs.device.ctrl_transfer(requestType, request, valueOrMode, 0,
                                           dataOrLength, timeout)
        else:
            raise FadeStickUSBException(
                f"Could not communicate with FadeStick {fs.serial} - it may have been removed")
