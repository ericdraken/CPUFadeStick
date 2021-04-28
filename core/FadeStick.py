#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations
from typing import Final

from multipledispatch import dispatch

from constants.FadeStickConsts import FS_SERIAL_INDEX, FS_REPORT_ID
from exceptions.FadeStickColorException import FadeStickColorException
from utils.Colors import invertRGB, colorToHex, hexToRGB
from utils.Types import RGB, USBDevice


class FadeStick(object):
    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        string = "TODO"  # TODO: this
        return string

    serial: str = ""
    device: USBDevice = None
    error_reporting: bool = True
    inverse: bool = False

    def __init__(self, device: USBDevice = None, error_reporting=True):
        self.error_reporting: Final = error_reporting

        if device:
            from core.FadeStickUSB import openUSBDevice, getUSBString
            self.device: Final = device
            openUSBDevice(device)
            self.serial: Final = getUSBString(device, FS_SERIAL_INDEX)

    @dispatch(str)
    def setColor(self, name_or_hex: str) -> RGB:
        try:
            return self.setColor(hexToRGB(colorToHex(name_or_hex)))
        except FadeStickColorException:
            return self.setColor(hexToRGB(name_or_hex))

    @dispatch(int, int, int)
    def setColor(self, red: int, green: int, blue: int) -> RGB:
        return self.setColor(RGB(red, green, blue))

    # noinspection PyBroadException
    @dispatch(RGB)
    def setColor(self, rgb: RGB) -> RGB:
        if self.inverse:
            rgb = invertRGB(rgb)

        control_string = bytes(bytearray([0, rgb.red, rgb.green, rgb.blue]))

        from core.FadeStickUSB import sendControlTransfer
        if self.error_reporting:
            sendControlTransfer(self, 0x20, 0x9, FS_REPORT_ID, 0, control_string)
        else:
            try:
                sendControlTransfer(self, 0x20, 0x9, FS_REPORT_ID, 0, control_string)
            except Exception:
                pass

        return rgb

    def turnOff(self) -> None:
        self.setColor(0, 0, 0)

    def getColor(self) -> RGB:
        from core.FadeStickUSB import sendControlTransfer
        device_bytes = sendControlTransfer(self, 0x80 | 0x20, 0x1, 0x0001, 0, 33)
        rgb = RGB(device_bytes[1], device_bytes[2], device_bytes[3])
        return invertRGB(rgb) if self.inverse else rgb
