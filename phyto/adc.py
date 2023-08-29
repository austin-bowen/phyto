from abc import abstractmethod

from adafruit_bus_device.i2c_device import I2CDevice
from busio import I2C

from phyto import config
from phyto.types import I2cAddress


def get_adc(
        i2c_bus: I2C,
        i2c_address: I2cAddress = config.ADS7830_I2C_ADDRESS,
) -> 'ADC':
    i2c_device = I2CDevice(i2c_bus, i2c_address)
    return ADS7830(i2c_device)


class ADC:
    @abstractmethod
    def read(self, channel: int) -> float:
        ...


class ADS7830(ADC):
    i2c_device: I2CDevice

    def __init__(self, i2c_device: I2CDevice):
        self.i2c_device = i2c_device
        self._voltage_scalar = 15.6 / 255

    def read(self, channel: int) -> float:
        if channel < 0 or channel > 7:
            raise ValueError(f'channel must be in range [0, 7]. channel={channel}')

        command = 0x84 | (((channel << 2 | channel >> 1) & 0x07) << 4)
        out_buffer = bytes([command])
        in_buffer = bytearray(1)

        with self.i2c_device:
            self.i2c_device.write_then_readinto(out_buffer, in_buffer)

        return in_buffer[0] * self._voltage_scalar
