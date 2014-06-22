#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

class BrainLoller:
	def __init__(self):
		self.brainfuck = ""
		self.bitmap = list()
		self.bitmap_width = 0
		self.bitmap_height = 0

	def fromBitmaptoBrainFuck(self, bitmap):
		self.bitmap = bitmap
		self.bitmap_width = len(bitmap[0])
		self.bitmap_height = len(bitmap)

		#print("bitmapa: sirka {} vyska {}".format(self.bitmap_width, self.bitmap_height))

		direction = 'R' #smer zpracovani do prava - R, smer do leva - L
		row = 0
		column = 0

		while row >= 0 and row < self.bitmap_height and column >= 0 and column < self.bitmap_width:
			#print("row {} column {}".format(row, column))

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
				column = self.bitmap_width - 1
				direction = 'L'
				#print("rotace do leva row {} column {}".format(row, column))

			if (self.bitmap_height == row or self.bitmap_width == column):
					break

			if self.bitmap[row][column][0] == 0 and self.bitmap[row][column][1] == 128 and self.bitmap[row][column][2] == 128:
				#rotace doprava
				row += 1
				column = 0
				direction = 'R'
				#print("rotace do prava row {} column {}".format(row, column))

			if direction == 'R':
				column += 1
			elif direction == 'L':
				column -= 1

		return self.brainfuck

	def fromBrainFuckToBitmap(self, brainfuck_code): 
		self.brainfuck = brainfuck_code

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
					row.insert(0, pixel)
				else:
					row.insert(0, [0, 128, 128])
					bitmap.append(row)

					direction = 'R'

					row = list()

					row.append([0, 128, 128])
					row.append(pixel)

		#padding
		padding = width - len(row)

		for i in range(padding):
			if direction == 'R':
				row.append([123, 123, 123]) #vloz balast na doplneni mezery
			else:
				row.insert(0, [123, 123, 123])

		bitmap.append(row)

		height = len(bitmap)

		return (bitmap, width, height)











