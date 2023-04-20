from busio import I2C

from phyto import config
from phyto.base.servo_controller import get_servo_controller
from phyto.types import Pin, I2cAddress


def servo_test(
        i2c_bus_sda: Pin = config.I2C_BUS_SDA,
        i2c_bus_scl: Pin = config.I2C_BUS_SCL,
        i2c_bus_freq: int = config.I2C_BUS_FREQ,
        pca9685_0_i2c_address: I2cAddress = config.PCA9685_0_I2C_ADDRESS,
        pca9685_1_i2c_address: I2cAddress = config.PCA9685_1_I2C_ADDRESS,
        pca9685_pwm_freq: int = config.PCA9685_PWM_FREQ,
) -> None:
    i2c_bus = I2C(i2c_bus_sda, i2c_bus_scl, frequency=i2c_bus_freq)

    servo_controller = get_servo_controller(
        i2c_bus,
        pca9685_0_i2c_address,
        pca9685_1_i2c_address,
        pca9685_pwm_freq,
    )

    channel = 0
    servo = servo_controller.get_servo(channel)

    while True:
        angle = servo.angle if servo.angle is not None else 'off'
        print(f'[Servo {channel}/{servo_controller.channel_count - 1}; angle={angle}]')
        print(f'Enter one of: angle; "off" to disable servo; "s#" to switch servo; "q" to quit:')
        command = input(f'> ')

        try:
            if command == 'off':
                servo.angle = None
            elif command.startswith('s'):
                channel = int(command[1:])
                servo = servo_controller.get_servo(channel)
            elif command == 'q':
                print('Quitting')
                break
            else:
                servo.angle = int(command)
        except Exception as e:
            print(f'Invalid command={repr(command)}; error={e}')
