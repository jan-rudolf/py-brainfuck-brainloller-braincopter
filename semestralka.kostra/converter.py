import os
import argparse
import math

import brainx
import image_png

class BrainFuck2BrainLoller():
	def __init__(self, brainfuck_code):
		brainfuck = brainfuck_code

		data = list()
		width = math.ceil(math.sqrt(len(brainfuck))) #aby bylo obrazek ctvercovy

		for prikaz in brainfuck:
			if prikaz == '>':
				data.append([255, 0, 0])

			if prikaz == '<':
				data.append([128, 0, 0])

			if prikaz == '+':
				data.append([0, 255, 0])

			if prikaz == '-':
				data.append([0, 128, 0])

			if prikaz == '.':
				data.append([0, 0, 255])

			if prikaz == ',':
				data.append([0, 0, 128])

			if prikaz == '[':
				data.append([255, 255, 0])

			if prikaz == ']':
				data.append([128, 128, 0])

		rows = 0
		columns = 0

		row = list()
		row_counter = 0
		self.bitmap = list()

		direction = 'R'

		for pixel in data:
			if ((len(row) + 1) < width):
				if direction == 'R':
					row.append(pixel)
				else:
					row.insert(0, pixel)
			elif ((len(row) + 1) == width):
				if direction == 'R':
					row.append([0, 255, 255]) #rotation right
					self.bitmap.append(row)
					
					direction = 'L'

					row = list()
					row.insert(0, [0, 255, 255]) #rotation left
					row.insert(0, pixel)
				else:
					row.insert(0, [0, 128, 128])
					self.bitmap.append(row)

					direction = 'R'

					row = list()

					row.append([0, 128, 128])
					row.append(pixel)

		#padding
		padding = width - len(row)

		for i in range(padding):
			if direction == 'R':
				row.append([123, 123, 123]) #enter padding
			else:
				row.insert(0, [123, 123, 123])

		self.bitmap.append(row)

class BrainFuck2BrainCopter():
	def __init__(self, bitmap, brainfuck_code):
		self.transition_table = {'>': 0, '<': 1, '+': 2, '-': 3, '.' : 4, ',' : 5, '[': 6, ']': 7, 'L': 8, 'R': 9}
		self.brainfuck = brainfuck_code
		self.bitmap_width = len(bitmap[0])
		self.bitmap_height = len(bitmap)

		if len(brainfuck_code) > (self.bitmap_height * self.bitmap_width):
			print("warning: BrainFuck source code is longer than this picture's bitmap, it will not be encoded the whole code")

		row = 0
		column = 0
		direction = 'R'
		brainfuck_counter = 0

		while row >= 0 and row < self.bitmap_height and column >= 0 and column < self.bitmap_width and brainfuck_counter < len(self.brainfuck):
			if((column + 1) == self.bitmap_width or (column == 0 and row > 0)):
				if ((column + 1) == self.bitmap_width):
					braincopter_number = self.transition_table['L']
					old_pixel = bitmap[row][column]
					new_pixel = self.BFpixelEncode(braincopter_number, old_pixel)

				if (column == 0 and row > 0):
					braincopter_number = self.transition_table['R']
					old_pixel = bitmap[row][column]
					new_pixel = self.BFpixelEncode(braincopter_number, old_pixel)

			else:
				braincopter_number = self.transition_table[self.brainfuck[brainfuck_counter]]
				old_pixel = bitmap[row][column]
				new_pixel = self.BFpixelEncode(braincopter_number, old_pixel)

			bitmap[row][column] = new_pixel

			if (braincopter_number == self.transition_table['L']):
				row += 1
				column = self.bitmap_width - 1
			elif (braincopter_number == self.transition_table['R']):
				row += 1
				column = 0
			else:
				if(direction == 'R'):
					column += 1
				else:
					column -= 1

		return bitmap

		def BFpixelEncode (self, value, pixel):
			r = pixel[0]
			g = pixel[1]
			b = pixel[2]

			while (((65536 * r + 256 * g + b) % 11) != value):
				r += 1
				g += 1
				b += 1

		return (r, g, b)



