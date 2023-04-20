from phyto import config
from phyto.base import get_base
from phyto.base.base import Base
from phyto.base.servo_controller import get_servo_controller
from phyto.i2c import get_i2c_bus
from phyto.types import I2cAddress, Pin


def main(
        i2c_bus_scl: Pin = config.I2C_BUS_SCL,
        i2c_bus_sda: Pin = config.I2C_BUS_SDA,
        i2c_bus_freq: int = config.I2C_BUS_FREQ,
        pca9685_0_i2c_address: I2cAddress = config.PCA9685_0_I2C_ADDRESS,
        pca9685_1_i2c_address: I2cAddress = config.PCA9685_1_I2C_ADDRESS,
        pca9685_pwm_freq: int = config.PCA9685_PWM_FREQ,
):
    with get_i2c_bus(i2c_bus_scl, i2c_bus_sda, i2c_bus_freq) as i2c_bus:
        with get_servo_controller(
                i2c_bus,
                pca9685_0_i2c_address,
                pca9685_1_i2c_address,
                pca9685_pwm_freq,
        ) as servo_controller:
            base = get_base(servo_controller)
            run(base)


def run(base: Base) -> None:
    while True:
        command = input('command (stand, rest): ')

        if command == 'stand':
            base.stand(1.0, 0.0)
        elif command == 'rest':
            base.rest(1.0)
        else:
            print(f'invalid command: {command}')
