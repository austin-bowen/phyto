from phyto.base.base_demo import base_demo
from phyto.base.servo_controller import get_servo_controller
from phyto.i2c import get_i2c_bus
from phyto.phyto_ import get_phyto


def main() -> None:
    base_demo()
    return

    with get_i2c_bus() as i2c_bus, get_servo_controller(i2c_bus) as servo_controller:
        phyto = get_phyto(servo_controller)
        phyto.run()
