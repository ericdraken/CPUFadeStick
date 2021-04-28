#  Copyright (c) Eric Draken, 2021.
from typing import NamedTuple, Iterable, Tuple, Any
from usb.core import Device

# Assignment over alias preferred for export
from exceptions.FadeStickColorException import FadeStickColorException

USBDevice = Device

class RGB(NamedTuple("RGB", [("red", int), ("green", int), ("blue", int)])):
    def __new__(cls, red, green, blue):
        if not all([
            0 <= red <= 255,
            0 <= green <= 255,
            0 <= blue <= 255,
        ]):
            raise FadeStickColorException(f"One ore more colors are "
                                          f"below 0 or above 255. Given {red}, {green}, {blue}.")
        # noinspection PyArgumentList
        return super().__new__(cls, int(red), int(green), int(blue))
