import math

from adafruit_motor.servo import Servo

from phyto.base.servo_controller import ServoController
from phyto.kinematics.inverse import InverseSolver3Dof
from phyto.motion import PositionSmoother
from phyto.types import Point3D

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

REST_POSITION = Point3D(0.1, 0, -0.01)


def get_legs(
        servo_controller: ServoController,
) -> Tuple[LegGroup, LegGroup]:
    solver = InverseSolver3Dof(l0=.032, l1=.090, l2=.112)

    left_legs = (
        get_left_front_leg(servo_controller, solver),
        get_left_middle_leg(servo_controller, solver),
        get_left_back_leg(servo_controller, solver),
    )

    right_legs = (
        get_right_front_leg(servo_controller, solver),
        get_right_middle_leg(servo_controller, solver),
        get_right_back_leg(servo_controller, solver),
    )

    return left_legs, right_legs


def get_left_front_leg(servo_controller: ServoController, solver: InverseSolver3Dof) -> 'Leg':
    return Leg(
        id='left_front',
        servos=servo_controller.get_servos(25, 24, 15),
        solver=solver,
        angle_from_base=ANGLE_FROM_BASE,
        # Calibration paper: angles=(85, 158, 124)
        # (center, 90, 90): angles=(85, 88, 87)
        angle_offsets=(90 + 5, 90 + 2, 180 + 3),
        flip_angles=True,
    )


def get_left_middle_leg(servo_controller: ServoController, solver: InverseSolver3Dof) -> 'Leg':
    return Leg(
        id='left_middle',
        servos=servo_controller.get_servos(28, 27, 26),
        solver=solver,
        angle_from_base=0.,
        # Calibration paper: angles = (70, 156, 116)
        # (center, 90, 90): angles = (70, 83, 78)
        angle_offsets=(90 + 20, 90 + 7, 180 + 12),
        flip_angles=True,
    )


def get_left_back_leg(servo_controller: ServoController, solver: InverseSolver3Dof) -> 'Leg':
    return Leg(
        id='left_back',
        servos=servo_controller.get_servos(31, 30, 29),
        solver=solver,
        angle_from_base=-ANGLE_FROM_BASE,
        # Calibration paper: angles = (83, 146, 123)
        # (center, 90, 90): angles = (83, 79, 88)
        angle_offsets=(90 + 7, 90 + 11, 180 + 2),
        flip_angles=True,
    )


def get_right_front_leg(servo_controller: ServoController, solver: InverseSolver3Dof) -> 'Leg':
    return Leg(
        id='right_front',
        servos=servo_controller.get_servos(6, 7, 11),
        solver=solver,
        angle_from_base=ANGLE_FROM_BASE,
        # Calibration paper: angles = (85, 21, 46)
        # (center, 90, 90): angles = (85, 89, 80)
        angle_offsets=(90 - 5, 90 - 1, 180 - 10),
    )


def get_right_middle_leg(servo_controller: ServoController, solver: InverseSolver3Dof) -> 'Leg':
    return Leg(
        id='right_middle',
        servos=servo_controller.get_servos(3, 4, 5),
        solver=solver,
        angle_from_base=0.,
        # Calibration paper: angles = (90, 15, 47)
        # (center, 90, 90): angles = (90, 89, 83)
        angle_offsets=(90 - 0, 90 - 1, 180 - 7),
    )


def get_right_back_leg(servo_controller: ServoController, solver: InverseSolver3Dof) -> 'Leg':
    return Leg(
        id='right_back',
        servos=servo_controller.get_servos(0, 1, 2),
        solver=solver,
        angle_from_base=-ANGLE_FROM_BASE,
        # Calibration paper: angles = (74, 20, 55)
        # (center, 90, 90): angles = (74, 90, 91)
        angle_offsets=(90 - 16, 90 - 0, 180 + 1),
    )


class Leg:
    id: str

    servos: LegServos
    """Three servos in order from internal to external joints."""

    solver: InverseSolver3Dof

    angle_from_base: float

    angle_offsets: Tuple[float, float, float]

    flip_angles: bool

    smoother: PositionSmoother

    def __init__(
            self,
            id: str,
            servos: LegServos,
            solver: InverseSolver3Dof,
            angle_from_base: float,
            angle_offsets: Tuple[float, float, float] = (90, 90, 180),
            flip_angles: bool = False,
            smoother: PositionSmoother = None
    ) -> None:
        assert len(servos) == 3, len(servos)

        self.id = id
        self.servos = servos
        self.solver = solver
        self.angle_from_base = angle_from_base
        self.angle_offsets = angle_offsets
        self.flip_angles = flip_angles
        self.smoother = smoother or PositionSmoother(REST_POSITION, 0.05)

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

    @property
    def position(self) -> Point3D:
        return self.smoother.position

    @property
    def at_target(self) -> bool:
        return self.smoother.at_target

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

    def set_target(self, target: Point3D, speed: float) -> None:
        self.smoother.set_target(target, speed=speed)

    def disable(self) -> None:
        for servo in self.servos:
            servo.angle = None

    def move(self) -> None:
        """Moves the leg one bit closer to the target, following the position smoother."""

        if self.at_target:
            return

        position = self.smoother.position

        theta0, theta1, theta2 = self.solver.solve(position.x, position.y, position.z)

        theta0 = self.angle_offsets[0] - math.degrees(theta0)
        theta1 = self.angle_offsets[1] - math.degrees(theta1)
        theta2 = self.angle_offsets[2] + math.degrees(theta2)

        self.angles = (theta0, theta1, theta2)
