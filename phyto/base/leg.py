import math
from time import sleep

from adafruit_motor.servo import Servo

from phyto.base.servo_controller import ServoController

try:
    from typing import Tuple, Optional

    ServoAngle = Optional[float]
    LegGroup = Tuple['Leg', 'Leg', 'Leg']
    LegServos = Tuple[Servo, Servo, Servo]
except ImportError:
    Tuple = ...
    Optional = ...

    ServoAngle = ...
    LegGroup = ...
    LegServos = ...

ANGLE_FROM_BASE: float = math.radians(54.2)


def get_legs(
        servo_controller: ServoController,
) -> Tuple[LegGroup, LegGroup]:
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
        angle_from_base=ANGLE_FROM_BASE,
        flip_angles=True,
        # angles=(85, 158, 124)
    )


def get_left_middle_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='left_middle',
        servos=servo_controller.get_servos(28, 27, 26),
        angle_from_base=0.,
        flip_angles=True,
        # angles = (70, 156, 116)
    )


def get_left_back_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='left_back',
        servos=servo_controller.get_servos(31, 30, 29),
        angle_from_base=-ANGLE_FROM_BASE,
        flip_angles=True,
        # angles = (83, 146, 123)
    )


def get_right_front_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='right_front',
        servos=servo_controller.get_servos(6, 7, 11),
        angle_from_base=ANGLE_FROM_BASE,
        # angles = (85, 21, 46)
    )


def get_right_middle_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='right_middle',
        servos=servo_controller.get_servos(3, 4, 5),
        angle_from_base=0.,
        # angles = (90, 15, 47)
    )


def get_right_back_leg(servo_controller: ServoController) -> 'Leg':
    return Leg(
        id='right_back',
        servos=servo_controller.get_servos(0, 1, 2),
        angle_from_base=-ANGLE_FROM_BASE,
        # angles = (74, 20, 55)
    )


class Leg:
    id: str

    servos: LegServos
    """Three servos in order from internal to external joints."""

    angle_from_base: float

    flip_angles: bool

    def __init__(
            self,
            id: str,
            servos: LegServos,
            angle_from_base: float,
            flip_angles: bool = False,
    ) -> None:
        assert len(servos) == 3, len(servos)

        self.id = id
        self.servos = servos
        self.angle_from_base = angle_from_base
        self.flip_angles = flip_angles

    def __repr__(self) -> str:
        return f'Leg(id={repr(self.id)})'

    @property
    def angles(self) -> Tuple[ServoAngle, ...]:
        return tuple(self.get_angle(i) for i, _ in enumerate(self.servos))

    @angles.setter
    def angles(self, angles: Tuple[ServoAngle, ...]) -> None:
        assert len(angles) == 3, len(angles)

        for i, angle in enumerate(angles):
            self.set_angle(i, angle)

    def get_angle(self, servo_index: int) -> ServoAngle:
        servo = self.servos[servo_index]

        angle = servo.angle
        if angle is None:
            return None

        return 180 - angle if self.flip_angles else angle

    def set_angle(self, servo_index: int, angle: ServoAngle) -> None:
        servo = self.servos[servo_index]

        if angle is None:
            servo.angle = None
        else:
            servo.angle = 180 - angle if self.flip_angles else angle

    def rest(self, speed: float) -> None:
        self.angles = (90, 10, 10)
        sleep(0.5)
        self.disable()

    def disable(self) -> None:
        for servo in self.servos:
            servo.angle = None

    def stand(self, speed: float, height: float) -> None:
        self.angles = (90, 90, 90)
        sleep(0.5)
