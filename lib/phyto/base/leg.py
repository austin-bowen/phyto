from typing import Sequence, Tuple, Optional

from adafruit_motor.servo import Servo

from phyto.base.servo_controller import ServoController

ServoAngle = Optional[float]


def get_legs(
        servo_controller: ServoController,
) -> Tuple[Sequence['Leg'], Sequence['Leg']]:
    left_legs = (
        get_left_front_leg(servo_controller),
        get_left_middle_leg(servo_controller),
        get_left_back_leg(servo_controller),
    )

    right_legs = (
        get_right_front_leg(servo_controller),
        get_right_middle_leg(servo_controller),
        get_right_back_leg(servo_controller),
    )

    return left_legs, right_legs


def get_left_front_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='left_front',
        servos=servo_controller.get_servos(22, 23, 27),
    )


def get_left_middle_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='left_middle',
        servos=servo_controller.get_servos(19, 20, 21),
    )


def get_left_back_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='left_back',
        servos=servo_controller.get_servos(16, 17, 18),
    )


def get_right_front_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='right_front',
        servos=servo_controller.get_servos(9, 8, 31),
    )


def get_right_middle_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='right_middle',
        servos=servo_controller.get_servos(12, 11, 10),
    )


def get_right_back_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='right_back',
        servos=servo_controller.get_servos(15, 14, 13),
    )


class Leg:
    id: str

    servos: Sequence[Servo]
    """Three servos in order from internal to external joints."""

    def __init__(self, id: str, servos: Sequence[Servo]) -> None:
        assert len(servos) == 3, len(servos)

        self.id = id
        self.servos = servos

    def __repr__(self) -> str:
        return f'Leg(id={self.id!r})'

    @property
    def angles(self) -> Tuple[ServoAngle, ...]:
        return tuple(servo.angle for servo in self.servos)

    @angles.setter
    def angles(self, angles: Tuple[ServoAngle, ...]) -> None:
        assert len(angles) == 3, len(angles)

        for servo, angle in zip(self.servos, angles):
            servo.angle = angle

    def rest(self, speed: float) -> None:
        # TODO Go to rest position

        for servo in self.servos:
            servo.angle = None

    def stand(self, speed: float, height: float) -> None:
        # TODO
        ...
