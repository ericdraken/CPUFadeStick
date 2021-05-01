#  Copyright (c) Eric Draken, 2021.

import time
from typing import Tuple, List, Final

from usb.core import USBError

from core.FadeStick import FadeStick
from core.FadeStickUSB import findFirstFadeStick
from utils.Colors import scaleToRGB


class CPU:
    _prev_time_doing_things: int = 0
    _prev_time_doing_nothing: int = 0

    # TODO: Mutex
    # REF: https://stackoverflow.com/a/54461187/1938889
    @staticmethod
    def getCPUTimes() -> Tuple[int, int]:
        # Read first line from /proc/stat. It should start with "cpu"
        # and contains times spend in various modes by all CPU's totalled.
        #
        with open("/proc/stat", "r") as procfile:
            cputats: List[str] = procfile.readline().split()

        # Sanity check
        if cputats[0] != "cpu":
            raise IOError("First line of /proc/stat not recognized")

        # Refer to "man 5 proc" (search for /proc/stat) for information
        # about which field means what.
        #
        # Here we do calculation as simple as possible:
        #
        # CPU% = 100 * time-doing-things / (time_doing_things + time_doing_nothing)
        user_time = int(cputats[1])    # time spent in user space
        nice_time = int(cputats[2])    # 'nice' time spent in user space
        system_time = int(cputats[3])  # time spent in kernel space

        idle_time = int(cputats[4])    # time spent idly
        iowait_time = int(cputats[5])  # time spent waiting is also doing nothing

        time_doing_things = user_time + nice_time + system_time
        time_doing_nothing = idle_time + iowait_time

        return time_doing_things, time_doing_nothing

    # Range: 0.0 - 1.0
    def getCPUTimeSlicePercentage(self) -> float:
        time_doing_things, time_doing_nothing = CPU.getCPUTimes()
        diff_time_doing_things = time_doing_things - self._prev_time_doing_things
        diff_time_doing_nothing = time_doing_nothing - self._prev_time_doing_nothing
        cpu_percentage = diff_time_doing_things / (diff_time_doing_things + diff_time_doing_nothing)

        # remember current values to subtract next iteration of the loop
        self._prev_time_doing_things = time_doing_things
        self._prev_time_doing_nothing = time_doing_nothing

        return cpu_percentage

if __name__ == "__main__":
    cpu: Final = CPU()
    fs = FadeStick(findFirstFadeStick())
    period_ms = 1000
    for _ in range(30):
        cpu_per: float = cpu.getCPUTimeSlicePercentage()
        print(f"CPU {cpu_per * 100.0:.2f}%")
        try:
            fs.morph(scaleToRGB(cpu_per), period_ms)
            time.sleep(period_ms / 1000.0)
        except USBError:
            # Try to get another handle if the CPU load is too high
            fs = FadeStick(findFirstFadeStick())
    fs.turnOff()
