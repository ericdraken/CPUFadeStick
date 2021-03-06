#  Copyright (c) Eric Draken, 2021.
from typing import Final
from unittest import TestCase

from core.pattern.Pattern import ColorDuration, Pattern
from exceptions.NumberExceptions import RangeIntException
from utils.Colors import colorToRGB
from utils.Types import RGB


class TestColorDuration(TestCase):
    def test_create(self):
        cd = ColorDuration(RGB(0, 0, 0), 100)
        self.assertEqual(100, cd.duration)
        self.assertEqual(RGB(0, 0, 0), cd.color)

    def test_large_duration(self):
        with self.assertRaises(RangeIntException):
            ColorDuration(RGB(0, 0, 0), 10000)

    def test_small_duration(self):
        with self.assertRaises(RangeIntException):
            ColorDuration(color=RGB(0, 0, 0), duration=-1)


class TestPattern(TestCase):
    red: Final = colorToRGB("red")
    green: Final = colorToRGB("green")
    blue: Final = colorToRGB("blue")

    def test_immutable(self):
        pattern = Pattern()
        pattern.addColorAndDuration(self.red, 100)

        pattern = Pattern()
        self.assertEqual(0, len(pattern))

    def test_add_color_and_duration(self):
        pattern = Pattern()
        pattern.addColorAndDuration(self.red, 100)
        self.assertEqual((self.red, 100), (pattern.getPattern()[0].color, pattern.getPattern()[0].duration))

    def test_add_color_and_durations(self):
        pattern = Pattern()
        pattern.addColorAndDuration(self.red, 100)
        pattern.addColorAndDuration(self.green, 200)
        self.assertEqual([(self.red, 100), (self.green, 200)],
                         list(map(lambda cd: (cd.color, cd.duration), pattern.getPattern())))

    def test_add_color_and_durations_max(self):
        pattern = Pattern()
        for i in range(0, Pattern.MAX_BUFFER_SIZE):
            pattern.addColorAndDuration(self.red, 100)
        self.assertEqual(Pattern.MAX_BUFFER_SIZE, len(pattern))

    def test_add_color_and_durations_over_max(self):
        pattern = Pattern()
        for i in range(0, Pattern.MAX_BUFFER_SIZE+1):
            pattern.addColorAndDuration(self.red, 100)
        self.assertEqual(Pattern.MAX_BUFFER_SIZE, len(pattern))

    def test_get_pattern_empty(self):
        pattern = Pattern()
        self.assertEqual([], pattern.getPattern())

    def test_get_pattern_many(self):
        pattern = Pattern()
        pattern.addColorAndDuration(self.red, 1)
        p = pattern.getPattern()
        self.assertEqual([(self.red, 1)], list(map(lambda cd: (cd.color, cd.duration), p)))

    def test_get_pattern_immutable(self):
        p1 = Pattern()
        p1.addColorAndDuration(self.red, 1)

        p2 = Pattern()
        self.assertEqual([], p2.getPattern())
        self.assertEqual([(self.red, 1)], list(map(lambda cd: (cd.color, cd.duration), p1.getPattern())))

    def test_get_int_pattern_empty(self):
        p = Pattern()
        self.assertEqual([0] * Pattern.PATTERN_BUFFER_BYTE_LENGTH, p.getIntPattern())

    def test_get_int_pattern(self):
        p = Pattern()
        p.addColorAndDuration(self.red, 100)
        self.assertEqual([1, 255, 0, 0, 10, 0, 0], p.getIntPattern()[:7])

    def test_get_int_pattern2(self):
        p = Pattern()
        p.addColorAndDuration(self.red, 100)
        p.addColorAndDuration(self.green, 100)
        self.assertEqual([2,
                          255, 0, 0, 10,
                          0, 255, 0, 10], p.getIntPattern()[:9])

    def test_get_int_pattern_duration(self):
        p = Pattern()
        p.addColorAndDuration(self.red, 9)
        self.assertEqual([1, 255, 0, 0, 1], p.getIntPattern()[:5])

    def test_get_int_pattern_duration2(self):
        p = Pattern()
        p.addColorAndDuration(self.red, 4)
        self.assertEqual([1, 255, 0, 0, 0], p.getIntPattern()[:5])
