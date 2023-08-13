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

    l0: Length
    l1: Length

    def __init__(self, l0: Length, l1: Length):
        self.l0 = l0
        self.l1 = l1

    def solve(self, x: float, y: float) -> Tuple[Angle, Angle]:
        theta1 = self._solve_theta1(x, y)
        theta0 = self._solve_theta0(x, y, theta1)
        return theta0, theta1

    def _solve_theta1(self, x: float, y: float) -> Angle:
        numerator = x ** 2 + y ** 2 - self.l0 ** 2 - self.l1 ** 2
        denominator = 2 * self.l0 * self.l1

        try:
            return -math.acos(numerator / denominator)
        except ValueError:
            raise NoSolution(f'No solution for x={x}, y={y} with link lengths l0={self.l0}, l1={self.l1}.')

    def _solve_theta0(self, x: float, y: float, theta1: Angle) -> Angle:
        k1 = self.l0 + self.l1 * math.cos(theta1)
        k2 = self.l1 * math.sin(theta1)
        return math.atan2(y, x) - math.atan2(k2, k1)


class InverseSolver3Dof:
    l0: Length

    _solver_2dof: InverseSolver2Dof

    def __init__(self, l0: Length, l1: Length, l2: Length):
        self.l0 = l0
        self._solver_2dof = InverseSolver2Dof(l1, l2)

    @property
    def l1(self) -> Length:
        return self._solver_2dof.l0

    @l1.setter
    def l1(self, l1: Length) -> None:
        self._solver_2dof.l0 = l1

    @property
    def l2(self) -> Length:
        return self._solver_2dof.l1

    @l2.setter
    def l2(self, l2: Length) -> None:
        self._solver_2dof.l1 = l2

    def solve(self, x: float, y: float, z: float) -> Tuple[Angle, Angle, Angle]:
        theta0 = self._solve_theta0(x, y)
        try:
            theta1, theta2 = self._solve_theta1_2(x, y, z)
        except NoSolution:
            raise NoSolution(
                f'No solution for x={x}, y={y}, z={z} with '
                f'link lengths l0={self.l0}, l1={self.l1}, l2={self.l2}.'
            )

        return theta0, theta1, theta2

    def _solve_theta0(self, x: float, y: float) -> Angle:
        return math.atan2(y, x)

    def _solve_theta1_2(self, x: float, y: float, z: float) -> Tuple[Angle, Angle]:
        x_proj = math.sqrt(x ** 2 + y ** 2) - self.l0
        y_proj = z

        return self._solver_2dof.solve(x_proj, y_proj)


class NoSolution(Exception):
    pass
