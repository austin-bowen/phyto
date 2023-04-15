from dataclasses import dataclass
from typing import Sequence

from phyto.base.leg import Leg, get_legs
from phyto.base.servo_controller import ServoController


def get_base(
        servo_controller: ServoController,
) -> 'Base':
    left_legs, right_legs = get_legs(servo_controller)
    return Base(left_legs, right_legs)


@dataclass
class Base:
    left_legs: Sequence[Leg]
    right_legs: Sequence[Leg]

    def step(self, speed: float, direction: float) -> None:
        # TODO
        print(f'step: speed={speed}, direction={direction}')
        import time; time.sleep(1)
