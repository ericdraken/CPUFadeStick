#  Copyright (c) Eric Draken, 2021.
import logging
import time
from unittest import TestCase

from core.FadeStick import FadeStick
from core.FadeStickUSB import findFirstFadeStick
from core.pattern.Pattern import Pattern
from exceptions.NumberExceptions import RangeIntException
from utils.Colors import RED, GREEN, BLUE
from utils.Decorators import disabled


class TestFadeStick(TestCase):
    device: FadeStick

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        logging.basicConfig(level=logging.INFO)
        cls.log = logging.getLogger(cls.__name__)
        cls.device = FadeStick(findFirstFadeStick())

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
        self.device.blink(RED, 2, 500)

    def test_blink2(self):
        self.device.blink(GREEN, 3, 100)

    def test_blink_many_steps(self):
        with self.assertRaises(RangeIntException):
            self.device.blink(BLUE, Pattern.MAX_BUFFER_SIZE // 2 + 1, 100)

    def test_morph(self):
        duration = 1000
        self.device.setColor(RED)
        self.device.morph(BLUE, duration, 60)
        time.sleep((duration / 1000.0) * 1.5)
        self.assertEqual(BLUE, self.device.getColor())
        self.device.turnOff()

    def test_morph_default_steps(self):
        duration = 1000
        self.device.setColor(RED)
        self.device.morph(GREEN, duration)
        time.sleep((duration / 1000.0) * 1.5)
        self.assertEqual(GREEN, self.device.getColor())
        self.device.turnOff()

    def test_morph_many_steps(self):
        with self.assertRaises(RangeIntException):
            self.device.morph(BLUE, 100, Pattern.MAX_BUFFER_SIZE + 1)

    def test_morph_too_long(self):
        with self.assertRaises(RangeIntException):
            self.device.morph(BLUE, 255 * 10 + 1, 1)

    @disabled
    def test_pulse(self):
        self.fail()
