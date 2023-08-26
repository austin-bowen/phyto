import time

from phyto.eyes import get_eyes


def eyes_demo():
    eyes = get_eyes()

    while True:
        print(eyes.read())
        time.sleep(0.5)
