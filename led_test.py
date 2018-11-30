#!/usr/bin/python
import apa102
import time
from gpiozero import LED

class led:
    def __init__(self):
        self.power = LED(5)
        self.power.on()

        # Initialize the library and the strip
        self.strip = apa102.APA102(num_led=12, global_brightness=31)

        # Turn off all pixels (sometimes a few light up when the strip gets power)
        self.strip.clear_strip()

    def start(self, quadrant):
        # i = quadrant % 4
        i = ( quadrant % 4 ) * 3 + 1
        print i
        self.strip.set_pixel_rgb(i, 0xFFFFFF) # White
        self.strip.set_pixel_rgb(i+1, 0xFFFFFF) # White
        self.strip.show()
        time.sleep(0.2)
        self.strip.set_pixel_rgb(i, 0xFF0000) # Red
        self.strip.set_pixel_rgb(i+1, 0xFF0000) # Red
        self.strip.show()
        time.sleep(0.2)
        self.strip.set_pixel_rgb(i, 0x00FF00) # Green
        self.strip.set_pixel_rgb(i+1, 0x00FF00) # Green
        self.strip.show()
        time.sleep(0.2)
        self.strip.set_pixel_rgb(i, 0x0000FF) # Blue
        self.strip.set_pixel_rgb(i+1, 0x0000FF) # Blue
        self.strip.show()
        time.sleep(0.2)
        self.strip.clear_strip()

# Copy the buffer to the Strip (i.e. show the prepared pixels)
# strip.show()

# Wait a few Seconds, to check the result
# time.sleep(5)

# Clear the strip and shut down
if __name__ == '__main__':
    led = led()
    while True:
        q=int(raw_input('Input:'))
        led.start(q)
