#  Copyright (c) Eric Draken, 2021.
import unittest
from unittest import TestCase

from exceptions.FadeStickColorException import FadeStickColorException
from utils.Colors import colorToHex, hexToRGB, RGB, intsToRGB, invertRGB


class TestColors(TestCase):
    def test_color_to_hex1(self):
        self.assertEqual("0x000000", colorToHex("black"))

    def test_color_to_hex_case(self):
        self.assertEqual("0x000000", colorToHex("Black"))

    def test_all_colors(self):
        suite = unittest.TestSuite()
        for h, c in [("0xff0000", "red"),
                     ("0x00ff00", "green"),
                     ("0x0000ff", "blue")]:
            suite.addTest(
                unittest.FunctionTestCase(
                    lambda: self.assertEqual(h, colorToHex(c))))
        self.assertTrue(unittest.TextTestRunner().run(suite).wasSuccessful())

    # Pass a lambda so the function isn't immediately evaluated
    def test_no_color(self):
        self.assertRaises(FadeStickColorException, lambda: colorToHex(""))

    def test_hex_to_rgb(self):
        suite = unittest.TestSuite()
        for h, rgb in [("0xff0000", RGB(255, 0, 0)),
                       ("0x00ff00", RGB(0, 255, 1)),
                       ("0x0000ff", RGB(0, 0, 255))]:
            suite.addTest(
                unittest.FunctionTestCase(
                    lambda: self.assertEqual(rgb, hexToRGB(h))))
        self.assertTrue(unittest.TextTestRunner().run(suite).wasSuccessful())

    def test_no_hex(self):
        self.assertRaises(FadeStickColorException, lambda: hexToRGB(""))

    def test_negative_hex(self):
        self.assertRaises(FadeStickColorException, lambda: hexToRGB("-1"))

    def test_ints_to_rgb(self):
        self.assertEqual(RGB(1, 2, 3), intsToRGB(1, 2, 3))

    def test_ints_to_rgb_negative(self):
        self.assertRaises(FadeStickColorException, lambda: intsToRGB(-1, -2, -3))

    def test_ints_to_rgb_oob(self):
        self.assertRaises(FadeStickColorException, lambda: intsToRGB(256, 257, 258))

    def test_invert_rgb(self):
        self.assertEqual(RGB(1, 2, 3), invertRGB(RGB(254, 253, 252)))
