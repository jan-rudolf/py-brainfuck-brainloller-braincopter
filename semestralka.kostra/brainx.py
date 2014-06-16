#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BrainFuck:
    """Interpretr jazyka brainfuck."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Inicializace interpretru brainfucku."""
        
        # data programu
        self.data = data
        instruction_pointer = 0
        
        # inicializace proměnných
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer
        
        # DEBUG a testy
        # a) paměť výstupu
        self.output = ''

        while instruction_pointer < len(self.data):
            instruction = self.data[instruction_pointer]
            #print(instruction)

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
                continue

            if instruction == ',':
                instruction_pointer += 1
                try:
                    self.memory[self.memory_pointer] = ord(input_stream.pop(0))
                except:
                    pass
                continue

            if instruction == '[' and self.memory[self.memory_pointer] == 0:
                while self.data[instruction_pointer] != ']':
                    instruction_pointer += 1
                instruction_pointer += 1
                continue

            if instruction == ']' and self.memory[self.memory_pointer] != 0:
                while self.data[instruction_pointer] != '[':
                    instruction_pointer = 0 if instruction_pointer == 0 else instruction_pointer - 1
                instruction_pointer += 1
                continue
            else:
                instruction_pointer += 1
                continue
    
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
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""
    
    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


