#  Copyright (c) Eric Draken, 2021.
from typing import NamedTuple, Any, Final
from usb.core import Device

# Assignment over alias preferred for export
from exceptions.FadeStickColorException import FadeStickColorException
from exceptions.NumberExceptions import RangeIntException

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


class RangeInt(int):
    def __init__(self, val: int, min: int, max: int, nice_name: str) -> None:
        self._min: int = min
        self._max: int = max
        self._nice_name: str = nice_name
        self._val: Final[int] = val

    def __new__(cls, *value):
        _val = int(value[0])
        _min = int(value[1])
        _max = int(value[2])
        _nice_name = str(value[3])

        if not _min < _max:
            raise RangeIntException(f"{_nice_name} has "
                                    f"a bad range [{_min}..{_max}]: {_val}")

        if not _min <= _val <= _max:
            raise RangeIntException(f"{_nice_name} is "
                                    f"out of range [{_min}..{_max}]: {_val}")
        return int.__new__(cls, _val)

    def __add__(self, val: int):
        if isinstance(val, RangeInt):
            return RangeInt(self._val + val._val, self._min, self._max, self._nice_name)
        return self._val + val

    def __eq__(self, other):
        if isinstance(other, RangeInt):
            return self._val == other._val
        return self._val == other

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return f"RangeInt({self._nice_name}, [{self._min}..{self._max}]: {self._val})"

