I2cAddress = int

try:
    from adafruit_blinka.microcontroller import generic_micropython

    Pin = generic_micropython.Pin
except ImportError:
    Pin = ...
