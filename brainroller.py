#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

class Brainroller:
	def __init__(self):
		self.brainfuck = ""
		self.bitmap = list()
		self.bitmap_width = 0
		self.bitmap_height = 0

	def fromBitmaptoBrainfuck(self):
		self.bitmap = [[[255, 0, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [255, 255, 0], [128, 0, 0], [0, 255, 0], [0, 255, 255]], [[0, 128, 128], [0, 0, 255], [128, 0, 0], [128, 128, 0], [0, 128, 0], [255, 0, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 255]], [[0, 0, 0], [255, 0, 1], [1, 255, 0], [0, 0, 0], [0, 0, 0], [1, 127, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [129, 1, 0], [128, 255, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [1, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 255], [0, 255, 1], [128, 1, 0], [0, 128, 0], [1, 0, 0], [255, 0, 0], [128, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 255], [0, 0, 0], [0, 0, 0], [128, 255, 0], [0, 0, 0], [0, 1, 255], [0, 0, 1], [255, 1, 0], [0, 0, 0], [1, 255, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [128, 1, 0], [255, 255, 1], [0, 255, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 255, 1], [1, 255, 0], [1, 255, 0], [1, 255, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [127, 0, 0], [1, 129, 0], [128, 0, 0], [0, 128, 0], [128, 0, 255], [255, 0, 1], [0, 0, 0], [0, 0, 0], [1, 255, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [129, 0, 0], [255, 127, 0], [1, 0, 0], [0, 127, 0], [0, 0, 1], [1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [128, 255, 0], [1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 1, 0], [0, 129, 0], [128, 129, 0], [128, 1, 0], [0, 129, 0], [0, 0, 0]], [[0, 0, 0], [0, 1, 255], [0, 255, 1], [0, 0, 0], [0, 0, 0], [0, 1, 255], [128, 0, 1], [0, 0, 0], [129, 0, 0], [128, 128, 0], [128, 0, 255], [0, 128, 1], [0, 0, 0], [0, 0, 0]], [[0, 128, 128], [0, 0, 128], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 128, 255], [0, 128, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 127, 255]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 255], [0, 255, 1], [255, 1, 0], [0, 0, 0], [1, 0, 255], [0, 128, 1], [0, 0, 0], [0, 0, 0], [0, 127, 255]]]
		self.bitmap_width = 14
		self.bitmap_height = 12

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
				#rotace doleva
				row += 1
				direction = 'L'

			if self.bitmap[row][column][0] == 0 and self.bitmap[row][column][1] == 128 and self.bitmap[row][column][2] == 128:
				#rotace doprava
				row += 1
				direction = 'R'

			if direction == 'R':
				column += 1
			elif direction == 'L':
				column -= 1

		print(self.brainfuck)
		print(self.bitmap[2][3])

	def fromBrainfuckToBitmap(self):
		#vysledek ctvercove
		self.brainfuck = ">+++++++++[<++++++++>-"

		data = list()
		width = math.ceil(math.sqrt(len(self.brainfuck))) #aby bylo obrazek ctvercovy

		for prikaz in self.brainfuck:
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
		bitmap = list()

		direction = 'R'

		for pixel in data:
			if ((len(row) + 1) < width):
				if direction == 'R':
					row.append(pixel)
				else:
					row.insert(0, pixel)
			elif ((len(row) + 1) == width):
				if direction == 'R':
					row.append([0, 255, 255]) #rotace doleva
					bitmap.append(row)
					
					direction = 'L'

					row = list()
					row.insert(0, [0, 255, 255]) #rotace doleva
				else:
					row.insert(0, [0, 128, 128])
					bitmap.append(row)

					direction = 'R'

					row = list()

					row.append([0, 128, 128])

		#padding
		padding = width - len(row)

		for i in range(padding):
			if direction == 'R':
				row.append([123, 345, 789]) #vloz balast na doplneni mezery
			else:
				row.insert(0, [123, 345, 789])

		bitmap.append(row)

		#print("Radek:")
		#print(row)
		#print("Bitmapa:")
		#for row in bitmap:
		#	print(row)
		return bitmap











