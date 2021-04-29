#  Copyright (c) Eric Draken, 2021.
import sys

import usb

from constants.FadeStickConsts import FS_VENDOR_ID, FS_PRODUCT_ID
from exceptions.FadeStickException import FadeStickException

if sys.platform == "win32":
    raise FadeStickException("Windows is not supported")

def main():
    print(f'Found FadeStick:')
    print(usb.core.find(find_all=False,
                        idVendor=FS_VENDOR_ID,
                        idProduct=FS_PRODUCT_ID))

if __name__ == "__main__":
    main()
