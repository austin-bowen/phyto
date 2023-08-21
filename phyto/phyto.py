from phyto.base.base import Base, get_base
from phyto.base.servo_controller import ServoController
from phyto.eyes import Eyes, get_eyes


def get_phyto(servo_controller: ServoController) -> 'Phyto':
    return Phyto(
        eyes=get_eyes(),
        base=get_base(servo_controller),
    )


class Phyto:
    eyes: Eyes
    base: Base

    def __init__(self, eyes: Eyes, base: Base):
        self.eyes = eyes
        self.base = base

    def run(self) -> None:
        ...
