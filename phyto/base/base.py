import time
from typing import Sequence

from phyto.base.leg import Leg, get_legs
from phyto.base.servo_controller import ServoController


def get_base(
        servo_controller: ServoController,
) -> 'Base':
    left_legs, right_legs = get_legs(servo_controller)
    return Base(left_legs, right_legs)


class Base:
    left_legs: Sequence[Leg]
    right_legs: Sequence[Leg]

    leg_groups: Sequence[Sequence[Leg]]

    def __init__(self, left_legs: Sequence[Leg], right_legs: Sequence[Leg]) -> None:
        self.left_legs = left_legs
        self.right_legs = right_legs

        self.leg_groups = [
            (left_legs[0], right_legs[1], left_legs[2]),
            (right_legs[0], left_legs[1], right_legs[2]),
        ]

    @property
    def legs(self) -> Sequence[Leg]:
        return tuple(*self.left_legs, *self.right_legs)

    def rest(self, speed: float) -> None:
        for leg in self.legs:
            leg.rest(speed)

        # TODO
        print(f'rest: speed={speed}')
        time.sleep(1)

    def stand(self, speed: float, height: float) -> None:
        for leg in self.legs:
            leg.stand(speed, height)

        # TODO
        print(f'stand: speed={speed}, height={height}')
        time.sleep(1)

    def step(self, speed: float, direction: float) -> None:
        # TODO
        print(f'step: speed={speed}, direction={direction}')
        time.sleep(1)
