#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations
from core.FadeStickBase import FadeStickBase
from core.pattern.Pattern import Pattern
from utils.Colors import BLACK
from utils.Types import RGB, RangeInt


class FadeStick(FadeStickBase):
    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        string = f"{self.__class__.__name__}[{self.device if self.device else ''}]"
        return string

    def __init__(self, fs: FadeStickBase = None):
        super().__init__(fs.device)

    def blink(self, color: RGB, blinks: int = 1, delay: int = 500):
        blinks = RangeInt(blinks, 1, self.MAX_BLINKS, "blinks")
        delay = RangeInt(delay, 1, self.MAX_DELAY, "delay")

        pattern = Pattern()
        ms_delay: int = round(float(delay) / float(1000))
        for x in range(blinks):
            if x:
                pattern.addColorAndDuration(BLACK, ms_delay)
            pattern.addColorAndDuration(color, ms_delay)
            pattern.addColorAndDuration(BLACK, 0)

        # Send the pattern to the FadeStick


    def morph(self, end_color: RGB, duration: int = 1000, steps: int = 50):
        super().morph(end_color, duration, steps)

    def pulse(self, color: RGB, pulses: int = 1, duration: int = 1000, steps: int = 50):
        super().pulse(color, pulses, duration, steps)


