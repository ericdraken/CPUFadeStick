#  Copyright (c) Eric Draken, 2021.
import time
from typing import List

from core.FadeStick import FadeStick
from utils.Types import RGB

class BlinkStick(FadeStick):
    def __init__(self, fs: FadeStick = None):
        super().__init__(fs.device)

    # Original blink method that slows the CPU
    def blink(self, color: RGB, repeats: int = 1, delay: int = 500):
        assert repeats > 0
        assert delay > 0
        ms_delay = float(delay) / float(1000)
        for x in range(repeats):
            if x:
                time.sleep(ms_delay)
            self.setColor(color)
            time.sleep(ms_delay)
            self.turnOff()

    # Original blink method that slows the CPU
    def morph(self, end_color: RGB, duration: int = 1000, steps: int = 50):
        assert steps > 0
        assert duration > 0
        r_end, g_end, b_end = end_color
        start_color = self.getColor()
        r_start, g_start, b_start = start_color
        gradient: List[RGB] = []

        steps += 1
        for n in range(1, steps):
            d = 1.0 * n / steps
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

    def pulse(self, color: RGB, pulses: int = 1, duration: int = 1000, steps: int = 50):
        assert pulses > 0
        assert steps > 0
        assert duration > 0
        self.turnOff()
        for x in range(pulses):
            self.morph(color, duration=duration, steps=steps)
            self.morph(RGB(0, 0, 0), duration=duration, steps=steps)
