import asyncio

from phyto.base.servo_controller import get_servo_controller
from phyto.i2c import get_i2c_bus
from phyto.phyto import get_phyto


def main() -> None:
    with get_i2c_bus() as i2c_bus, get_servo_controller(i2c_bus) as servo_controller:
        phyto = get_phyto(i2c_bus, servo_controller)
        asyncio.run(phyto.run())
