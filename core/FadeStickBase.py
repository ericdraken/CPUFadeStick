#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations

from typing import Final

from multipledispatch import dispatch

from constants.FadeStickConsts import FS_SERIAL_INDEX, FS_MODE_COLOR
from exceptions.FadeStickColorException import FadeStickColorException
from utils import Colors
from utils.Colors import invertRGB, colorToHex, hexToRGB
from utils.Decorators import abstract
from utils.Types import RGB, USBDevice


class FadeStickBase(object):
    serial: str = ""
    device: USBDevice = None
    inverse: bool = False

    def __init__(self, device: USBDevice = None):
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
            rgb: RGB = invertRGB(rgb)

        payload = bytes([rgb.red, rgb.green, rgb.blue])  #

        from core.FadeStickUSB import sendControlTransfer, R_USB_SEND, R_SET_CONFIG
        sendControlTransfer(self, R_USB_SEND, R_SET_CONFIG, FS_MODE_COLOR, payload)
        return rgb

    def turnOff(self) -> None:
        self.setColor(0, 0, 0)

    def getColor(self) -> RGB:
        from core.FadeStickUSB import sendControlTransfer, R_USB_RECV, R_CLEAR_FEATURE
        device_bytes = sendControlTransfer(self, R_USB_RECV, R_CLEAR_FEATURE,
                                           FS_MODE_COLOR, dataOrLength=4)
        rgb = RGB(device_bytes[1], device_bytes[2], device_bytes[3])
        return invertRGB(rgb) if self.inverse else rgb

    def isOff(self) -> bool:
        return self.getColor() == Colors.OFF

    @abstract
    def blink(self, color: RGB, blinks: int = 1, delay: int = 500) -> None:
        ...

    @abstract
    def morph(self, end_color: RGB, duration: int = 1000, steps: int = 50) -> None:
        ...

    @abstract
    def pulse(self, color: RGB, pulses: int = 1, duration: int = 1000,
              steps: int = 50) -> None:
        ...
