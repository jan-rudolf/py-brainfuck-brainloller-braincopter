#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import image_png


class Brainfuck:
    """The interpreter of Brainfuck language."""
    def __init__(self, source_code: str, memory: bytes=b'\x00', memory_pointer: int=0) -> str:
        """__init__ method/constructor."""
        self.input = str()
        self.output = str()
        # instruction pointer - initially on 0 address
        instruction_pointer = 0

        # instruction memory for a source code
        self.instruction_memory = source_code

        # memory initialization
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer

        self.strip_comments()

        while instruction_pointer < len(self.instruction_memory):
            # get actual instruction from instruction memory
            instruction = self.instruction_memory[instruction_pointer]

            if instruction == '>':
                # move the pointer to the right
                instruction_pointer += 1

                self.memory_pointer += 1

                if len(self.memory) == self.memory_pointer:
                    self.memory.append(0)
                continue

            if instruction == '<':
                # move the pointer to the left
                instruction_pointer += 1
                self.memory_pointer = 0 if self.memory_pointer == 0 else self.memory_pointer - 1
                continue

            if instruction == '+':
                # increment the memory cell under the pointer
                instruction_pointer += 1
                self.memory[self.memory_pointer] = (self.memory[self.memory_pointer] + 1) % 256
                continue

            if instruction == '-':
                # decrement the memory cell under the pointer
                instruction_pointer += 1
                self.memory[self.memory_pointer] = 255 if self.memory[self.memory_pointer] == 0 else self.memory[self.memory_pointer] - 1
                continue

            if instruction == '.':
                # output the character signified by the cell at the pointer
                instruction_pointer += 1

                self.output += chr(self.memory[self.memory_pointer])
                print(chr(self.memory[self.memory_pointer]), sep='', end='')
                
                continue

            if instruction == ',':
                # input a character and store it in the cell at the pointer
                instruction_pointer += 1
                
                if len(self.input):
                    self.memory[self.memory_pointer] = ord(self.input[0])
                    self.input = self.input[1:]
                else:
                    self.memory[self.memory_pointer] = ord(sys.stdin.read(1))
                continue

            if instruction == '[' and self.memory[self.memory_pointer] == 0:
                # jump past the matching ] if the cell under the pointer is 0
                nested_cycle_bracket = 0

                while True:
                    instruction_pointer += 1
                    current_instruction = self.instruction_memory[instruction_pointer]

                    if current_instruction == ']' and nested_cycle_bracket == 0:
                        break

                    if current_instruction == ']':
                        nested_cycle_bracket -= 1

                    if current_instruction == '[':
                        nested_cycle_bracket += 1

                instruction_pointer += 1
                continue

            if instruction == ']' and self.memory[self.memory_pointer] != 0:
                # jump back to the matching [ if the cell under the pointer is nonzero
                nested_cycle_bracket = 0

                while True:
                    instruction_pointer = 0 if instruction_pointer == 0 else instruction_pointer - 1
                    current_instruction = self.instruction_memory[instruction_pointer]

                    if current_instruction == '[' and nested_cycle_bracket == 0:
                        break
                
                    if current_instruction == ']':
                        nested_cycle_bracket += 1

                    if current_instruction == '[':
                        nested_cycle_bracket -= 1

                instruction_pointer += 1
                continue

            #move instruction pointer to next address
            instruction_pointer += 1

    def strip_comments(self) -> None:
        """Delete comments from the source code of Brainfuck."""
        input_loading = False

        for instruction in self.instruction_memory:
            if input_loading:
                self.input += instruction

            if instruction == '!':
                if input_loading:
                    input_loading = False
                else:
                    input_loading = True

    def get_memory(self) -> bytes:
        """Get the memory of the interpreter."""
        return bytes(self.memory)


