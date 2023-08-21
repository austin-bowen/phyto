from math import pi

from phyto.base.leg import Leg, get_legs, LegGroup, REST_POSITION
from phyto.base.servo_controller import ServoController
from phyto.types import Point3D
from phyto.utils import rotate_point

try:
    from typing import Sequence, Tuple
except ImportError:
    Sequence = ...
    Tuple = ...


def get_base(
        servo_controller: ServoController,
) -> 'Base':
    left_legs, right_legs = get_legs(servo_controller)
    return Base(left_legs, right_legs)


class Base:
    left_legs: LegGroup
    right_legs: LegGroup

    legs: Tuple[Leg, Leg, Leg, Leg, Leg, Leg]

    left_leg_group: LegGroup
    right_leg_group: LegGroup
    leg_groups: Tuple[LegGroup, LegGroup]

    def __init__(self, left_legs: LegGroup, right_legs: LegGroup) -> None:
        assert len(left_legs) == 3, len(left_legs)
        assert len(right_legs) == 3, len(right_legs)

        self.left_legs = left_legs
        self.right_legs = right_legs

        self.legs = left_legs + right_legs

        self.left_leg_group = (left_legs[0], right_legs[1], left_legs[2])
        self.right_leg_group = (right_legs[0], left_legs[1], right_legs[2])
        self.leg_groups = (self.left_leg_group, self.right_leg_group)

    def rest(self, speed: float, rest_target: Point3D = REST_POSITION) -> None:
        for leg in self.legs:
            leg.set_target(rest_target, speed=speed)

        self._wait_for_legs_to_reach_targets()
        self.disable()

    def disable(self) -> None:
        for leg in self.legs:
            leg.disable()

    def stand(self, speed: float, height: float) -> None:
        for leg in self.legs:
            ...

    def walk(self, speed: float, direction: float, steps: int) -> None:
        assert steps >= 0, steps
        for _ in range(steps):
            self.step(speed, direction)

    def step(self, speed: float, direction: float) -> None:
        assert speed > 0, speed
        assert -pi <= direction <= pi, direction

        x = 0.1
        dy = 0.04
        dz = 0.05
        low = -0.08
        high = low + dz
        lean = 0.02 / 2

        leg_center = Point3D(x, 0, 0)

        travel_speed = 1.5 * speed

        left_targets = [
            (Point3D(x, -dy, low), speed),
            (Point3D(x, -dy - lean, low), travel_speed),
            (Point3D(x, -dy, high), travel_speed),
            (Point3D(x, dy + lean, high), travel_speed),
            (Point3D(x, dy, low), travel_speed),
            (Point3D(x, 0, low), speed),
        ]

        right_targets = left_targets[len(left_targets) // 2:] + left_targets[:len(left_targets) // 2]

        for left_target, right_target in zip(left_targets, right_targets):
            self._set_leg_group_targets(left_target, right_target, direction, leg_center)
            self._wait_for_legs_to_reach_targets()

    def _set_leg_group_targets(
            self,
            left_target: Tuple[Point3D, float],
            right_target: Tuple[Point3D, float],
            direction: float,
            leg_center: Point3D,
    ) -> None:
        # Set leg targets
        for legs, target, d in [
            (self.left_leg_group, left_target, -direction),
            (self.right_leg_group, right_target, direction),
        ]:
            target_position, target_speed = target
            for leg, dd in zip(legs, (d, -d, d)):
                theta = -leg.angle_from_base + dd
                leg_target = rotate_point(target_position - leg_center, theta) + leg_center
                leg.set_target(leg_target, speed=target_speed)

    def _wait_for_legs_to_reach_targets(self) -> None:
        legs_not_at_target = self._legs_not_at_target()
        while legs_not_at_target:
            for leg in legs_not_at_target:
                leg.move()

            legs_not_at_target = self._legs_not_at_target()

    def _legs_not_at_target(self) -> Sequence[Leg]:
        return [leg for leg in self.legs if not leg.at_target]
