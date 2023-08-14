import time

try:
    from typing import Callable
except ImportError:
    Callable = ...

from phyto.types import Point3D, TimeFunc


class PositionSmoother:
    speed: float
    time_func: TimeFunc
    tolerance: float

    _position: Point3D
    _target: Point3D
    _t_last_update: float

    def __init__(self, position: Point3D, speed: float, time_func=time.monotonic, tolerance: float = 0.001):
        self.speed = speed
        self.time_func = time_func
        self.tolerance = tolerance

        self.position = position
        self.target = position

    @property
    def position(self) -> Point3D:
        self._update_position()
        return self._position

    def _update_position(self) -> None:
        if self.at_target:
            return

        now = self.time_func()
        dt = now - self._t_last_update
        self._t_last_update = now

        error = (self.target - self._position)
        error_norm = error.norm()
        step = (error / error_norm) * self.speed * dt

        if step.norm() < error_norm:
            self._position += step
        else:
            self._position = self.target

    @position.setter
    def position(self, position: Point3D) -> None:
        self._position = position
        self._t_last_update = self.time_func()

    @property
    def target(self) -> Point3D:
        return self._target

    @target.setter
    def target(self, target: Point3D) -> None:
        self._target = target
        self._t_last_update = self.time_func()

    @property
    def at_target(self) -> bool:
        return self._position.almost_equal(self.target, tolerance=self.tolerance)
