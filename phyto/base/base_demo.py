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

    speed = 0.15

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

    direction = math.radians(0)

    x = 0.1
    dy = 0.04
    dz = 0.05
    low = -0.16
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

    solver = InverseSolver3Dof(l0=.032, l1=.090, l2=.112)

    while True:
        try:
            steps = int(input('steps: '))

            for step in range(steps):
                for left_target, right_target in zip(left_targets, right_targets):
                    # Set smoother targets
                    for legs, smoothers, target, d in [
                        (left_leg_group, left_smoothers, left_target, -direction),
                        (right_leg_group, right_smoothers, right_target, direction),
                    ]:
                        target_position, target_speed = target
                        for leg, smoother, dd in zip(legs, smoothers, (d, -d, d)):
                            theta = -leg.angle_from_base + dd
                            leg_target = rotate_point(target_position - leg_center, theta) + leg_center
                            smoother.set_target(leg_target, speed=target_speed)

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

                            try:
                                leg.angles = (theta0, theta1, theta2)
                            except ValueError:
                                print(f'ERROR: Invalid angles for {leg.id}: {theta0}, {theta1}, {theta2}')
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f'ERROR: {repr(e)}')


def rotate_point(point: Point3D, angle: float) -> Point3D:
    return Point3D(
        point.x * cos(angle) - point.y * sin(angle),
        point.x * sin(angle) + point.y * cos(angle),
        point.z
    )
