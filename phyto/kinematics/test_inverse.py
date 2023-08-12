import unittest
from math import pi
from unittest import TestCase

from parameterized import parameterized

from phyto.kinematics.inverse import InverseSolver2Dof, NoSolution


class InverseSolver2DofTest(TestCase):
    def setUp(self):
        self.solver = InverseSolver2Dof(2, 1)

    @parameterized.expand([
        (3, 0, 0, 0),
        (-3, 0, pi, 0),
        (0, 3, pi / 2, 0),
        (0, -3, -pi / 2, 0),
        (2, -1, 0, -pi / 2),
        (2, 0, .5053605, -1.8234766),
        (1.5, -1.5, -0.2987032, -1.6961242),
    ])
    def test_solve(self, x: float, y: float, theta1: float, theta2: float):
        actual_theta1, actual_theta2 = self.solver.solve(x, y)
        self.assertAlmostEqual(theta1, actual_theta1)
        self.assertAlmostEqual(theta2, actual_theta2)

    @parameterized.expand([
        (3.001, 0),
        (0, 0.999),
    ])
    def test_no_solution(self, x: float, y: float):
        self.assertRaises(NoSolution, self.solver.solve, x, y)


if __name__ == '__main__':
    unittest.main()
