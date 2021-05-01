#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations
import time
from typing import List, Final

from core.FadeStickBase import FadeStickBase
from utils.Colors import OFF
from utils.Types import RGB, RangeInt

class BlinkStick(FadeStickBase):
    MAX_BLINKS: Final = 100
    MAX_DELAY: Final = 5000
    MAX_DURATION: Final = 5000
    MAX_STEPS: Final = 100
    MAX_PULSES: Final = 100

    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        string = f"{self.__class__.__name__}[{self.device if self.device else ''}]"
        return string

    def __init__(self, fs: FadeStickBase):
        super().__init__(fs.device)

    # Original blink logic that slows the CPU
    def blink(self, color: RGB, blinks: int = 1, delay: int = 500) -> None:
        blinks = RangeInt(blinks, 1, self.MAX_BLINKS, "blinks")
        delay = RangeInt(delay, 1, self.MAX_DELAY, "delay_ms")

        ms_delay = float(delay) / float(1000)
        for x in range(blinks):
            if x:
                time.sleep(ms_delay)
            self.setColor(color)
            time.sleep(ms_delay)
            self.turnOff()

    # Original morph logic that slows the CPU
    # noinspection DuplicatedCode
    def morph(self, end_color: RGB, duration: int = 1000, steps: int = 50) -> None:
        duration = RangeInt(duration, 1, self.MAX_DURATION, "duration")
        steps = RangeInt(steps, 1, self.MAX_STEPS, "steps")

        r_end, g_end, b_end = end_color
        start_color = self.getColor()
        r_start, g_start, b_start = start_color
        gradient: List[RGB] = []

        steps += 1
        for n in range(1, steps):
            d = 1.0 * n / float(steps)
            r = (r_start * (1 - d)) + (r_end * d)
            g = (g_start * (1 - d)) + (g_end * d)
            b = (b_start * (1 - d)) + (b_end * d)
            gradient.append(RGB(int(r), int(g), int(b)))
        gradient.append(end_color)

        ms_delay = float(duration) / float(1000 * steps)

        for grad in gradient:
            self.setColor(grad)
            time.sleep(ms_delay)
        self.setColor(end_color)

    # Original pulse logic that slows the CPU
    def pulse(self, color: RGB, pulses: int = 1, duration: int = 1000, steps: int = 50) -> None:
        pulses = RangeInt(pulses, 1, self.MAX_PULSES, "pulses")
        duration = RangeInt(duration, 1, self.MAX_DURATION, "duration")
        steps = RangeInt(steps, 1, self.MAX_STEPS, "steps")

        self.turnOff()
        for x in range(pulses):
            self.morph(color, duration=duration, steps=steps)
            self.morph(OFF, duration=duration, steps=steps)
