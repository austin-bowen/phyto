import math

from phyto.base import get_base
from phyto.base.servo_controller import get_servo_controller, ServoController
from phyto.i2c import get_i2c_bus


def base_demo() -> None:
    with get_i2c_bus() as i2c_bus, get_servo_controller(i2c_bus) as servo_controller:
        run(servo_controller)


def run(servo_controller: ServoController) -> None:
    base = get_base(servo_controller)

    speed = 0.1

    direction = math.radians(0)

    while True:
        try:
            steps = int(input('steps: '))
            base.walk(speed, direction, steps)
        except KeyboardInterrupt:
            base.rest(speed)
            break
        except Exception as e:
            print(f'ERROR: {repr(e)}')
