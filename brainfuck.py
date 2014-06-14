"""
Brainfuck interpreter
---------------------
Author: Jan Rudolf
4.3.2013 23:43
"""

source_code = "+++[--]>+"

input_stream = list("AHOJ")
output_stream = list()

data_pointer = 0
instruction_pointer = 0

memory = [ 0 for x in range(10) ]

while instruction_pointer < len(source_code):
	instruction = source_code[instruction_pointer]
	instruction_pointer += 1

	if instruction == '>':
		data_pointer = 255 if data_pointer == 255 else data_pointer + 1

	if instruction == '<':
		data_pointer =  0 if data_pointer == 0 else data_pointer - 1

	if instruction == '+':
		memory[data_pointer] = (memory[data_pointer] + 1) % 255

	if instruction == '-':
		memory[data_pointer] = 0 if memory[data_pointer] == 0 else memory[data_pointer] - 1

	if instruction == '.':
		output_stream.append(chr(memory[data_pointer]))

	if instruction == ',':
		try:
			memory[data_pointer] = ord(input_stream.pop(0))
		except:
			pass

	if instruction == '[' and memory[data_pointer] == 0:
		while source_code[instruction_pointer] != ']':
			instruction_pointer += 1
		instruction_pointer += 1

	if instruction == ']' and memory[data_pointer] != 0:
		while source_code[instruction_pointer] != '[':
			instruction_pointer -= 1
		instruction_pointer += 1



print("Paměť:")

for memory_cell in memory:
	print(" {0} ".format(memory_cell), end = '')

print()

print("Výstup:")

for output_element in output_stream:
	print(output_element, end = '')

print()