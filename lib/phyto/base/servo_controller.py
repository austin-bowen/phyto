from abc import abstractmethod
from typing import Sequence

from adafruit_motor.servo import Servo
from adafruit_pca9685 import PCA9685
from busio import I2C

from phyto.types import I2cAddress

Channel = int


def get_servo_controller(
        i2c_bus: I2C,
        pca9685_0_i2c_address: I2cAddress,
        pca9685_1_i2c_address: I2cAddress,
        pwm_freq: int,
) -> 'ServoController':
    servo_controller_0 = PCA9685ServoController(i2c_bus, address=pca9685_0_i2c_address)
    servo_controller_0.frequency = pwm_freq

    servo_controller_1 = PCA9685ServoController(i2c_bus, address=pca9685_1_i2c_address)
    servo_controller_1.frequency = pwm_freq

    return DualServoController(servo_controller_0, servo_controller_1)


class ServoController:
    @abstractmethod
    def get_servo(self, channel: Channel) -> Servo:
        ...

    def get_servos(self, *channels: int) -> Sequence[Servo]:
        return tuple(self.get_servo(channel) for channel in channels)


class PCA9685ServoController(PCA9685, ServoController):
    def get_servo(self, channel: Channel) -> Servo:
        return Servo(self.channels[channel])


class DualServoController(ServoController):
    """Operates like a single, 32-channel servo controller."""

    servo_controller_0: ServoController
    servo_controller_1: ServoController

    def __init__(self, servo_controller_0: ServoController, servo_controller_1: ServoController):
        self.servo_controller_0 = servo_controller_0
        self.servo_controller_1 = servo_controller_1

    def get_servo(self, channel: Channel) -> Servo:
        if 0 <= channel < 16:
            return self.servo_controller_0.get_servo(channel)
        elif 16 <= channel < 32:
            return self.servo_controller_1.get_servo(channel - 16)
        else:
            raise ValueError(f'Invalid channel: {channel}')
