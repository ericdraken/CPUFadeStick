#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations
import logging
from typing import List, Final, Any
from utils.Types import RGB, RangeInt


class ColorDuration:
    MAX_DURATION: Final = 2_550

    def __init__(self, color: RGB, duration: int) -> None:
        self.color: Final[RGB] = color
        self.duration: Final[int] = RangeInt(duration, 1, self.MAX_DURATION, "duration")

    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        string = f"({self.color}, {self.duration}ms)"
        return string


class Pattern:
    MAX_BUFFER_SIZE: Final = 62
    DURATION_RESOLUTION: Final = 10.0
    _pattern: List[ColorDuration]

    def __new__(cls) -> Any:
        logging.basicConfig(level=logging.INFO)
        cls.log = logging.getLogger(cls.__name__)

    def __init__(self) -> None:
        _pattern: List[ColorDuration] = []

    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        string = f"{self.__class__.__name__}[{self._pattern}]"
        return string

    def addColorAndDuration(self, color: RGB, duration: int):
        if len(self._pattern) >= self.MAX_BUFFER_SIZE:
            self.log.warning(f"The max color buffer size is {self.MAX_BUFFER_SIZE}. "
                             f"Not adding new entry ({color}, {duration}).")
            return None
            # raise PatternException(f"The max color buffer size is {self.MAX_BUFFER_SIZE}")

        self._pattern.append(ColorDuration(color, duration))

    def getPattern(self) -> List[ColorDuration]:
        # REF: https://www.geeksforgeeks.org/python-cloning-copying-list/
        # REF: https://stackoverflow.com/a/22796367/1938889
        return self._pattern[:]

    def __len__(self) -> int:
        return len(self._pattern)


