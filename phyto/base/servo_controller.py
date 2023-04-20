try:
    from typing import Sequence, Optional, Type
except ImportError:
    pass

from abc import abstractmethod

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
    @property
    def channel_count(self) -> int:
        return self.get_channel_count()

    @abstractmethod
    def __enter__(self) -> 'ServoController':
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

    @abstractmethod
    def get_channel_count(self) -> int:
        ...

    @abstractmethod
    def get_servo(self, channel: Channel) -> Servo:
        ...

    def get_servos(self, *channels: int) -> Sequence[Servo]:
        return tuple(self.get_servo(channel) for channel in channels)

    def disable(self) -> None:
        """Disables all servos."""
        for channel in range(self.channel_count):
            servo = self.get_servo(channel)
            servo.angle = None


class PCA9685ServoController(PCA9685, ServoController):
    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.disable()
        PCA9685.__exit__(self, exception_type, exception_value, traceback)

    def get_channel_count(self) -> int:
        return 16

    def get_servo(self, channel: Channel) -> Servo:
        return Servo(self.channels[channel])


class DualServoController(ServoController):
    """Operates like a single, 32-channel servo controller."""

    servo_controller_0: ServoController
    servo_controller_1: ServoController

    def __init__(self, servo_controller_0: ServoController, servo_controller_1: ServoController):
        self.servo_controller_0 = servo_controller_0
        self.servo_controller_1 = servo_controller_1

    def __enter__(self) -> 'ServoController':
        self.servo_controller_0.__enter__()
        self.servo_controller_1.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.servo_controller_0.__exit__(exc_type, exc_val, exc_tb)
        self.servo_controller_1.__exit__(exc_type, exc_val, exc_tb)

    def get_channel_count(self) -> int:
        return 32

    def get_servo(self, channel: Channel) -> Servo:
        if 0 <= channel < 16:
            return self.servo_controller_0.get_servo(channel)
        elif 16 <= channel < 32:
            return self.servo_controller_1.get_servo(channel - 16)
        else:
            raise ValueError(f'Invalid channel: {channel}')
