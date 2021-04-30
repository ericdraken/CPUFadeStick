#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations

from constants.FadeStickConsts import FS_MODE_PATTERN
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

    def blink(self, color: RGB, blinks: int = 1, delay_ms: int = 500) -> None:
        blinks = RangeInt(blinks, 1, self.MAX_BLINKS, "blinks")
        delay_ms = RangeInt(delay_ms, 1, self.MAX_DELAY, "delay_ms")

        pattern = Pattern()
        for x in range(blinks):
            if x:
                pattern.addColorAndDuration(BLACK, delay_ms)
            pattern.addColorAndDuration(color, delay_ms)
        pattern.addColorAndDuration(BLACK, 0)

        # Send the pattern to the FadeStick
        payload = pattern.getBytePattern()

        from core.FadeStickUSB import sendControlTransfer, R_USB_SEND, R_SET_CONFIG
        sendControlTransfer(self, R_USB_SEND, R_SET_CONFIG, FS_MODE_PATTERN, payload)

    def morph(self, end_color: RGB, duration: int = 1000, steps: int = 50) -> None:
        super().morph(end_color, duration, steps)

    def pulse(self, color: RGB, pulses: int = 1, duration: int = 1000, steps: int = 50) -> None:
        super().pulse(color, pulses, duration, steps)


