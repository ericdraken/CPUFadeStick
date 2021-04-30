#  Copyright (c) Eric Draken, 2021.
import logging
from unittest import TestCase

from core.FadeStick import FadeStick
from core.FadeStickUSB import findFirstFadeStick
from utils.Colors import RED
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

    @disabled
    def test_morph(self):
        self.fail()

    @disabled
    def test_pulse(self):
        self.fail()
