try:
    from typing import Sequence, Tuple
except ImportError:
    pass

import time

from phyto.base.leg import Leg, get_legs
from phyto.base.servo_controller import ServoController


def get_base(
        servo_controller: ServoController,
) -> 'Base':
    left_legs, right_legs = get_legs(servo_controller)
    return Base(left_legs, right_legs)


class Base:
    left_legs: Tuple[Leg, Leg, Leg]
    right_legs: Tuple[Leg, Leg, Leg]

    leg_groups: Tuple[Tuple[Leg, Leg, Leg], Tuple[Leg, Leg, Leg]]

    def __init__(self, left_legs: Tuple[Leg, Leg, Leg], right_legs: Tuple[Leg, Leg, Leg]) -> None:
        assert len(left_legs) == 3, len(left_legs)
        assert len(right_legs) == 3, len(right_legs)

        self.left_legs = left_legs
        self.right_legs = right_legs

        self.leg_groups = (
            (left_legs[0], right_legs[1], left_legs[2]),
            (right_legs[0], left_legs[1], right_legs[2]),
        )

    @property
    def legs(self) -> Sequence[Leg]:
        return self.left_legs + self.right_legs

    def rest(self, speed: float) -> None:
        for leg in self.legs:
            leg.rest(speed)

        # TODO
        print(f'rest: speed={speed}')
        time.sleep(1)

    def disable(self) -> None:
        for leg in self.legs:
            leg.disable()

    def stand(self, speed: float, height: float) -> None:
        for leg in self.legs:
            leg.stand(speed, height)

    def step(self, speed: float, direction: float) -> None:
        # TODO
        print(f'step: speed={speed}, direction={direction}')
        time.sleep(1)
