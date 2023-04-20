try:
    from typing import Sequence, Tuple, Optional

    ServoAngle = Optional[float]
except ImportError:
    pass

from adafruit_motor.servo import Servo

from phyto.base.servo_controller import ServoController


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
        servos=servo_controller.get_servos(25, 24, 15),
    )


def get_left_middle_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='left_middle',
        servos=servo_controller.get_servos(28, 27, 26),
    )


def get_left_back_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='left_back',
        servos=servo_controller.get_servos(31, 30, 29),
    )


def get_right_front_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='right_front',
        servos=servo_controller.get_servos(6, 7, 11),
    )


def get_right_middle_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='right_middle',
        servos=servo_controller.get_servos(3, 4, 5),
    )


def get_right_back_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='right_back',
        servos=servo_controller.get_servos(0, 1, 2),
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
        return f'Leg(id={repr(self.id)})'

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
