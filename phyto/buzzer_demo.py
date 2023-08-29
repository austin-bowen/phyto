import asyncio

from phyto.buzzer import get_buzzer


def buzzer_demo():
    asyncio.run(_buzzer_demo())


async def _buzzer_demo():
    buzzer = get_buzzer()

    while True:
        for count in range(1, 6):
            await buzzer.chirp(count)
            await asyncio.sleep(3)
