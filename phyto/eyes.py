import math
from abc import abstractmethod

try:
    from analogio import AnalogIn
except NotImplementedError:
    AnalogIn = ...

from phyto import config
from phyto.types import Pin


def get_eyes(
        left_eye_adc_pin: Pin = config.LEFT_EYE_ADC_PIN,
        right_eye_adc_pin: Pin = config.RIGHT_EYE_ADC_PIN,
        back_eye_adc_pin: Pin = config.BACK_EYE_ADC_PIN,
) -> 'Eyes':
    return Eyes(
        left_eye=AdcEye(AnalogIn(left_eye_adc_pin)),
        right_eye=AdcEye(AnalogIn(right_eye_adc_pin)),
        back_eye=AdcEye(AnalogIn(back_eye_adc_pin)),
    )


class Eye:
    @abstractmethod
    def read(self) -> float:
        ...


class AdcEye(Eye):
    adc_pin: AnalogIn

    def __init__(self, adc_pin: AnalogIn):
        self.adc_pin = adc_pin

    def read(self) -> float:
        return self.adc_pin.value / 65535


class Eyes:
    left_eye: Eye
    right_eye: Eye
    back_eye: Eye

    _cos_theta: float
    _sin_theta: float

    def __init__(self, left_eye: Eye, right_eye: Eye, back_eye: Eye):
        self.left_eye = left_eye
        self.right_eye = right_eye
        self.back_eye = back_eye

        theta = math.radians(60)
        self._cos_theta = math.cos(theta)
        self._sin_theta = math.sin(theta)

    def read(self) -> 'EyesReading':
        left = self.left_eye.read()
        right = self.right_eye.read()
        back = self.back_eye.read()

        x = (left + right) * self._cos_theta - back
        y = (left - right) * self._sin_theta

        return EyesReading(
            brightest_direction=math.atan2(y, x),
            direction_magnitude=math.sqrt(x ** 2 + y ** 2),
            light_level=(left + right + back) / 3,
        )


class EyesReading:
    brightest_direction: float
    direction_magnitude: float
    light_level: float

    def __init__(self, brightest_direction: float, direction_magnitude: float, light_level: float):
        self.brightest_direction = brightest_direction
        self.direction_magnitude = direction_magnitude
        self.light_level = light_level

    def __repr__(self) -> str:
        dir_degrees = math.degrees(self.brightest_direction)
        return (
            f'EyesReading(' +
            f'brightest_direction={dir_degrees:.3f}°, ' +
            f'direction_magnitude={self.direction_magnitude:.3f}, ' +
            f'light_level={self.light_level:.3f})'
        )
