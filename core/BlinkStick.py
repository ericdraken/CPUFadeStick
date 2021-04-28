#  Copyright (c) Eric Draken, 2021.
import time
from typing import List

from core.FadeStick import FadeStick
from utils.Types import RGB, RangeInt

class BlinkStick(FadeStick):
    def __init__(self, fs: FadeStick = None):
        super().__init__(fs.device)

    # Original blink logic that slows the CPU
    def blink(self, color: RGB, blinks: int = 1, delay: int = 500):
        blinks = RangeInt(blinks, 1, 100, "blinks")
        delay = RangeInt(delay, 1, 5000, "delay")

        ms_delay = float(delay) / float(1000)
        for x in range(blinks):
            if x:
                time.sleep(ms_delay)
            self.setColor(color)
            time.sleep(ms_delay)
            self.turnOff()

    # Original morph logic that slows the CPU
    def morph(self, end_color: RGB, duration: int = 1000, steps: int = 50):
        duration = RangeInt(duration, 1, 5000, "duration")
        steps = RangeInt(steps, 1, 100, "steps")

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
            gradient.append(RGB(r, g, b))

        ms_delay = float(duration) / float(1000 * steps)

        self.setColor(start_color)
        for grad in gradient:
            self.setColor(grad)
            time.sleep(ms_delay)
        self.setColor(end_color)

    # Original pulse logic that slows the CPU
    def pulse(self, color: RGB, pulses: int = 1, duration: int = 1000, steps: int = 50):
        pulses = RangeInt(pulses, 1, 100, "pulses")
        duration = RangeInt(duration, 1, 5000, "duration")
        steps = RangeInt(steps, 1, 100, "steps")

        self.turnOff()
        for x in range(pulses):
            self.morph(color, duration=duration, steps=steps)
            self.morph(RGB(0, 0, 0), duration=duration, steps=steps)
