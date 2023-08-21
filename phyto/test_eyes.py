import unittest
from math import pi
from unittest import TestCase

from parameterized import parameterized

from phyto.eyes import Eye, Eyes


class EyesTest(TestCase):
    def setUp(self) -> None:
        self.eyes = Eyes(FakeEye(0.), FakeEye(0.), FakeEye(0.))

    @parameterized.expand([
        (1., 1., 0., 0.),
        (0., 0., 1., pi),
        (1., 0., 0.5, pi / 2),
        (0., 1., 0.5, -pi / 2),
    ])
    def test_brightness_direction(self, left: float, right: float, back: float, direction: float):
        self.set_eye_values(left, right, back)
        self.assertAlmostEqual(direction, self.eyes.brightest_direction())

    @parameterized.expand([
        (0., 0., 0., 0 / 3),
        (1., 0., 0., 1 / 3),
        (0., 1., 1., 2 / 3),
        (1., 1., 1., 3 / 3),
    ])
    def test_light_level(self, left: float, right: float, back: float, level: float):
        self.set_eye_values(left, right, back)
        self.assertAlmostEqual(level, self.eyes.light_level())

    def set_eye_values(self, left: float, right: float, back: float) -> None:
        self.eyes.left_eye.value = left
        self.eyes.right_eye.value = right
        self.eyes.back_eye.value = back


class FakeEye(Eye):
    def __init__(self, value: float):
        self.value = value

    def read(self) -> float:
        return self.value


if __name__ == '__main__':
    unittest.main()
