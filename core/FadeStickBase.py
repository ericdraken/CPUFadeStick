#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations

from abc import abstractmethod, ABCMeta
from typing import Final

from multipledispatch import dispatch

from constants.FadeStickConsts import FS_SERIAL_INDEX, FS_REPORT_ID
from exceptions.FadeStickColorException import FadeStickColorException
from utils.Colors import invertRGB, colorToHex, hexToRGB
from utils.Decorators import abstract
from utils.Types import RGB, USBDevice


class FadeStickBase(object):
    MAX_BLINKS: Final = 100
    MAX_DELAY: Final = 5000
    MAX_DURATION: Final = 5000
    MAX_STEPS: Final = 100
    MAX_PULSES: Final = 100

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
            rgb = invertRGB(rgb)

        control_string = bytes(bytearray([0, rgb.red, rgb.green, rgb.blue]))

        from core.FadeStickUSB import sendControlTransfer
        sendControlTransfer(self, 0x20, 0x9, FS_REPORT_ID, 0, control_string)
        return rgb

    def turnOff(self) -> None:
        self.setColor(0, 0, 0)

    def getColor(self) -> RGB:
        from core.FadeStickUSB import sendControlTransfer
        device_bytes = sendControlTransfer(self, 0x80 | 0x20, 0x1, 0x0001, 0, 33)
        rgb = RGB(device_bytes[1], device_bytes[2], device_bytes[3])
        return invertRGB(rgb) if self.inverse else rgb

    @abstract
    def blink(self, color: RGB, blinks: int = 1, delay: int = 500): ...

    @abstract
    def morph(self, end_color: RGB, duration: int = 1000, steps: int = 50): ...

    @abstract
    def pulse(self, color: RGB, pulses: int = 1, duration: int = 1000, steps: int = 50): ...
