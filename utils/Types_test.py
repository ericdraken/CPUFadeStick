#  Copyright (c) Eric Draken, 2021.

from unittest import TestCase

from exceptions.FadeStickColorException import FadeStickColorException
from utils.Types import RGB


class TestRGB(TestCase):
    def test_normal(self):
        self.assertEqual((1, 2, 3), RGB(1, 2, 3))

    def test_min(self):
        self.assertEqual((0, 0, 0), RGB(0, 0, 0))

    def test_max(self):
        self.assertEqual((255, 255, 255), RGB(255, 255, 255))

    def test_negative_r(self):
        with self.assertRaises(FadeStickColorException):
            RGB(-1, 0, 0)

    def test_negative_g(self):
        with self.assertRaises(FadeStickColorException):
            RGB(0, -1, 0)

    def test_negative_b(self):
        with self.assertRaises(FadeStickColorException):
            RGB(0, 0, -1)

    def test_large_r(self):
        with self.assertRaises(FadeStickColorException):
            RGB(256, 0, 0)

    def test_large_g(self):
        with self.assertRaises(FadeStickColorException):
            RGB(0, 256, 0)

    def test_nlarge_b(self):
        with self.assertRaises(FadeStickColorException):
            RGB(0, 0, 256)
