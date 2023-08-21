import math

from phyto.base.leg import get_legs
from phyto.base.servo_controller import get_servo_controller, ServoController
from phyto.i2c import get_i2c_bus
from phyto.kinematics.inverse import InverseSolver3Dof
from phyto.motion import PositionSmoother
from phyto.types import Point3D


def leg_demo() -> None:
    with get_i2c_bus() as i2c_bus, get_servo_controller(i2c_bus) as servo_controller:
        run(servo_controller)


def run(servo_controller: ServoController) -> None:
    left_legs, right_legs = get_legs(servo_controller)

    legs = dict(
        lf=left_legs[0],
        lm=left_legs[1],
        lb=left_legs[2],
        rf=right_legs[0],
        rm=right_legs[1],
        rb=right_legs[2],
    )

    smoother = PositionSmoother(
        position=Point3D(0.1, 0, 0),
        speed=0.05,
    )

    leg_name = 'all'

    solver = InverseSolver3Dof(l0=.032, l1=.090, l2=.112)

    while True:
        try:
            print(f'Leg: {leg_name}')
            command = input('"<l|r><f|m|b>" OR "all" OR x,y,z: ')

            if command in legs or command == 'all':
                leg_name = command
                continue

            x, y, z = map(float, command.split(','))
            smoother.target = Point3D(x, y, z)

            while not smoother.at_target:
                position = smoother.position

                print(f'Position: {position}')

                theta0, theta1, theta2 = solver.solve(position.x, position.y, position.z)

                theta0 = math.degrees(theta0)
                theta1 = math.degrees(theta1)
                theta2 = math.degrees(theta2)

                print(f'Raw   : theta0={theta0}, theta1={theta1}, theta2={theta2}')

                theta0 = 90 - theta0
                theta1 = 90 - theta1
                theta2 = 180 + theta2

                print(f'Offset: theta0={theta0}, theta1={theta1}, theta2={theta2}')

                for leg in legs.values() if leg_name == 'all' else [legs[leg_name]]:
                    try:
                        leg.angles = (theta0, theta1, theta2)
                    except ValueError:
                        print(f'ERROR: Invalid angles for {leg.id}: {theta0}, {theta1}, {theta2}')
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f'ERROR: {repr(e)}')
