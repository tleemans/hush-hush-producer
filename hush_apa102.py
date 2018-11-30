"""
    extend the apa102 class to add setting max_brightness
    """
import apa102

class HUSH_APA102(apa102.APA102):

    # set the max_brightness
    def set_max_brightness(self, brightness):
        # Limit the brightness to the maximum if it's set higher
        if brightness > self.MAX_BRIGHTNESS:
            self.global_brightness = self.MAX_BRIGHTNESS
        else:
            self.global_brightness = brightness

