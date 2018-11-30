#!/usr/bin/env python

# Copyright (C) 2017 Seeed Technology Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numpy
import time
import json

class HushLedPattern(object):
    def __init__(self, show=None, number=12, saturation=127):
        self.pixels_number = number
        self.pixels = [0] * 4 * number
        self.saturation = saturation

        self.set_basis()

        if not show or not callable(show):
            def dummy(data):
                pass
            show = dummy

        self.show = show
        self.stop = False

    # cycle the colors in the quadrant
    def quadrant(self, quadrant):
        colors = [[ 0, self.saturation, 0, 0 ], [ 0, 0, self.saturation, 0], [ 0, 0, 0, self.saturation ]]
        color = 0
        step = 1
        position = 12
        while not self.stop:
            pixels = []
            for q in range(4):
                for p in range(q*3, q*3+3):
                    if quadrant[q]:
                        pixels.extend(colors[color])
                    else:
                        pixels.extend([0,self.saturation,self.saturation,self.saturation])
            self.show(pixels)
            time.sleep(0.4)
            color = ( color + 1 ) % 3

    def direction(self, direction=0):
        colors = [[ 0, self.saturation, 0, 0 ], [ 0, 0, self.saturation, 0], [ 0, 0, 0, self.saturation ]]
        color = 0
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number

        pixels = [0, self.saturation, self.saturation, self.saturation] * self.pixels_number
        while not self.stop:
            for i in range(3):
                pixels[position * 4 + i+1] = colors[color][i+1]
            self.show(pixels)
            time.sleep(0.4)
            color = ( color + 1 ) % 3

    # pattern for party
    def party(self, direction=0):
        while not self.stop:
            position = int((direction + 15) / 30) % 12

            basis = numpy.roll(self.basis, position * 4)
            import pprint
            pprint.pprint(basis)
            for i in range(1, 25):
                pixels = basis * i
                if self.stop:
                    break
                self.show(pixels)
                time.sleep(0.05)

            pixels = numpy.roll(pixels, 4)
            self.show(pixels)
            time.sleep(0.1)

            for i in range(2):
                new_pixels = numpy.roll(pixels, 4)
                if self.stop:
                    break
                self.show(new_pixels * 0.5 + pixels)
                pixels = new_pixels
                time.sleep(0.1)

            if self.stop:
                break
            self.show(pixels)
            self.pixels = pixels

    # all off
    def off(self):
        self.show([0] * 4 * 12)

    # set saturation
    def set_saturation(self, saturation):
        self.saturation = saturation
        self.set_basis()

    # set basis color array
    def set_basis(self):
        self.basis = numpy.array([0] * 4 * 12)
        self.basis[0 * 4 + 1] = self.saturation
        self.basis[3 * 4 + 1] = self.saturation / 2
        self.basis[3 * 4 + 2] = self.saturation / 2
        self.basis[6 * 4 + 2] = self.saturation
        self.basis[9 * 4 + 3] = self.saturation


