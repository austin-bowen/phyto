import math
import time

from phyto.eyes import get_eyes


def eyes_demo():
    eyes = get_eyes()

    while True:
        direction = eyes.brightest_direction()
        direction = math.degrees(direction)
        print(f'{direction:.2f}°')

        time.sleep(0.5)
