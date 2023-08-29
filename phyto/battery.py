from phyto import config
from phyto.adc import ADC


def get_batteries(
        adc: ADC,
        logic_battery_channel: int = config.LOGIC_BATTERY_CHANNEL,
        motor_battery_channel: int = config.MOTOR_BATTERY_CHANNEL,
        low_voltage: float = config.LOW_BATTERY_VOLTAGE,
) -> 'Batteries':
    return Batteries(
        logic_battery=Battery(adc, logic_battery_channel, low_voltage),
        motor_battery=Battery(adc, motor_battery_channel, low_voltage),
    )


class Battery:
    adc: ADC
    channel: int
    low_voltage: float

    def __init__(self, adc: ADC, channel: int, low_voltage: float):
        self.adc = adc
        self.channel = channel
        self.low_voltage = low_voltage

    @property
    def voltage(self) -> float:
        return self.adc.read(self.channel)

    @property
    def voltage_is_low(self) -> bool:
        return self.voltage <= self.low_voltage


class Batteries:
    logic_battery: Battery
    motor_battery: Battery

    def __init__(self, logic_battery: Battery, motor_battery: Battery):
        self.logic_battery = logic_battery
        self.motor_battery = motor_battery
