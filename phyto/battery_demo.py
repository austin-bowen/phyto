import time

from phyto.adc import get_adc
from phyto.battery import get_batteries
from phyto.i2c import get_i2c_bus


def battery_demo():
    with get_i2c_bus() as i2c_bus:
        adc = get_adc(i2c_bus)
        batteries = get_batteries(adc)

        while True:
            for name, battery in (
                    ('Logic battery', batteries.logic_battery),
                    ('Motor battery', batteries.motor_battery),
            ):
                print(f'{name}: {battery.voltage} (is_low={battery.voltage_is_low}')
            print()
            time.sleep(1)
