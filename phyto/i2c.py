from time import sleep

from busio import I2C

from phyto.types import Pin


def get_i2c_bus(scl: Pin, sda: Pin, freq: int):
    while True:
        try:
            return I2C(scl, sda, frequency=freq)
        except RuntimeError as e:
            print(f'Error creating I2C bus; error={e}')
            print('Retrying...')
            sleep(1)
