#  Copyright (c) Eric Draken, 2021.
import time
import unittest
from unittest import TestCase

from core.FadeStickUSB import findFirstFadeStick
from core.FadeStick import FadeStick
from utils.Types import RGB


class TestFadeStick(TestCase):
    device: FadeStick

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.device = findFirstFadeStick()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        if cls.device:
            cls.device.turnOff()

    def setUp(self) -> None:
        super().setUp()
        if self.device:
            self.device.turnOff()

    def tearDown(self) -> None:
        super().tearDown()
        if self.device:
            self.device.turnOff()

    def test_set_color_hex(self):
        rgb = self.device.setColor("0xff0000")
        self.assertEqual(RGB(255, 0, 0), rgb)

    def test_set_color_name(self):
        rgb = self.device.setColor("red")
        self.assertEqual(RGB(255, 0, 0), rgb)

    def test_get_color_black(self):
        rgb = self.device.setColor(0, 0, 0)
        self.assertEqual(RGB(0, 0, 0), rgb)
        curr_rgb = self.device.getColor()
        self.assertEqual(RGB(0, 0, 0), curr_rgb)

    def test_get_color_white(self):
        rgb = self.device.setColor(255, 255, 255)
        self.assertEqual(RGB(255, 255, 255), rgb)
        curr_rgb = self.device.getColor()
        self.assertEqual(RGB(255, 255, 255), curr_rgb)

    def test_get_color_mixed(self):
        rgb = self.device.setColor(10, 20, 30)
        self.assertEqual(RGB(10, 20, 30), rgb)
        curr_rgb = self.device.getColor()
        self.assertEqual(RGB(10, 20, 30), curr_rgb)

    def test_try_all_colors(self):
        from utils.Colors import COLOR_DICT
        suite = unittest.TestSuite()
        for k, v in COLOR_DICT.items():
            suite.addTest(
                unittest.FunctionTestCase(
                    # Using 'None if' because lambdas are () -> None
                    # Bind color to local variable k
                    lambda color=k: None if (
                        print(color),
                        setRGB := self.device.setColor(color),
                        getRGB := self.device.getColor(),
                        self.assertEqual(setRGB, getRGB),
                        time.sleep(0.2)  # Pleasing delay to see the colors
                    ) else None)
            )
        self.assertTrue(unittest.TextTestRunner().run(suite).wasSuccessful())
