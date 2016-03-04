#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import image_png


class BrainFuck:
    """interpret of brainfuck"""
    def input_check(self):
        input_loading = False

        for instruction in self.data:
            if input_loading:
                self.input += instruction

            if instruction == '!':
                if input_loading:
                    input_loading = False
                else:
                    input_loading = True
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """init of interpreter"""
        
        # program data
        self.data = data
        instruction_pointer = 0
        
        # inicialization of variables
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer

        self.input = ''

        self.input_check()

        self.output = ''

        while instruction_pointer < len(self.data):
            instruction = self.data[instruction_pointer]

            if instruction == '>':
                instruction_pointer += 1

                self.memory_pointer += 1

                if len(self.memory) == self.memory_pointer:
                    self.memory.append(0)
                continue

            if instruction == '<':
                instruction_pointer += 1
                self.memory_pointer =  0 if self.memory_pointer == 0 else self.memory_pointer - 1
                continue

            if instruction == '+':
                instruction_pointer += 1
                self.memory[self.memory_pointer] = (self.memory[self.memory_pointer] + 1) % 256
                continue

            if instruction == '-':
                instruction_pointer += 1
                self.memory[self.memory_pointer] = 255 if self.memory[self.memory_pointer] == 0 else self.memory[self.memory_pointer] - 1
                continue

            if instruction == '.':
                instruction_pointer += 1

                self.output += chr(self.memory[self.memory_pointer])
                print(chr(self.memory[self.memory_pointer]), sep='', end='')
                
                continue

            if instruction == ',':
                instruction_pointer += 1
                
                if len(self.input):
                    self.memory[self.memory_pointer] = ord(self.input[0])
                    self.input = self.input[1:]
                else:
                    self.memory[self.memory_pointer] = ord(sys.stdin.read(1))
                continue

            if instruction == '[' and self.memory[self.memory_pointer] == 0:
                nested_cycle_bracket = 0

                while True:
                    instruction_pointer += 1
                    current_instruction = self.data[instruction_pointer]

                    if current_instruction == ']' and nested_cycle_bracket == 0:
                        break

                    if current_instruction == ']':
                        nested_cycle_bracket -= 1

                    if current_instruction == '[':
                        nested_cycle_bracket += 1

                instruction_pointer += 1
                continue

            if instruction == ']' and self.memory[self.memory_pointer] != 0:
                nested_cycle_bracket = 0

                while True:
                    instruction_pointer = 0 if instruction_pointer == 0 else instruction_pointer - 1
                    current_instruction = self.data[instruction_pointer]

                    if current_instruction == '[' and nested_cycle_bracket == 0:
                        break
                
                    if current_instruction == ']':
                        nested_cycle_bracket += 1

                    if current_instruction == '[':
                        nested_cycle_bracket -= 1

                instruction_pointer += 1
                continue

            instruction_pointer += 1
    
    #
    # for test need
    #
    def get_memory(self):
        return bytes(self.memory)


class BrainLoller():
    """class for Brainloller"""
    
    def __init__(self, filename, run=True):
        """init"""
        
        # stores source code of Brainfuck
        self.data = ''

        bitmap = image_png.PngReader(filename).rgb
        bitmap_width = len(bitmap[0])
        bitmap_height = len(bitmap)

        # direction of parsing - R = right, L = left
        direction = 'R'
        row = 0
        column = 0

        while row >= 0 and row < bitmap_height and column >= 0 and column < bitmap_width:
            if bitmap[row][column][0] == 255 and bitmap[row][column][1] == 0 and bitmap[row][column][2] == 0:
                self.data += '>'

            if bitmap[row][column][0] == 128 and bitmap[row][column][1] == 0 and bitmap[row][column][2] == 0:
                self.data += '<'

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 255 and bitmap[row][column][2] == 0:
                self.data += '+'

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 128 and bitmap[row][column][2] == 0:
                self.data += '-'

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 0 and bitmap[row][column][2] == 255:
                self.data += '.'

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 0 and bitmap[row][column][2] == 128:
                self.data += ','

            if bitmap[row][column][0] == 255 and bitmap[row][column][1] == 255 and bitmap[row][column][2] == 0:
                self.data += '['

            if bitmap[row][column][0] == 128 and bitmap[row][column][1] == 128 and bitmap[row][column][2] == 0:
                self.data += ']'

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
            self.program = BrainFuck(self.data)


class BrainCopter():
    """class BrainCopter"""
    
    def __init__(self, filename, run=True):
        """init"""
        
        # contains source code of Brainfuck
        self.data = ''

        bitmap = image_png.PngReader(filename).rgb
        bitmap_width = len(bitmap[0])
        bitmap_height = len(bitmap)

        #direction od parsing - L = left, R = right
        direction = 'R'
        row = 0
        column = 0

        while row >= 0 and row < bitmap_height and column >= 0 and column < bitmap_width:
            brainfuck_code = (65536 * bitmap[row][column][0] + 256 * bitmap[row][column][1] + bitmap[row][column][2]) % 11

            if brainfuck_code == 0:
                self.data += '>'

            if brainfuck_code == 1:
                self.data += '<'

            if brainfuck_code == 2:
                self.data += '+'

            if brainfuck_code == 3:
                self.data += '-'

            if brainfuck_code == 4:
                self.data += '.'

            if brainfuck_code == 5:
                self.data += ','

            if brainfuck_code == 6:
                self.data += '['

            if brainfuck_code == 7:
                self.data += ']'

            if brainfuck_code == 8:
                #right rotation
                row += 1
                column = bitmap_width - 1
                direction = 'L'

            if brainfuck_code == 9:
                #left rotation
                row += 1
                column = 0
                direction = 'R'

            if direction == 'R':
                column += 1
            elif direction == 'L':
                column -= 1

        if run:
            self.program = BrainFuck(self.data)

class WhichBrainxPic():
    def __init__(self, src):
        self.format = ""

        brainloller_instructions = [(255, 0, 0), (128, 0, 0), (0, 255, 0), (0, 128, 0), (0, 0, 255), (0, 0, 128), (255, 255, 0), (128, 128, 0)]
        bitmap = image_png.PngReader(src).rgb
        width = len(bitmap[0])

        instruction_match_counter = 0
        max_check_iterator = 0

        for pixel in bitmap[0]:
            if pixel in brainloller_instructions:
                instruction_match_counter += 1
            
            max_check_iterator += 1

        if instruction_match_counter >= (max_check_iterator / 2):
            self.format = "bl"
        else:
            self.format = "bc"

if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="source code or file with source code")
    arg = parser.parse_args()

    if os.path.isfile(arg.src):
        if arg.src[-4:] == ".txt" or arg.src[-2:] == ".b":
            with open(arg.src, "r", encoding="ascii") as f:
                lines = f.readlines()

            brainfuck_code = ""

            for line in lines:
                brainfuck_code += line

            BrainFuck(brainfuck_code)
        elif arg.src[-4:] == ".png":
            format = WhichBrainxPic(arg.src).format

            if format == "bl":
                BrainLoller(arg.src)
            else:
                BrainCopter(arg.src)
        else:
            print("src: unknown source file")
    else:
        BrainFuck(arg.src)


