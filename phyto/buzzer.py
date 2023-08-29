import asyncio

from digitalio import DigitalInOut, Direction

from phyto import config
from phyto.types import Pin


def get_buzzer(
    pin: Pin = config.BUZZER_PIN,
) -> 'Buzzer':
    pin = DigitalInOut(pin)
    pin.direction = Direction.OUTPUT

    return Buzzer(pin)


class Buzzer:
    pin: DigitalInOut

    def __init__(self, pin: DigitalInOut):
        self.pin = pin
        self.is_on = False

    @property
    def is_on(self) -> bool:
        return self.pin.value

    @is_on.setter
    def is_on(self, is_on: bool) -> None:
        self.pin.value = is_on

    async def timed_buzz(self, seconds: float) -> None:
        self.is_on = True
        await asyncio.sleep(seconds)
        self.is_on = False

    async def timed_buzzes(self, count: int, on_seconds: float, off_seconds: float) -> None:
        for _ in range(count):
            await self.timed_buzz(on_seconds)
            await asyncio.sleep(off_seconds)

    async def chirp(self, count: int) -> None:
        await self.timed_buzzes(count, on_seconds=0.01, off_seconds=0.05)
