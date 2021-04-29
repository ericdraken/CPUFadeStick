#  Copyright (c) Eric Draken, 2021.

from unittest import TestCase

from exceptions.FadeStickColorException import FadeStickColorException
from exceptions.NumberExceptions import RangeIntException
from utils.Types import RGB, RangeInt


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


class TestRangeInt(TestCase):
    def test_simple(self):
        self.assertEqual(1, RangeInt(1, 0, 255, "test"))

    def test_out_range(self):
        v = -1
        mn = 0
        mx = 255
        with self.assertRaises(RangeIntException) as m:
            RangeInt(v, mn, mx, "test")
        self.assertEqual(f"test is out of range [{mn}..{mx}]: {v}", str(m.exception))

    def test_out_range2(self):
        v = 256
        mn = 0
        mx = 255
        with self.assertRaises(RangeIntException) as m:
            RangeInt(v, mn, mx, "test")
        self.assertEqual(f"test is out of range [{mn}..{mx}]: {v}", str(m.exception))

    def test_range_too_small(self):
        v = 0
        mn = 0
        mx = 0
        with self.assertRaises(RangeIntException) as m:
            RangeInt(v, mn, mx, "test")
        self.assertEqual(f"test has a bad range [{mn}..{mx}]: {v}", str(m.exception))

    def test_range_too_small2(self):
        v = 100
        mn = 10
        mx = -10
        with self.assertRaises(RangeIntException) as m:
            RangeInt(v, mn, mx, "test")
        self.assertEqual(f"test has a bad range [{mn}..{mx}]: {v}", str(m.exception))

    def test_str(self):
        self.assertEqual("1", str(RangeInt(1, 0, 255, "test")))

    def test_repr(self):
        self.assertEqual(f"{'RangeInt'}({'test'}, [{0}..{255}]: {1})"
                         , repr(RangeInt(1, 0, 255, "test")))
