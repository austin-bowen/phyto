import board

from phyto.types import I2cAddress, Pin

I2C_BUS_SDA: Pin = board.SDA
I2C_BUS_SCL: Pin = board.SCL
I2C_BUS_FREQ: int = 100000

PCA9685_0_I2C_ADDRESS: I2cAddress = 0x40
PCA9685_1_I2C_ADDRESS: I2cAddress = 0x41
PCA9685_PWM_FREQ: int = 50
