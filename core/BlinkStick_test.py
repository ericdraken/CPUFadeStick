#  Copyright (c) Eric Draken, 2021.
import logging
from unittest import TestCase

from core.BlinkStick import BlinkStick
from core.FadeStickUSB import findFirstFadeStick
from exceptions.NumberExceptions import RangeIntException
from utils.Colors import colorToRGB


class TestBlinkStick(TestCase):
    device: BlinkStick

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logging.basicConfig(level=logging.INFO)
        cls.log = logging.getLogger(cls.__name__)
        cls.device = BlinkStick(findFirstFadeStick())

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

    def test_blink(self):
        self.device.blink(colorToRGB("red"), 1, 50)
        curr_rgb = self.device.getColor()
        self.assertEqual(colorToRGB("off"), curr_rgb)

    def test_blink_twice(self):
        self.device.blink(colorToRGB("blue"), 2, 50)
        curr_rgb = self.device.getColor()
        self.assertEqual(colorToRGB("off"), curr_rgb)

    def test_morph_black_red(self):
        self.device.setColor("black")
        self.device.morph(colorToRGB("red"), 1000)
        curr_rgb = self.device.getColor()
        self.assertEqual(colorToRGB("red"), curr_rgb)

    def test_morph_blue_red(self):
        self.device.setColor("blue")
        self.device.morph(colorToRGB("red"), 1000)
        curr_rgb = self.device.getColor()
        self.assertEqual(colorToRGB("red"), curr_rgb)

    def test_morph_police(self):
        self.device.setColor("black")
        self.device.morph(colorToRGB("red"), 200)
        self.device.morph(colorToRGB("blue"), 200)
        self.device.morph(colorToRGB("red"), 200)
        self.device.morph(colorToRGB("blue"), 200)
        self.device.morph(colorToRGB("off"), 200)
        curr_rgb = self.device.getColor()
        self.assertEqual(colorToRGB("off"), curr_rgb)

    def test_pulse(self):
        self.device.turnOff()
        self.device.pulse(colorToRGB("red"))
        curr_rgb = self.device.getColor()
        self.assertEqual(colorToRGB("off"), curr_rgb)

    def test_pulse_two(self):
        self.device.turnOff()
        self.device.pulse(colorToRGB("green"), 2, 500)
        curr_rgb = self.device.getColor()
        self.assertEqual(colorToRGB("off"), curr_rgb)

    def test_pulse_bad1(self):
        with self.assertRaises(RangeIntException):
            self.device.pulse(colorToRGB("green"), -2)

    def test_pulse_bad2(self):
        with self.assertRaises(RangeIntException):
            self.device.pulse(colorToRGB("green"), 1, -1)

    def test_pulse_bad3(self):
        with self.assertRaises(RangeIntException):
            self.device.pulse(colorToRGB("green"), 1, 1, -1)

    def test_morph_bad(self):
        with self.assertRaises(RangeIntException):
            self.device.morph(colorToRGB("green"), -1, -2)

    def test_blink_bad(self):
        with self.assertRaises(RangeIntException):
            self.device.blink(colorToRGB("green"), 0, -2)
