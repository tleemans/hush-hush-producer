#!/usr/bin/python3

import time
import threading
import signal
from gpiozero import LED
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from hush_led_pattern import HushLedPattern
import hush_apa102

class Pixels:
    PIXELS_N = 12
    quadrant = [False] * 4
    bright_percent = 50

    def __init__(self, pattern=HushLedPattern, max_brightness=31):
        self.pattern = pattern(show=self.show)
        self.max_brightness = int(max_brightness) % 32

        self.dev = hush_apa102.HUSH_APA102(num_led=self.PIXELS_N, global_brightness=self.max_brightness)
        
        self.power = LED(5)
        self.power.on()

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    # Add the function to the queue
    def run_quadrant(self):
        def f():
            self.pattern.quadrant(self.quadrant)
        self.put(f)

    # Add the function to the queue
    def run_direction(self, direction):
        def f():
            self.pattern.direction(direction)
        self.put(f)

    # Add the function to the queue
    def run_party(self):
        def f():
            self.pattern.party()
        self.put(f)

    # activate a quadrant
    def activate_quadrant(self, quadrant, exclusive=True):
        if exclusive:
            for i in range(4):
                self.quadrant[i] = False
        self.quadrant[quadrant]=True

    # deactivate a quadrant
    def deactivate_quadrant(self, quadrant):
        self.quadrant[quadrant]=False

    # set the maximum brightness
    def set_max_brightness(self, brightness):
        self.dev.set_max_brightness(brightness)

    # set the maximum brightness
    def set_bright_percent(self, brightness):
        self.bright_percent=brightness

    # set the maximum brightness
    def set_saturation(self, saturation):
        self.pattern.set_saturation(saturation)

    def off(self):
        self.put(self.pattern.off)
        time.sleep(0.5)
        self.dev.clear_strip()

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]), self.bright_percent)
        self.dev.show()

if __name__ == '__main__':
    pixels = Pixels()

    pixels.run_party()
    signal.pause()
