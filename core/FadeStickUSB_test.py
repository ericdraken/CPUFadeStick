#  Copyright (c) Eric Draken, 2021.

import unittest
from typing import List
from unittest import TestCase

from usb.core import Device

from constants.FadeStickConsts import FS_MANUFACTURER, FS_USB_STRING
from core.FadeStick import FadeStick
from core.FadeStickUSB import findAllFadeSticks, _findFadeSticksAsGenerator, findFadeStickBySerial, findFirstFadeStick, \
    getUSBString


class TestFadeStickUSB(TestCase):
    def test__find_all_fade_sticks(self):
        devices: List[FadeStick] = findAllFadeSticks()
        self.assertTrue(devices, "Non-empty list of FadeSticks")
        self.assertEqual(devices[0].device.manufacturer, FS_MANUFACTURER)

    def test_find_first_fade_stick(self):
        device: FadeStick = findFirstFadeStick()
        self.assertEqual(device.device.manufacturer, FS_MANUFACTURER)

    def test__find_fade_stick_by_serial(self):
        device: Device = next(_findFadeSticksAsGenerator())
        found = findFadeStickBySerial(device.serial_number)
        self.assertEqual(str(found.device), str(device))

    def test__find_fade_sticks_as_generator(self):
        device: Device = next(_findFadeSticksAsGenerator())
        self.assertEqual(device.manufacturer, FS_MANUFACTURER)

    def test__get_usbstring_device(self):
        device: FadeStick = findFirstFadeStick()
        string = getUSBString(device.device)  # Pass Device
        self.assertEquals(string, FS_USB_STRING)

    def test__get_usbstring_fadestick(self):
        device: FadeStick = findFirstFadeStick()
        string = getUSBString(device)  # Pass FadeStick
        self.assertEquals(string, FS_USB_STRING)

if __name__ == '__main__':
    unittest.main()
