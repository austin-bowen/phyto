import asyncio


def get_buzzer(

) -> 'Buzzer':
    return Buzzer()


class Buzzer:
    def start(self, freq: float) -> None:
        ...

    def stop(self) -> None:
        ...

    async def timed_buzz(self, freq: float, seconds: float) -> None:
        self.start(freq)
        await asyncio.sleep(seconds)
        self.stop()
