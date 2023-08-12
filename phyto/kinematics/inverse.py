import math

try:
    from typing import Tuple
except ImportError:
    pass

from phyto.types import Angle, Length


class InverseSolver2Dof:
    """
    Solve the inverse kinematics problem for a 2 degree of freedom robot arm.

    Based on: https://www.osrobotics.org/osr/kinematics/inverse_kinematics.html
    """

    def __init__(self, l1: Length, l2: Length):
        self.l1 = l1
        self.l2 = l2

    def solve(self, x: float, y: float) -> Tuple[Angle, Angle]:
        theta2 = self._solve_theta2(x, y)
        theta1 = self._solve_theta1(x, y, theta2)
        return theta1, theta2

    def _solve_theta2(self, x: float, y: float) -> Angle:
        numerator = x ** 2 + y ** 2 - self.l1 ** 2 - self.l2 ** 2
        denominator = 2 * self.l1 * self.l2

        try:
            return -math.acos(numerator / denominator)
        except ValueError:
            raise NoSolution(f'No solution for x={x}, y={y} with link lengths l1={self.l1}, l2={self.l2}.')

    def _solve_theta1(self, x: float, y: float, theta2: Angle) -> Angle:
        k1 = self.l1 + self.l2 * math.cos(theta2)
        k2 = self.l2 * math.sin(theta2)
        return math.atan2(y, x) - math.atan2(k2, k1)


class NoSolution(Exception):
    pass
