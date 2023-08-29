import time

from phyto.adc import get_adc
from phyto.i2c import get_i2c_bus


def adc_demo():
    i2c = get_i2c_bus()
    adc = get_adc(i2c)

    while True:
        voltages = []
        for channel in (0, 4):
            voltage = adc.read(channel)
            voltages.append(f'{channel}={voltage:.2f}V')

        print('; '.join(voltages))
        time.sleep(0.5)
