import math

from phyto import config
from phyto.base.leg import get_right_front_leg, get_right_middle_leg, get_right_back_leg
from phyto.base.servo_controller import get_servo_controller, ServoController
from phyto.i2c import get_i2c_bus
from phyto.kinematics.inverse import InverseSolver3Dof, NoSolution
from phyto.types import Pin, I2cAddress


def leg_test(
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
    # leg = get_right_front_leg(servo_controller)
    leg = get_right_middle_leg(servo_controller)
    # leg = get_right_back_leg(servo_controller)

    solver = InverseSolver3Dof(l0=.032, l1=.090, l2=.112)

    while True:
        try:
            command = input('x,y,z: ')
            x, y, z = map(float, command.split(','))

            theta0, theta1, theta2 = solver.solve(x, y, z)

            theta0 = math.degrees(theta0)
            theta1 = math.degrees(theta1)
            theta2 = math.degrees(theta2)

            print(f'Raw   : theta0={theta0}, theta1={theta1}, theta2={theta2}')

            theta0 = 90 - theta0
            theta1 = 90 - theta1
            theta2 = 180 + theta2

            print(f'Offset: theta0={theta0}, theta1={theta1}, theta2={theta2}')

            leg.angles = (theta0, theta1, theta2)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f'ERROR: {e}')
