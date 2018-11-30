#!/usr/bin/python3

import signal
import pixels
import time
import sys
from pprint import pprint

wait=2

# test activating different quadrants
def test_quadrant():
    while True:
        try:
            pixels.set_max_brightness(1)
            pixels.run_quadrant()
            print("q 0")
            pixels.activate_quadrant(0)
            time.sleep(wait)
            print("q 1")
            pixels.activate_quadrant(1)
            time.sleep(wait)
            print("q 1&2")
            pixels.activate_quadrant(2, False)
            time.sleep(wait)
            print("q 3")
            pixels.activate_quadrant(3)
            time.sleep(wait)

            print("off")
            pixels.off()
            time.sleep(10)

        except KeyboardInterrupt:
            break

# test setting the maxumum brightness
def test_max_brightness():
    pixels.activate_quadrant(1)
    while True:
        try:
            pixels.run_quadrant()
            print("b 31")
            pixels.set_max_brightness(31)
            time.sleep(wait)
            print("b 16")
            pixels.set_max_brightness(16)
            time.sleep(wait)
            print("b 15")
            pixels.set_max_brightness(15)
            time.sleep(wait)
            print("b 8")
            pixels.set_max_brightness(8)
            time.sleep(wait)
            print("b 7")
            pixels.set_max_brightness(7)
            time.sleep(wait)
            print("b 4")
            pixels.set_max_brightness(4)
            time.sleep(wait)
            print("b 3")
            pixels.set_max_brightness(3)
            time.sleep(wait)
            print("b 2")
            pixels.set_max_brightness(2)
            time.sleep(wait)
            print("b 1")
            pixels.set_max_brightness(1)
            time.sleep(wait)
 
            print("off")
            pixels.off()
            time.sleep(wait)

        except KeyboardInterrupt:
            break

# test setting the brightness percentage
def test_bright_percent():
    pixels.activate_quadrant(1)
    while True:
        try:
            pixels.run_quadrant()
            print("bp 1")
            pixels.set_bright_percent(1)
            time.sleep(wait)
            print("bp 50")
            pixels.set_bright_percent(10)
            time.sleep(wait)
            print("bp 100")
            pixels.set_bright_percent(100)
            time.sleep(wait)

            print("off")
            pixels.off()
            time.sleep(wait)

        except KeyboardInterrupt:
            break

# test activating different directions
def test_direction():
    while True:
        try:
            print("d 0")
            pixels.run_direction(0)
            time.sleep(wait)
            print("d 45")
            pixels.run_direction(45)
            time.sleep(wait)
            print("d 90")
            pixels.run_direction(90)
            time.sleep(wait)
            print("d 180")
            pixels.run_direction(180)
            time.sleep(wait)

            print("off")
            pixels.off()
            time.sleep(10)

        except KeyboardInterrupt:
            break


# party time!
def test_party():
#     pixels.set_bright_percent(100)
    while True:
        print("sat 255")
        pixels.set_saturation(255)
        pixels.run_party()
        time.sleep(wait*2)
        print("sat 127")
        pixels.set_saturation(127)
        time.sleep(wait*2)
        print("sat 63")
        pixels.set_saturation(63)
        time.sleep(wait*2)
        print("sat 10")
        pixels.set_saturation(10)
        time.sleep(wait*2)
    signal.pause()

# start the test
pixels = pixels.Pixels()
if len(sys.argv)!=2:
    test_party()
elif sys.argv[1]=="1":
    test_quadrant()
elif sys.argv[1]=="2":
    test_max_brightness()
elif sys.argv[1]=="3":
    test_bright_percent()
elif sys.argv[1]=="4":
    test_direction()
else:
    test_party()

print("off")
pixels.off()
time.sleep(1)

