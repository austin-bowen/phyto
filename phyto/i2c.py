from time import sleep

from busio import I2C

from phyto import config
from phyto.types import Pin


def get_i2c_bus(
        scl: Pin = config.I2C_BUS_SCL,
        sda: Pin = config.I2C_BUS_SDA,
        freq: int = config.I2C_BUS_FREQ,
) -> I2C:
    while True:
        try:
            return I2C(scl, sda, frequency=freq)
        except RuntimeError as e:
            print(f'Error creating I2C bus; error={e}')
            print('Retrying...')
            sleep(1)
