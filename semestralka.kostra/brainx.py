#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import image_png

class BrainFuck:
    """Interpretr jazyka brainfuck."""
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
        """Inicializace interpretru brainfucku."""
        
        # data programu
        self.data = data
        instruction_pointer = 0
        
        # inicializace proměnných
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer

        #input
        self.input = ''

        self.input_check()
        
        # DEBUG a testy
        # a) paměť výstupu
        self.output = ''

        while instruction_pointer < len(self.data):
            instruction = self.data[instruction_pointer]
            #print(instruction, end="")

            if instruction == '>':
                instruction_pointer += 1

                self.memory_pointer += 1

                if(len(self.memory) == self.memory_pointer):
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
                sys.stdout.write(chr(self.memory[self.memory_pointer]))
                
                continue

            if instruction == ',':
                instruction_pointer += 1
                
                if (len(self.input)):
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
    # pro potřeby testů
    #
    def get_memory(self):
        # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
        return bytes(self.memory)


class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""
    
    def __init__(self, filename):
        """Inicializace interpretru brainlolleru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''

        bitmap = image_png.PngReader(filename).rgb
        bitmap_width = len(bitmap[0])
        bitmap_height = len(bitmap)

        #print("bitmapa: sirka {} vyska {}".format(self.bitmap_width, self.bitmap_height))

        direction = 'R' #smer zpracovani do prava - R, smer do leva - L
        row = 0
        column = 0

        while row >= 0 and row < bitmap_height and column >= 0 and column < bitmap_width:
            #print("row {} column {}".format(row, column))

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
                #rotace doleva
                row += 1
                column = bitmap_width - 1
                direction = 'L'
                #print("rotace do leva row {} column {}".format(row, column))

            if (bitmap_height == row or bitmap_width == column):
                    break

            if bitmap[row][column][0] == 0 and bitmap[row][column][1] == 128 and bitmap[row][column][2] == 128:
                #rotace doprava
                row += 1
                column = 0
                direction = 'R'
                #print("rotace do prava row {} column {}".format(row, column))

            if direction == 'R':
                column += 1
            elif direction == 'L':
                column -= 1

        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""
    
    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''

        print("BrainCopter: PNG načítám data...")
        bitmap = image_png.PngReader(filename).rgb
        print("BrainCopter: Parsuju BrainFuck...")
        bitmap_width = len(bitmap[0])
        bitmap_height = len(bitmap)

        direction = 'R' #smer zpracovani do prava - R, smer do leva - L
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
                #rotace doleva
                row += 1
                column = bitmap_width - 1
                direction = 'L'

            if brainfuck_code == 9:
                #rotace doprava
                row += 1
                column = 0
                direction = 'R'

            if direction == 'R':
                column += 1
            elif direction == 'L':
                column -= 1

        print("BrainCopter: Spoustim...")
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


