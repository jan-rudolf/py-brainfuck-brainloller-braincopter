#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import argparse
import math

import brainx
import image_png


class Brainfuck2Brainloller():
    def __init__(self, brainfuck_source_code):
        data = list()

        for command in brainfuck_source_code:
            if command == '>':
                data.append([255, 0, 0])

            if command == '<':
                data.append([128, 0, 0])

            if command == '+':
                data.append([0, 255, 0])

            if command == '-':
                data.append([0, 128, 0])

            if command == '.':
                data.append([0, 0, 255])

            if command == ',':
                data.append([0, 0, 128])

            if command == '[':
                data.append([255, 255, 0])

            if command == ']':
                data.append([128, 128, 0])

        row = list()
        direction = 'R'
        width = math.ceil(math.sqrt(len(brainfuck_source_code)))

        self.bitmap = list()

        for pixel in data:
            if (len(row) + 1) < width:
                if direction == 'R':
                    row.append(pixel)
                else:
                    row.insert(0, pixel)

            elif (len(row) + 1) == width:
                # rotation right
                if direction == 'R':
                    row.append([0, 255, 255])
                    self.bitmap.append(row)
                    
                    direction = 'L'

                    # rotation left
                    row = list()
                    row.insert(0, [0, 255, 255])
                    row.insert(0, pixel)
                else:
                    row.insert(0, [0, 128, 128])

                    self.bitmap.append(row)

                    direction = 'R'

                    row = list()
                    row.append([0, 128, 128])
                    row.append(pixel)

        # padding
        padding = width - len(row)

        for i in range(padding):
            # enter padding
            if direction == 'R':
                row.append([123, 123, 123])
            else:
                row.insert(0, [123, 123, 123])

        self.bitmap.append(row)


class Brainfuck2Braincopter():
    def __init__(self, bitmap, brainfuck_source_code):
        self.transition_table = {
            '>': 0,
            '<': 1,
            '+': 2,
            '-': 3,
            '.': 4,
            ',': 5,
            '[': 6,
            ']': 7,
            'R': 8,
            'L': 9,
            'N': 10
        }
        self.bitmap = bitmap
        self.bitmap_width = len(bitmap[0])
        self.bitmap_height = len(bitmap)
        self.brainfuck = brainfuck_source_code

        if len(self.brainfuck) > (self.bitmap_height * self.bitmap_width):
            print(
                "warning: Brainfuck source code is longer than this picture's bitmap, it will not encode the whole code"
            )

        row = 0
        column = 0
        direction = 'R'
        counter = 0

        while row >= 0 and row < self.bitmap_height and column >= 0 and column < self.bitmap_width:
            if (column + 1) == self.bitmap_width or (column == 0 and row > 0):
                if (column + 1) == self.bitmap_width:
                    braincopter_number = self.transition_table['R']
                    old_pixel = self.bitmap[row][column]
                    new_pixel = self.brainfuck_pixel_encode(braincopter_number, old_pixel)
                    self.bitmap[row][column] = new_pixel

                    row += 1

                    if row >= self.bitmap_height:
                        break

                    self.bitmap[row][column] = new_pixel

                    direction = 'L'

                if column == 0 and row > 0:
                    braincopter_number = self.transition_table['L']
                    old_pixel = self.bitmap[row][column]
                    new_pixel = self.brainfuck_pixel_encode(braincopter_number, old_pixel)
                    self.bitmap[row][column] = new_pixel

                    row += 1

                    if row >= self.bitmap_height:
                        break

                    self.bitmap[row][column] = new_pixel

                    direction = 'R'

            elif counter < len(self.brainfuck):
                braincopter_number = self.transition_table[self.brainfuck[counter]]
                old_pixel = self.bitmap[row][column]
                new_pixel = self.brainfuck_pixel_encode(braincopter_number, old_pixel)
                self.bitmap[row][column] = new_pixel

                counter += 1

            else:
                braincopter_number = self.transition_table['N']
                old_pixel = self.bitmap[row][column]
                new_pixel = self.brainfuck_pixel_encode(braincopter_number, old_pixel)
                self.bitmap[row][column] = new_pixel

                counter += 1

            if direction == 'R':
                column += 1
            else:
                column -= 1

    def brainfuck_pixel_encode(self, value, pixel):
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        while ((65536 * r + 256 * g + b) % 11) != value:
            b = (b + 1) % 256

        return r, g, b


