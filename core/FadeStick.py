#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations

from math import floor
from typing import Final

from constants.FadeStickConsts import FS_MODE_PATTERN
from core.FadeStickBase import FadeStickBase
from core.pattern.Pattern import Pattern, ColorDuration
from utils.Colors import OFF
from utils.Types import RGB, RangeInt


class FadeStick(FadeStickBase):
    MAX_BLINKS: Final = Pattern.MAX_BUFFER_SIZE // 2
    MAX_DELAY: Final = ColorDuration.MAX_DURATION
    MAX_DURATION: Final = ColorDuration.MAX_DURATION
    MAX_STEPS: Final = Pattern.MAX_BUFFER_SIZE

    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        string = f"{self.__class__.__name__}[{self.device if self.device else ''}]"
        return string

    def __init__(self, fs: FadeStickBase = None):
        super().__init__(fs.device)

    def blink(self, color: RGB, blinks: int = 1, delay_ms: int = 500) -> None:
        blinks = RangeInt(blinks, 1, self.MAX_BLINKS, "blinks")
        delay_ms = RangeInt(delay_ms, 1, self.MAX_DELAY, "delay_ms")

        pattern = Pattern()
        for x in range(blinks):
            if x:
                pattern.addColorAndDuration(OFF, delay_ms)
            pattern.addColorAndDuration(color, delay_ms)
        pattern.addColorAndDuration(OFF, 0)

        # Send the pattern to the FadeStick
        payload = pattern.getBytePattern()

        from core.FadeStickUSB import sendControlTransfer, R_USB_SEND, R_SET_CONFIG
        sendControlTransfer(self, R_USB_SEND, R_SET_CONFIG, FS_MODE_PATTERN, payload)

    # noinspection DuplicatedCode
    def morph(self, end_color: RGB, duration: int = 1000, steps: int = MAX_STEPS) -> None:
        duration = RangeInt(duration, 1, self.MAX_DURATION, "duration")
        steps = RangeInt(steps, 1, self.MAX_STEPS, "steps")

        r_end, g_end, b_end = end_color
        start_color = self.getColor()
        r_start, g_start, b_start = start_color
        pattern: Pattern = Pattern()
        ms_delay = floor(float(duration) / float(steps))

        for n in range(0, steps):  # Range is exclusive
            d = 1.0 * (n + 1) / float(steps)
            r = (r_start * (1 - d)) + (r_end * d)
            g = (g_start * (1 - d)) + (g_end * d)
            b = (b_start * (1 - d)) + (b_end * d)
            pattern.addColorAndDuration(RGB(r, g, b), ms_delay)

        # Send the pattern to the FadeStick
        payload = pattern.getBytePattern()

        from core.FadeStickUSB import sendControlTransfer
        from core.FadeStickUSB import R_USB_SEND
        from core.FadeStickUSB import R_SET_CONFIG
        sendControlTransfer(self, R_USB_SEND, R_SET_CONFIG, FS_MODE_PATTERN, payload)


    # def pulse(self, color: RGB, pulses: int = 1, duration: int = 1000, steps: int = 50) -> None:
    #     pulses = RangeInt(pulses, 1, self.MAX_PULSES, "pulses")
    #     duration = RangeInt(duration, 1, self.MAX_DURATION, "duration")
    #     steps = RangeInt(steps, 1, self.MAX_STEPS, "steps")
    #
    #     self.turnOff()
    #     for x in range(pulses):
    #         self.morph(color, duration=duration, steps=steps)
    #         self.morph(OFF, duration=duration, steps=steps)


