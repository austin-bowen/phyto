import asyncio
import time

from busio import I2C

from phyto.adc import get_adc
from phyto.asyncio import be_nice
from phyto.base.base import Base, get_base
from phyto.base.servo_controller import ServoController
from phyto.battery import get_batteries, Batteries, BatteryMonitor
from phyto.buttons import Buttons, get_buttons
from phyto.buzzer import get_buzzer
from phyto.eyes import Eyes, get_eyes

Mode = str
WALK = 'walk'
REST = 'rest'

WalkSpeed = str
SLOW = 'slow'
FAST = 'fast'


def get_phyto(i2c_bus: I2C, servo_controller: ServoController) -> 'Phyto':
    adc = get_adc(i2c_bus)
    batteries = get_batteries(adc)
    buzzer = get_buzzer()
    battery_monitor = BatteryMonitor(batteries, buzzer)

    return Phyto(
        eyes=get_eyes(),
        base=get_base(servo_controller),
        buttons=get_buttons(),
        batteries=batteries,
        battery_monitor=battery_monitor,
    )


class Phyto:
    mode: 'Mode'
    eyes: Eyes
    base: Base
    buttons: Buttons
    batteries: Batteries
    battery_monitor: BatteryMonitor

    fast_walk_speed: float
    slow_walk_speed: float
    rest_speed: float

    def __init__(
            self,
            eyes: Eyes,
            base: Base,
            buttons: Buttons,
            batteries: Batteries,
            battery_monitor: BatteryMonitor,
            fast_walk_speed: float = 0.1,
            slow_walk_speed: float = 0.05,
            rest_speed: float = 0.05,
    ):
        self.mode = WALK
        self.eyes = eyes
        self.base = base
        self.buttons = buttons
        self.batteries = batteries
        self.battery_monitor = battery_monitor

        self.fast_walk_speed = fast_walk_speed
        self.slow_walk_speed = slow_walk_speed
        self.rest_speed = rest_speed

        self._walk_speed = SLOW
        self._resume_walking_time = None
        self._rested = False

        self._mode_toggle_button = self.buttons.button0
        self._walk_speed_button = self.buttons.button1

    @property
    def can_walk(self) -> bool:
        return not self.batteries.motor_battery.voltage_is_low

    async def run(self) -> None:
        await asyncio.gather(
            self.battery_monitor.run(),
            self._handle_mode_toggle_button(),
            self._handle_walk_speed_button(),
            self._run_base(),
        )

    async def _handle_mode_toggle_button(self) -> None:
        while True:
            await self._mode_toggle_button.until_pressed()
            self._toggle_mode()
            await self._mode_toggle_button.until_not_pressed()

    def _toggle_mode(self) -> None:
        if self.mode == WALK:
            self.mode = REST
            self._rested = False
        elif self.mode == REST:
            self.mode = WALK
            self._resume_walking_time = None
        else:
            raise RuntimeError(f'Unknown mode: {self.mode}')

        print(f'Mode: {self.mode}')

    async def _handle_walk_speed_button(self) -> None:
        while True:
            await self._walk_speed_button.until_pressed()
            self._toggle_walk_speed()
            await self._walk_speed_button.until_not_pressed()

    def _toggle_walk_speed(self) -> None:
        if self._walk_speed == FAST:
            self._walk_speed = SLOW
            self._resume_walking_time = None
        elif self._walk_speed == SLOW:
            self._walk_speed = FAST
        else:
            raise RuntimeError(f'Unknown walk speed: {self._walk_speed}')

        print(f'Walk speed: {self._walk_speed}')

    async def _run_base(self) -> None:
        while True:
            can_walk = self.can_walk

            if can_walk and self.mode == WALK:
                await self._walk_mode()
            elif not can_walk or self.mode == REST:
                await self._rest_mode()
            else:
                raise RuntimeError(f'Unknown mode: {self.mode}')

            await be_nice()

    async def _walk_mode(self) -> None:
        if self._walk_speed == FAST:
            await self._walk_fast()
        elif self._walk_speed == SLOW:
            await self._walk_slow()
        else:
            raise RuntimeError(f'Unknown walk speed: {self._walk_speed}')

    async def _walk_fast(self) -> None:
        direction = self.eyes.read().brightest_direction
        await self.base.walk(self.fast_walk_speed, direction, steps=1)

    async def _walk_slow(self) -> None:
        if self._should_resume_walking():
            eyes_reading = self.eyes.read()

            if eyes_reading.light_level < 0.92:
                direction = eyes_reading.brightest_direction
                await self.base.walk(self.slow_walk_speed, direction, steps=1)
                await self.base.rest(self.rest_speed)

            self._resume_walking_time = time.monotonic() + 60 * 1

    def _should_resume_walking(self) -> bool:
        return self._resume_walking_time is None or time.monotonic() > self._resume_walking_time

    async def _rest_mode(self) -> None:
        if not self._rested:
            self._rested = True
            await self.base.rest(self.rest_speed)
