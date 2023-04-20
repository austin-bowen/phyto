from time import sleep

from busio import I2C

from phyto import config
from phyto.base import get_base
from phyto.base.servo_controller import get_servo_controller
from phyto.types import I2cAddress, Pin


def main(
        i2c_bus_scl: Pin = config.I2C_BUS_SCL,
        i2c_bus_sda: Pin = config.I2C_BUS_SDA,
        i2c_bus_freq: int = config.I2C_BUS_FREQ,
        pca9685_0_i2c_address: I2cAddress = config.PCA9685_0_I2C_ADDRESS,
        pca9685_1_i2c_address: I2cAddress = config.PCA9685_1_I2C_ADDRESS,
        pca9685_pwm_freq: int = config.PCA9685_PWM_FREQ,
):
    i2c_bus = get_i2c_bus(i2c_bus_scl, i2c_bus_sda, i2c_bus_freq)

    servo_controller = get_servo_controller(
        i2c_bus,
        pca9685_0_i2c_address,
        pca9685_1_i2c_address,
        pca9685_pwm_freq,
    )

    base = get_base(servo_controller)

    while True:
        base.step(speed=1., direction=0.)


def get_i2c_bus(scl: Pin, sda: Pin, freq: int):
    while True:
        try:
            return I2C(scl, sda, frequency=freq)
        except RuntimeError as e:
            print(f'Error creating I2C bus; error={e}')
            print('Retrying...')
            sleep(1)
