import board

from phyto.types import I2cAddress, Pin

try:
    I2C_BUS_SCL: Pin = board.GP21
    I2C_BUS_SDA: Pin = board.GP20

    LEFT_EYE_ADC_PIN: Pin = board.A0
    RIGHT_EYE_ADC_PIN: Pin = board.A1
    BACK_EYE_ADC_PIN: Pin = board.A2

    BUTTON0_PIN: Pin = board.GP0
    BUTTON1_PIN: Pin = board.GP4
except AttributeError:
    I2C_BUS_SCL: Pin = ...
    I2C_BUS_SDA: Pin = ...

    LEFT_EYE_ADC_PIN: Pin = ...
    RIGHT_EYE_ADC_PIN: Pin = ...
    BACK_EYE_ADC_PIN: Pin = ...

    BUTTON0_PIN: Pin = ...
    BUTTON1_PIN: Pin = ...

I2C_BUS_FREQ: int = 100000

PCA9685_0_I2C_ADDRESS: I2cAddress = 0x40
PCA9685_1_I2C_ADDRESS: I2cAddress = 0x41
PCA9685_PWM_FREQ: int = 50
