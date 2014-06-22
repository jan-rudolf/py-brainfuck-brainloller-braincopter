#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

class BrainCopter:
	def __init__(self):
		self.brainfuck = ""
		self.bitmap = list()
		self.bitmap_width = 0
		self.bitmap_height = 0
		self.transition_table = {'>': 0, '<': 1, '+': 2, '-': 3, '.' : 4, ',' : 5, '[': 6, ']': 7, 'L': 8, 'R': 9}

	def BFpixelEncode (value, pixel):
		r = pixel[0]
		g = pixel[1]
		b = pixel[2]

		while (((65536 * r + 256 * g + b) % 11) != value):
			r += 1
			g += 1
			b += 1

		return [r, g, b]

	def fromBitmaptoBrainFuck(self, bitmap):
		self.bitmap = bitmap
		self.bitmap_width = len(bitmap[0])
		self.bitmap_height = len(bitmap)
		self.brainfuck = ""

		direction = 'R' #smer zpracovani do prava - R, smer do leva - L
		row = 0
		column = 0

		while row >= 0 and row < self.bitmap_height and column >= 0 and column < self.bitmap_width:
			brainfuck_code = (65536 * self.bitmap[row][column][0] + 256 * self.bitmap[row][column][1] + self.bitmap[row][column][2]) % 11 
			if brainfuck_code == 0:
				self.brainfuck += '>'

			if brainfuck_code == 1:
				self.brainfuck += '<'

			if brainfuck_code == 2:
				self.brainfuck += '+'

			if brainfuck_code == 3:
				self.brainfuck += '-'

			if brainfuck_code == 4:
				self.brainfuck += '.'

			if brainfuck_code == 5:
				self.brainfuck += ','

			if brainfuck_code == 6:
				self.brainfuck += '['

			if brainfuck_code == 7:
				self.brainfuck += ']'

			if brainfuck_code == 8:
				#rotace doleva
				row += 1
				column = self.bitmap_width - 1
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

		return self.brainfuck

	def fromBrainFuckToBitmap(self, bitmap, brainfuck_code): 
		self.brainfuck = brainfuck_code
		self.bitmap_width = len(bitmap[0])
		self.bitmap_height = len(bitmap)

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















