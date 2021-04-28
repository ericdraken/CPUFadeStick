#  Copyright (c) Eric Draken, 2021.
from typing import NamedTuple
from usb.core import Device

# Assignment over alias preferred for export
USBDevice = Device

class RGB(NamedTuple):
    red: int
    green: int
    blue: int
