import time

from phyto.base.base import Base, get_base
from phyto.base.servo_controller import ServoController
from phyto.buttons import Buttons, get_buttons
from phyto.eyes import Eyes, get_eyes

Mode = str
WALK = 'walk'
REST = 'rest'

WalkSpeed = str
SLOW = 'slow'
FAST = 'fast'


def get_phyto(servo_controller: ServoController) -> 'Phyto':
    return Phyto(
        eyes=get_eyes(),
        base=get_base(servo_controller),
        buttons=get_buttons(),
    )


class Phyto:
    mode: 'Mode'
    eyes: Eyes
    base: Base
    buttons: Buttons

    fast_walk_speed: float
    slow_walk_speed: float
    rest_speed: float

    def __init__(
            self,
            eyes: Eyes,
            base: Base,
            buttons: Buttons,
            fast_walk_speed: float = 0.1,
            slow_walk_speed: float = 0.05,
            rest_speed: float = 0.05,
    ):
        self.mode = WALK
        self.eyes = eyes
        self.base = base
        self.buttons = buttons

        self.fast_walk_speed = fast_walk_speed
        self.slow_walk_speed = slow_walk_speed
        self.rest_speed = rest_speed

        self._walk_speed = SLOW
        self._resume_walking_time = None
        self._rested = False

        self._mode_toggle_button = self.buttons.button0
        self._walk_speed_button = self.buttons.button1

    def run(self) -> None:
        try:
            while True:
                if self._mode_toggle_button.pressed:
                    self._mode_toggle_button.wait_not_pressed()
                    self._toggle_mode()

                if self.mode == WALK:
                    self._walk_mode()
                elif self.mode == REST:
                    self._rest_mode()
                else:
                    raise RuntimeError(f'Unknown mode: {self.mode}')
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f'ERROR: {repr(e)}')
        finally:
            self.base.rest(self.rest_speed)

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

    def _walk_mode(self) -> None:
        if self._walk_speed_button.pressed:
            self._walk_speed_button.wait_not_pressed()
            self._toggle_walk_speed()

        if self._walk_speed == FAST:
            self._walk_fast()
        elif self._walk_speed == SLOW:
            self._walk_slow()
        else:
            raise RuntimeError(f'Unknown walk speed: {self._walk_speed}')

    def _toggle_walk_speed(self) -> None:
        if self._walk_speed == FAST:
            self._walk_speed = SLOW
            self._resume_walking_time = None
        elif self._walk_speed == SLOW:
            self._walk_speed = FAST
        else:
            raise RuntimeError(f'Unknown walk speed: {self._walk_speed}')

        print(f'Walk speed: {self._walk_speed}')

    def _walk_fast(self) -> None:
        direction = self.eyes.brightest_direction()
        self.base.walk(self.fast_walk_speed, direction, steps=1)

    def _walk_slow(self) -> None:
        if self._should_resume_walking():
            direction = self.eyes.brightest_direction()
            self.base.walk(self.slow_walk_speed, direction, steps=1)
            self.base.rest(self.rest_speed)
            self._resume_walking_time = time.monotonic() + 60 * 1

    def _should_resume_walking(self) -> bool:
        return self._resume_walking_time is None or time.monotonic() > self._resume_walking_time

    def _rest_mode(self) -> None:
        if not self._rested:
            self._rested = True
            self.base.rest(self.rest_speed)
