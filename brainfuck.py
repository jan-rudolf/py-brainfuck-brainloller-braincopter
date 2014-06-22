#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

class BrainFuck:
    """Interpretr jazyka brainfuck."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Inicializace interpretru brainfucku."""
        
        # data programu
        self.data = data
        self.instruction_pointer = 0
        
        # inicializace proměnných
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer
        
        # DEBUG a testy
        # a) paměť výstupu
        self.output = ''

        while self.instruction_pointer < len(self.data):
            instruction = self.data[self.instruction_pointer]

            if instruction == '>':
                self.instruction_pointer += 1

                self.memory_pointer += 1

                if(len(self.memory) == self.memory_pointer):
                    self.memory.append(0)
                continue

            if instruction == '<':
                self.instruction_pointer += 1
                self.memory_pointer =  0 if self.memory_pointer == 0 else self.memory_pointer - 1
                continue

            if instruction == '+':
                self.instruction_pointer += 1
                self.memory[self.memory_pointer] = (self.memory[self.memory_pointer] + 1) % 256
                continue

            if instruction == '-':
                self.instruction_pointer += 1
                self.memory[self.memory_pointer] = 255 if self.memory[self.memory_pointer] == 0 else self.memory[self.memory_pointer] - 1
                continue

            if instruction == '.':
                self.instruction_pointer += 1
                #self.output += chr(self.memory[self.memory_pointer])
                print(chr(self.memory[self.memory_pointer]), end="")
                continue

            if instruction == ',':
                self.instruction_pointer += 1
                try:
                    input_str = input()
                    self.memory[self.memory_pointer] = ord(input_str[0])
                except:
                    pass
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

            self.instruction_pointer += 1
    
    #
    # pro potřeby testů
    #
    def get_memory(self):
        return bytes(self.memory)

    def print_debug(self):
        print("Instruction pointer: {}".format(self.instruction_pointer))
        print("Memory pointer: {}".format(self.memory_pointer))
        print("Memory:")
        print(self.get_memory())