#  Copyright (c) Eric Draken, 2021.
import sys
import time
from typing import Final

from daemonize import Daemonize
from usb.core import USBError

from core.CPU import CPU
from core.FadeStick import FadeStick
from core.FadeStickUSB import findFirstFadeStick
from exceptions.FadeStickException import FadeStickException
from utils.Colors import scaleToRGB

if sys.platform == "win32":
    raise FadeStickException("Windows is not supported")

def main():
    cpu: Final = CPU()
    fs = FadeStick(findFirstFadeStick())
    period_ms = 1000
    for _ in range(20):
        cpu_per: float = cpu.getCPUTimeSlicePercentage()
        print(f"CPU {cpu_per * 100.0:.2f}%")
        try:
            fs.morph(scaleToRGB(cpu_per), period_ms)
            time.sleep(period_ms / 1000.0)
        except USBError:
            # Try to get another handle if the CPU load is too high
            fs = FadeStick(findFirstFadeStick())
    fs.turnOff()

if __name__ == '__main__':
    # script_path = str(os.path.dirname(os.path.abspath(__file__)))
    # print(script_path)
    # sha1 = hashlib.sha1(script_path.encode("utf-8")).hexdigest()
    # app_name = f"cpufadestick-{sha1}"
    app_name = f"cpufadestick"
    pidfile = f"/tmp/{app_name}"
    daemon = Daemonize(app=app_name, pid=pidfile, action=main)
    daemon.start()
