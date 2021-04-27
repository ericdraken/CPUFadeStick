#  Copyright (c) Eric Draken, 2021.
import sys

from core.FadeStickUSB import findAllFadeSticks
from exceptions.FadeStickException import FadeStickException

if sys.platform == "win32":
    raise FadeStickException("Windows is not supported")

def main():
    print(f'Found FadeSticks:')

    devices = findAllFadeSticks()
    print(devices)


if __name__ == "__main__":
    sys.exit(main())
