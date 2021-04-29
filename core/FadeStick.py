#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations
from core.FadeStickBase import FadeStickBase
from utils.Types import RGB


class FadeStick(FadeStickBase):
    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        string = f"{self.__class__.__name__}[{self.device if self.device else ''}]"
        return string

    def __init__(self, fs: FadeStickBase = None):
        super().__init__(fs.device)

    def blink(self, color: RGB, blinks: int = 1, delay: int = 500):
        super().blink(color, blinks, delay)

    def morph(self, end_color: RGB, duration: int = 1000, steps: int = 50):
        super().morph(end_color, duration, steps)

    def pulse(self, color: RGB, pulses: int = 1, duration: int = 1000, steps: int = 50):
        super().pulse(color, pulses, duration, steps)


