#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Brainroller:
	def __init__(self):
		self.brainfuck = ""
		self.bitmap = list()
		self.bitmap_width = 0
		self.bitmap_height = 0

	def toBrainfuck(self):
		self.bitmap = [[[255, 0, 0], [0, 255, 0], [0, 0, 255]], [[255, 255, 255], [127, 127, 127], [0, 0, 0]], [[255, 255, 0], [255, 0, 255], [0, 255, 255]]]
		self.bitmap_width = 3
		self.bitmap_height = 3

		direction = 'R' #smer zpracovani do prava - R, smer do leva - L
		row = 0
		column = 0

		while row >= 0 and row < self.bitmap_height and column >= 0 and column < self.bitmap_width:
			if self.bitmap[row][column][0] == 255 and self.bitmap[row][column][1] == 0 and self.bitmap[row][column][2] == 0:
				self.brainfuck += '>'

			if self.bitmap[row][column][0] == 128 and self.bitmap[row][column][1] == 0 and self.bitmap[row][column][2] == 0:
				self.brainfuck += '<'

			if self.bitmap[row][column][0] == 0 and self.bitmap[row][column][1] == 255 and self.bitmap[row][column][2] == 0:
				self.brainfuck += '+'

			if self.bitmap[row][column][0] == 0 and self.bitmap[row][column][1] == 128 and self.bitmap[row][column][2] == 0:
				self.brainfuck += '-'

			if self.bitmap[row][column][0] == 0 and self.bitmap[row][column][1] == 0 and self.bitmap[row][column][2] == 255:
				self.brainfuck += '.'

			if self.bitmap[row][column][0] == 0 and self.bitmap[row][column][1] == 0 and self.bitmap[row][column][2] == 128:
				self.brainfuck += ','

			if self.bitmap[row][column][0] == 255 and self.bitmap[row][column][1] == 255 and self.bitmap[row][column][2] == 0:
				self.brainfuck += '['

			if self.bitmap[row][column][0] == 128 and self.bitmap[row][column][1] == 128 and self.bitmap[row][column][2] == 0:
				self.brainfuck += ']'

			if self.bitmap[row][column][0] == 0 and self.bitmap[row][column][1] == 255 and self.bitmap[row][column][2] == 255:
				#rotace doprava
				row += 1
				column += 1
				direction = 'R'

			if self.bitmap[row][column][0] == 0 and self.bitmap[row][column][1] == 128 and self.bitmap[row][column][2] == 128:
				#rotace doleva
				row += 1
				column -= 1
				direction = 'L'

			if direction == 'R':
				column += 1
			else:
				column -= 1

		print(self.brainfuck)