def bf2bl(src, dst):
    # Brainfuck to Brainloller
    brainfuck_source_code = str()

    with open(src, "r", encoding="ascii") as f:
        lines = f.readlines()

    for line in lines:
        brainfuck_source_code += line

    bitmap = Brainfuck2Brainloller(brainfuck_source_code).bitmap

    image_png.PNGWriter(bitmap, dst)


def bl2bf(src, dst):
    # Brainloller to Brainfuck
    program = brainx.Brainloller(src, run=False)

    with open(dst, "w", encoding="ascii") as f:
        f.write(program.data)


def bc2bf(src, dst):
    # Braincopter to Brainfuck
    program = brainx.Braincopter(src, run=False)

    with open(dst, "w", encoding="ascii") as f:
        f.write(program.data)


def bf2bc(src, dst):
    # Brainfuck to Braincopter
    brainfuck_code = str()

    with open(src, "r", encoding="ascii") as f:
        lines = f.readlines()

    for line in lines:
        brainfuck_code += line

    bitmap = image_png.PNGReader(dst).rgb

    bitmap = Brainfuck2Braincopter(bitmap, brainfuck_code).bitmap

    image_png.PNGWriter(bitmap, dst)


def bl2bc(src, dst):
    # Brainloller to Braincopter
    brainfuck_code = brainx.Brainloller(src, run=False).data

    bitmap = image_png.PNGReader(dst).rgb
    bitmap = Brainfuck2Braincopter(bitmap, brainfuck_code).bitmap

    image_png.PNGWriter(bitmap, dst)


def bc2bl(src, dst):
    # Braincopter to Brainloller
    brainfuck_code = brainx.Braincopter(src, run=False).data

    bitmap = Brainfuck2Brainloller(brainfuck_code).bitmap

    image_png.PNGWriter(bitmap, dst)


if __name__ == "__main__":
    # a dict of conversion functions
    convert_functions = {
        "bf2bl": bf2bl,
        "bl2bf": bl2bf,
        "bc2bf": bc2bf,
        "bf2bc": bf2bc,
        "bl2bc": bl2bc,
        "bc2bl": bc2bl
    }

    format_from = str()
    format_to = str()

    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="path to the source file")
    parser.add_argument("dst", help="path to the destination file")
    arg = parser.parse_args()

    if arg.src.endswith('.png') or arg.src.endswith('.txt') or arg.src.endswith('.b'):
        if arg.src.endswith('.png'):
            format_from = brainx.WhichBrainxPic(arg.src).format

        if arg.src.endswith('.txt') or arg.src.endswith('.b'):
            format_from = "bf"

    else:
        print("src: unknown source file")

    if arg.dst.endswith('.png') or arg.dst.endswith('.txt') or arg.dst.endswith('.b'):

        if arg.dst.endswith('.png'):
            if os.path.isfile(arg.dst):
                format_to = "bc"

            if format_from == "bl":
                format_to = "bc"
            elif len(format_to) == 0:
                format_to = "bl"

        if arg.dst.endswith('.txt') or arg.dst.endswith('.b'):
            format_to = "bf"
    else:
        print("dst: unknown source file")

    conversion_string = '{}2{}'.format(format_from, format_to)

    if conversion_string in convert_functions:
        print("conversion: {}".format(conversion_string))
        convert_functions[conversion_string](arg.src, arg.dst)
    else:
        print("unknown conversion {}".format(conversion_string))

