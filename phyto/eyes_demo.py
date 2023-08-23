import math
import time

from phyto.eyes import get_eyes


def eyes_demo():
    eyes = get_eyes()

    while True:
        direction = eyes.brightest_direction()
        direction = math.degrees(direction)

        level = eyes.light_level()

        print(f'direction={direction:.2f}°;\tlevel={level:.2f}')

        time.sleep(0.5)