def bf2bl(src, dst):
	with open(src, "r", encoding="ascii") as f:
		lines = f.readlines()

	brainfuck_code = ""

	for line in lines:
		brainfuck_code += line

	bitmap = BrainFuck2BrainLoller(brainfuck_code).bitmap

	image_png.PNGWriter(bitmap, dst)



def bl2bf(src, dst):
	#otestovat existence souboru
	program = brainx.BrainLoller(src, run=False)

	with open(dst, "w", encoding="ascii") as f:
		f.write(program.data)

def bc2bf(src, dst):
	program = brainx.BrainCopter(src, run=False)

	with open(dst, "w", encoding="ascii") as f:
		f.write(program.data)

def bf2bc(src, dst):
	with open(src, "r", encoding="ascii") as f:
		f.readlines()

	brainfuck_code = ""

	for line in lines:
		brainfuck_code += line

	bitmap = image_png.PngReader(dst).rgb

	bitmap = BrainFuck2BrainCopter(bitmap, brainfuck_code)

	image_png.PNGWriter(bitmap, dst)



def bl2bc(src, dst):
	brainfuck_code = brainx.BrainLoller(src, run=False).data

	bitmap = image_png.PngReader(dst).rgb

	bitmap = BrainFuck2BrainCopter(bitmap, brainfuck_code)

	image_png.PNGWriter(bitmap, dst)

def bc2bl(src, dst):
	brainfuck_code = brainx.BrainCopter(src, run=False).data

	bitmap = BrainFuck2BrainLoller(brainfuck_code).bitmap

	image_png.PNGWriter(bitmap, dst)

class WhichBrainxPic():
	def __init__(self, src):
		self.format = ""

		brainloller_instructions = [(255, 0, 0), (128, 0, 0), (0, 255, 0), (0, 128, 0), (0, 0, 255), (0, 0, 128), (255, 255, 0), (128, 128, 0)]
		bitmap = image_png.PngReader(src).rgb
		width = len(bitmap[0])

		instruction_match_counter = 0
		max_check = 2 * width
		max_check_iterator = 0

		for pixel in bitmap:
			if max_check_iterator == max_check:
				break

			if pixel in brainloller_instructions:
				instruction_match_counter += 1
			
			max_check_iterator += 1

		if instruction_match_counter >= (max_check / 2):
			self.format = "bl"
		else:
			self.format = "bc"


if __name__ == "__main__":
	convert_fce = {"bf2bl": bf2bl, "bl2bf": bl2bf, "bc2bf": bc2bf, "bf2bc": bf2bc, "bl2bc": bl2bc, "bc2bl": bc2bl}

	parser = argparse.ArgumentParser()
	parser.add_argument("src", help="path to the source file")
	parser.add_argument("dst", help="path to the destination file")
	arg = parser.parse_args()

	if (arg.src[-4:] == '.png' or arg.src[-4:] == '.txt' or arg.src[-2:] == '.b'):
		if (arg.src[-4:] == '.png'):
			format_from = WhichBrainxPic(src)

		if (arg.src[-4:] == '.txt' or arg.src[-2:] == '.b'):
			format_from = "bf"

	else:
		print("src: unknown source file")

	if (arg.dst[-4:] == '.png' or arg.dst[-4:] == '.txt' or arg.dst[-2:] == '.b'):
		if (arg.dst[-4:] == '.png'):
			if format_from == "bl":
				format_to = "bc"
			else:
				format_to = "bl"

		if (arg.dst[-4:] == '.txt' or arg.dst[-2:] == '.b'):
			format_to = "bf"
	else:
		print("dst: unknown source file")

	conversion = format_from + "2" + format_to

	if conversion in convert_fce:
		print("conversion: {}".format(conversion))
		convert_fce[conversion](arg.src, arg.dst)
	else:
		print("unknown conversion {}".format(conversion)) 

