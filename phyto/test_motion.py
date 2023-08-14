import unittest
from unittest import TestCase

from phyto.motion import PositionSmoother
from phyto.types import Point3D


class PositionSmootherTest(TestCase):
    def setUp(self) -> None:
        self.smoother = PositionSmoother(
            position=Point3D(0, 0, 0),
            speed=0.5,
            time_func=FakeTimeFunc(0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.),
        )

    def test_position(self):
        self.smoother.target = Point3D(1.5, 0, 0)

        self.assertEqual(Point3D(0.5, 0., 0.), self.smoother.position)
        self.assertEqual(Point3D(1.0, 0., 0.), self.smoother.position)
        self.assertEqual(Point3D(1.5, 0., 0.), self.smoother.position)
        self.assertEqual(Point3D(1.5, 0., 0.), self.smoother.position)

    def test_moving_target(self):
        self.smoother.target = Point3D(1.5, 0, 0)

        self.assertEqual(Point3D(0.5, 0.0, 0.0), self.smoother.position)
        self.assertEqual(Point3D(1.0, 0.0, 0.0), self.smoother.position)

        self.smoother.target = Point3D(1, 1.5, 0)

        self.assertEqual(Point3D(1.0, 0.5, 0.0), self.smoother.position)
        self.assertEqual(Point3D(1.0, 1.0, 0.0), self.smoother.position)

        self.smoother.target = Point3D(1, 1, 1.5)

        self.assertEqual(Point3D(1.0, 1.0, 0.5), self.smoother.position)
        self.assertEqual(Point3D(1.0, 1.0, 1.0), self.smoother.position)

    def test_changing_position(self):
        self.smoother.target = Point3D(1.5, 0, 0)

        self.assertEqual(Point3D(0.5, 0.0, 0.0), self.smoother.position)
        self.assertEqual(Point3D(1.0, 0.0, 0.0), self.smoother.position)

        self.smoother.position = Point3D(1.5, 1, 0)

        self.assertEqual(Point3D(1.5, 0.5, 0.0), self.smoother.position)
        self.assertEqual(Point3D(1.5, 0.0, 0.0), self.smoother.position)
        self.assertEqual(Point3D(1.5, 0.0, 0.0), self.smoother.position)

    def test_changing_speed(self):
        self.smoother.target = Point3D(3.0, 0, 0)
        self.smoother.speed = 0.5

        self.assertEqual(Point3D(0.5, 0.0, 0.0), self.smoother.position)
        self.assertEqual(Point3D(1.0, 0.0, 0.0), self.smoother.position)

        self.smoother.speed = 1.0

        self.assertEqual(Point3D(2.0, 0.0, 0.0), self.smoother.position)
        self.assertEqual(Point3D(3.0, 0.0, 0.0), self.smoother.position)
        self.assertEqual(Point3D(3.0, 0.0, 0.0), self.smoother.position)

    def test_infinite_speed(self):
        self.smoother.target = Point3D(1, 0, 0)
        self.smoother.speed = float('inf')

        self.assertEqual(Point3D(1, 0, 0), self.smoother.position)


class FakeTimeFunc:
    def __init__(self, *times: float):
        self.times = list(times)

    def __call__(self) -> float:
        return self.times.pop(0)


if __name__ == '__main__':
    unittest.main()
