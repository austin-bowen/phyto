import math
from math import cos, sin

from phyto import config
from phyto.base import get_base
from phyto.base.servo_controller import get_servo_controller, ServoController
from phyto.i2c import get_i2c_bus
from phyto.kinematics.inverse import InverseSolver3Dof
from phyto.motion import PositionSmoother
from phyto.types import Pin, I2cAddress, Point3D


def base_test(
        i2c_bus_scl: Pin = config.I2C_BUS_SCL,
        i2c_bus_sda: Pin = config.I2C_BUS_SDA,
        i2c_bus_freq: int = config.I2C_BUS_FREQ,
        pca9685_0_i2c_address: I2cAddress = config.PCA9685_0_I2C_ADDRESS,
        pca9685_1_i2c_address: I2cAddress = config.PCA9685_1_I2C_ADDRESS,
        pca9685_pwm_freq: int = config.PCA9685_PWM_FREQ,
) -> None:
    i2c_bus = get_i2c_bus(i2c_bus_scl, i2c_bus_sda, i2c_bus_freq)

    servo_controller = get_servo_controller(
        i2c_bus,
        pca9685_0_i2c_address,
        pca9685_1_i2c_address,
        pca9685_pwm_freq,
    )

    with i2c_bus, servo_controller:
        run(servo_controller)


def run(servo_controller: ServoController) -> None:
    base = get_base(servo_controller)

    left_leg_group, right_leg_group = base.leg_groups
    all_legs = left_leg_group + right_leg_group

    speed = 0.2

    left_smoothers = [
        PositionSmoother(
            position=Point3D(0.1, 0, 0),
            speed=speed,
        ) for _ in range(3)
    ]

    right_smoothers = [
        PositionSmoother(
            position=Point3D(0.1, 0, 0),
            speed=speed,
        ) for _ in range(3)
    ]

    all_smoothers = left_smoothers + right_smoothers

    x = 0.08
    dy = 0.02
    low, high = -0.06, -0.03

    left_targets = [
        Point3D(x, dy, low),
        Point3D(x, 0.0, low),
        Point3D(x, -dy, low),
        Point3D(x, 0.0, high),
    ]

    right_targets = [
        Point3D(x, -dy, low),
        Point3D(x, 0.0, high),
        Point3D(x, dy, low),
        Point3D(x, 0.0, low),
    ]

    solver = InverseSolver3Dof(l0=.032, l1=.090, l2=.112)

    while True:
        try:
            steps = int(input('steps: '))

            for step in range(steps):
                for left_target, right_target in zip(left_targets, right_targets):
                    # Set smoother targets
                    for legs, smoothers, target in [
                        (left_leg_group, left_smoothers, left_target),
                        (right_leg_group, right_smoothers, right_target),
                    ]:
                        for leg, smoother in zip(legs, smoothers):
                            theta = -leg.angle_from_base
                            leg_target = rotate_point(target, theta)
                            smoother.target = leg_target

                    # Update positions
                    while not all(smoother.at_target for smoother in all_smoothers):
                        for leg, smoother in zip(all_legs, all_smoothers):
                            if smoother.at_target:
                                continue

                            position = smoother.position

                            theta0, theta1, theta2 = solver.solve(position.x, position.y, position.z)

                            theta0 = 90 - math.degrees(theta0)
                            theta1 = 90 - math.degrees(theta1)
                            theta2 = 180 + math.degrees(theta2)

                            leg.angles = (theta0, theta1, theta2)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f'ERROR: {e}')


def rotate_point(point: Point3D, angle: float) -> Point3D:
    return Point3D(
        point.x * cos(angle) - point.y * sin(angle),
        point.x * sin(angle) + point.y * cos(angle),
        point.z
    )