class Brainloller():
    """The interpreter of Brainloller. Transform a PNG image into Brainfuck source code nad run it."""
    
    def __init__(self, filename: str, run: bool=True) -> str:
        """__init__ method/constructor."""
        # Brainfuck source code
        self.brainfuck_source_code = str()

        # image data
        bitmap = image_png.PNGReader(filename).rgb
        bitmap_width = len(bitmap[0])
        bitmap_height = len(bitmap)

        # direction of parsing: R = right, L = left
        direction = 'R'
        row = 0
        column = 0

        while row >= 0 and row < bitmap_height and column >= 0 and column < bitmap_width:
            # translation of pixels to instructions

            if bitmap[row][column][0] == 255 and bitmap[row][column][1] == 0 and bitmap[row][column][2] == 0:
                # move the pointer to the right
                self.brainfuck_source_code += '>'

            if bitmap[row][column][0] == 128 and bitmap[row][column][1] == 0 and bitmap[row][column][2] == 0:
                # move the pointer to the left
                self.brainfuck_source_code += '<'

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 255 and bitmap[row][column][2] == 0:
                # increment the memory cell under the pointer
                self.brainfuck_source_code += '+'

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 128 and bitmap[row][column][2] == 0:
                # decrement the memory cell under the pointer
                self.brainfuck_source_code += '-'

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 0 and bitmap[row][column][2] == 255:
                # output the character signified by the cell at the pointer
                self.brainfuck_source_code += '.'

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 0 and bitmap[row][column][2] == 128:
                # input a character and store it in the cell at the pointer
                self.brainfuck_source_code += ','

            if bitmap[row][column][0] == 255 and bitmap[row][column][1] == 255 and bitmap[row][column][2] == 0:
                # jump past the matching ] if the cell under the pointer is 0
                self.brainfuck_source_code += '['

            if bitmap[row][column][0] == 128 and bitmap[row][column][1] == 128 and bitmap[row][column][2] == 0:
                # jump back to the matching [ if the cell under the pointer is nonzero
                self.brainfuck_source_code += ']'

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 255 and bitmap[row][column][2] == 255:
                # left rotation
                row += 1
                column = bitmap_width - 1
                direction = 'L'

            if bitmap_height == row or bitmap_width == column:
                    break

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 128 and bitmap[row][column][2] == 128:
                #right rotation
                row += 1
                column = 0
                direction = 'R'

            if direction == 'R':
                column += 1
            elif direction == 'L':
                column -= 1

        if run:
            self.program = Brainfuck(self.brainfuck_source_code)


class Braincopter():
    """The interpreter of Braincopter. Extract Brainfuck source code from a PNG image and run it."""
    
    def __init__(self, filename: str, run: bool=True) -> str:
        """__init__ method/constructor."""
        # Brainfuck source code
        self.brainfuck_source_code = str()

        # image data
        bitmap = image_png.PNGReader(filename).rgb
        bitmap_width = len(bitmap[0])
        bitmap_height = len(bitmap)

        #direction od parsing: L = left, R = right
        direction = 'R'
        row = 0
        column = 0

        while row >= 0 and row < bitmap_height and column >= 0 and column < bitmap_width:
            code = (65536 * bitmap[row][column][0] + 256 * bitmap[row][column][1] + bitmap[row][column][2]) % 11

            if code == 0:
                # move the pointer to the right
                self.brainfuck_source_code += '>'

            if code == 1:
                # move the pointer to the left
                self.brainfuck_source_code += '<'

            if code == 2:
                # increment the memory cell under the pointer
                self.brainfuck_source_code += '+'

            if code == 3:
                # decrement the memory cell under the pointer
                self.brainfuck_source_code += '-'

            if code == 4:
                # output the character signified by the cell at the pointer
                self.brainfuck_source_code += '.'

            if code == 5:
                # input a character and store it in the cell at the pointer
                self.brainfuck_source_code += ','

            if code == 6:
                # jump past the matching ] if the cell under the pointer is 0
                self.brainfuck_source_code += '['

            if code == 7:
                # jump back to the matching [ if the cell under the pointer is nonzero
                self.brainfuck_source_code += ']'

            if code == 8:
                #right rotation
                row += 1
                column = bitmap_width - 1
                direction = 'L'

            if code == 9:
                #left rotation
                row += 1
                column = 0
                direction = 'R'

            if direction == 'R':
                column += 1
            elif direction == 'L':
                column -= 1

        if run:
            self.program = Brainfuck(self.brainfuck_source_code)


class WhichBrainxPic():
    """Class for naive statistic classification of Brainfuck dialect based on pixels."""
    def __init__(self, src: list) -> None:
        """__init__ method/constructor."""
        self.format = str()

        counter_match = 0

        brainloller_instructions = [
            (255, 0, 0),
            (128, 0, 0),
            (0, 255, 0),
            (0, 128, 0),
            (0, 0, 255),
            (0, 0, 128),
            (255, 255, 0),
            (128, 128, 0)
        ]

        bitmap = image_png.PNGReader(src).rgb

        for pixel in bitmap[0]:
            if pixel in brainloller_instructions:
                counter_match += 1

        if counter_match >= (len(bitmap[0]) / 2):
            self.format = "bl"
        else:
            self.format = "bc"

#
# ensure to be able to run the script from command line
#

if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="source code or file with source code")

    arg = parser.parse_args()

    if os.path.isfile(arg.src):
        if arg.src.endswith(".txt") or arg.src.endswith(".b"):
            brainfuck_source_code = str()

            with open(arg.src, "r", encoding="ascii") as f:
                lines = f.readlines()

            for line in lines:
                brainfuck_source_code += line

            Brainfuck(brainfuck_source_code)
        elif arg.src.endswith(".png"):
            format_ = WhichBrainxPic(arg.src).format

            if format_ == "bl":
                Brainloller(arg.src)
            else:
                Braincopter(arg.src)
        else:
            print("src: unknown source file")
    else:
        Brainfuck(arg.src)


