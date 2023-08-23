from adafruit_debouncer import Debouncer

from phyto import config
from phyto.types import Pin

try:
    from digitalio import DigitalInOut, Direction, Pull
except ImportError:
    DigitalInOut = ...
    Direction = ...
    Pull = ...


def get_buttons(
        button0_pin: Pin = config.BUTTON0_PIN,
        button1_pin: Pin = config.BUTTON1_PIN,
) -> 'Buttons':
    return Buttons(
        button0=Button(button0_pin, pressed_level=False, pull=Pull.UP),
        button1=Button(button1_pin, pressed_level=False, pull=Pull.UP),
    )


class Buttons:
    button0: 'Button'
    button1: 'Button'

    def __init__(self, button0: 'Button', button1: 'Button'):
        self.button0 = button0
        self.button1 = button1


class Button:
    pressed_level: bool

    _debouncer: Debouncer

    def __init__(self, pin: Pin, pressed_level: bool, pull: Pull = None, debounce_interval: float = 0.01):
        self.pressed_level = pressed_level

        input_pin = DigitalInOut(pin)
        input_pin.direction = Direction.INPUT
        if pull is not None:
            input_pin.pull = pull

        self._debouncer = Debouncer(input_pin, interval=debounce_interval)

    @property
    def pressed(self) -> bool:
        self._debouncer.update()
        return self._debouncer.value == self.pressed_level

    def wait_not_pressed(self) -> None:
        while self.pressed:
            pass
