#  Copyright (c) Eric Draken, 2021.
import unittest
from typing import List
from unittest import TestCase

from constants.FadeStickConsts import FS_MANUFACTURER, FS_USB_STRING, FS_SERIAL_INDEX
from core.FadeStickBase import FadeStickBase
from core.FadeStickUSB import USBDevice, findAllFadeSticks, _findFadeSticksAsGenerator, \
    findFadeStickBySerial, findFirstFadeStick, getUSBString, getManufacturer, \
    getDescription


class TestFadeStickUSB(TestCase):
    def test_find_all_fade_sticks(self):
        devices: List[FadeStickBase] = findAllFadeSticks()
        self.assertTrue(devices, "Non-empty list of FadeSticks")
        self.assertEqual(FS_MANUFACTURER, devices[0].device.manufacturer)

    def test_find_first_fade_stick(self):
        device: FadeStickBase = findFirstFadeStick()
        self.assertEqual(FS_MANUFACTURER, device.device.manufacturer)

    def test_find_fade_stick_by_serial(self):
        device: USBDevice = next(_findFadeSticksAsGenerator())
        found = findFadeStickBySerial(device.serial_number)
        self.assertEqual(str(found.device), str(device))

    def test_find_fade_sticks_as_generator(self):
        device: USBDevice = next(_findFadeSticksAsGenerator())
        self.assertEqual(FS_MANUFACTURER, device.manufacturer)

    def test_get_usbstring_device(self):
        device: FadeStickBase = findFirstFadeStick()
        string = getUSBString(device.device, FS_SERIAL_INDEX)  # Pass Device
        self.assertEqual(FS_USB_STRING, string)

    def test_get_usbstring_fadestick(self):
        device: FadeStickBase = findFirstFadeStick()
        string = getUSBString(device, FS_SERIAL_INDEX)  # Pass FadeStick
        self.assertEqual(FS_USB_STRING, string)

    def test_get_manufacturer(self):
        device: FadeStickBase = findFirstFadeStick()
        self.assertEqual(FS_MANUFACTURER, getManufacturer(device))

    def test_get_description(self):
        device: FadeStickBase = findFirstFadeStick()
        self.assertGreater(len(getDescription(device)), 5)


if __name__ == '__main__':
    unittest.main()
