from phyto.base.servo_controller import get_servo_controller, ServoController
from phyto.i2c import get_i2c_bus


def servo_demo() -> None:
    with get_i2c_bus() as i2c_bus, get_servo_controller(i2c_bus) as servo_controller:
        run(servo_controller)


def run(servo_controller: ServoController) -> None:
    channel = 0
    servo = servo_controller.get_servo(channel)

    while True:
        angle = servo.angle if servo.angle is not None else 'off'
        print(f'[Servo {channel}/{servo_controller.channel_count - 1}; angle={angle}]')
        print(f'Enter one of: angle; "off" to disable servo; "s#" to switch servo; "q" to quit:')
        command = input(f'> ')

        try:
            if command == 'off':
                servo.angle = None
            elif command.startswith('s'):
                channel = int(command[1:])
                servo = servo_controller.get_servo(channel)
            elif command == 'q':
                print('Quitting')
                break
            else:
                servo.angle = int(command)
        except Exception as e:
            print(f'Invalid command={repr(command)}; error={e}')
