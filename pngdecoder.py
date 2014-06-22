#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import zlib

class PNGWrongHeaderError(Exception):
    """Výjimka oznamující, že načítaný soubor zřejmě není PNG-obrázkem."""
    pass


class PNGNotImplementedError(Exception):
    """Výjimka oznamující, že PNG-obrázek má strukturu, kterou neumíme zpracovat."""
    pass


class PNGDecoder:
	def __init__(self, filepath):
		self.file = filepath
		self.chunks = list()
		self.rawdata = b""
		self.bitmap = list()
		self.settings = {"width": 0, "height": 0, "bit_depth": 0, "colour_type": 0, "compression_method": 0, "filter_method": 0, "interlace_method": 0}

		self.parse()

		if (self.settings["bit_depth"] != 8 or self.settings["compression_method"] != 0 or self.settings["filter_method"] != 0 or self.settings["interlace_method"] != 0 or self.settings["colour_type"] != 2):
			raise PNGNotImplementedError()

		self.handleRawData()

	def getWidth(self):
		return self.settings["width"]

	def getHeight(self):
		return self.settings["height"]

	def Filter4Paeth(self, a, b, c):
		p = a + b - c
		pa = abs(p - a)
		pb = abs(p - b)
		pc = abs(p - c)

		if pa <= pb and pa <= pc:
			return a
		elif pb <= pc:
			return b
		else:
			return c

	def handleRawData(self):
		row_counter = 0
		row_size = (self.settings["width"] * 3) + 1 
		row = list()
		pixel = list()
		pixel_counter = 1

		for byte in self.rawdata:
			if row_counter % row_size == 0:
				if len(row) != 0:
					self.bitmap.append(row)

				row = list()
				filtration = byte

				if filtration > 4:
					pass #raise exception

			else:
				if pixel_counter % 3 == 0:
					pixel.append(byte)
					#"""
					if filtration == 1:
						a_index = len(row) - 1
						if (a_index < 0):
							a = [0, 0, 0]
						else:
							a = row[a_index]

						pixel[0] = (a[0] + pixel[0]) % 256
						pixel[1] = (a[1] + pixel[1]) % 256
						pixel[2] = (a[2] + pixel[2]) % 256
					elif filtration == 2:
						b_index = len(self.bitmap) - 1
						if (b_index < 0):
							b = [0, 0, 0]
						else:
							b = self.bitmap[b_index][len(row)]

						pixel[0] = (b[0] + pixel[0]) % 256
						pixel[1] = (b[1] + pixel[1]) % 256
						pixel[2] = (b[2] + pixel[2]) % 256
					elif filtration == 3:
						a_index = len(row) - 1
						if (a_index < 0):
							a = [0, 0, 0]
						else:
							a = row[a_index]

						b_index = len(self.bitmap) - 1
						if (b_index < 0):
							b = [0, 0, 0]
						else:
							b = self.bitmap[b_index][len(row)]

						pixel[0] = (pixel[0] + (a[0] + b[0]) // 2) % 256
						pixel[1] = (pixel[1] + (a[1] + b[1]) // 2) % 256
						pixel[2] = (pixel[2] + (a[2] + b[2]) // 2) % 256
					elif filtration == 4:
						a_index = len(row) - 1
						if (a_index < 0):
							a = [0, 0, 0]
						else:
							a = row[a_index]

						b_index = len(self.bitmap) - 1
						if (b_index < 0):
							b = [0, 0, 0]
						else:
							b = self.bitmap[b_index][len(row)]

						c_index = [len(self.bitmap) - 1, len(row) - 1]
						if (c_index[0] < 0 or c_index[1] < 0):
							c = [0, 0, 0]
						else:
							c = self.bitmap[c_index[0]][c_index[1]]

						p = [self.Filter4Paeth(a[0], b[0], c[0]), self.Filter4Paeth(a[1], b[1], c[1]), self.Filter4Paeth(a[2], b[2], c[2])]

						pixel[0] = (p[0] + pixel[0]) % 256
						pixel[1] = (p[1] + pixel[1]) % 256
						pixel[2] = (p[2] + pixel[2]) % 256
					#"""
					row.append(pixel)

					pixel = list()
				else:
					pixel.append(byte)

				pixel_counter += 1

			row_counter += 1

		self.bitmap.append(row)

		return self.bitmap


	def parse(self):
		if os.path.exists(self.file) == False:
			print("error - PNG parse: file {} doesn't exist".format(self.file))
			return False

		with open(self.file, 'rb') as f:
			data = f.read(8)

			#png header test
			if data != b'\x89PNG\r\n\x1a\n':
				raise PNGWrongHeaderError()

			#IHDR
			bytes = f.read(4) #lenght
			chunk_data_length = int.from_bytes(bytes, 'big')

			if chunk_data_length != 13: #if it's not 13 bytes, it's not the IHDR chunk or a valid IHDR chunk
				print("error - PNG parse: not valid IHDR chunk, the size is not 13 bytes")
				return False

			chunk_type = f.read(4)
	
			if chunk_type == b"IHDR":
				self.chunks.append("IHDR")
			else:
				print("error - PNG parse: IHDR chunk type")
				return False
	
			chunk_data = f.read(chunk_data_length)
			chunk_crc = int.from_bytes(f.read(4), "big")

			if chunk_crc != zlib.crc32(chunk_type + chunk_data):
				print("error - PNG parse: crc")
				return False

			self.settings["width"] = int.from_bytes(chunk_data[0:4], "big")
			self.settings["height"] = int.from_bytes(chunk_data[4:8], "big")
			self.settings["bit_depth"] = chunk_data[8]
			self.settings["colour_type"] = chunk_data[9]
			self.settings["compression_method"] = chunk_data[10]
			self.settings["filter_method"] = chunk_data[11]
			self.settings["interlace_method"] = chunk_data[12]

			print("PNG parse: IHDR loaded")

			#reading other chunks
			while 1:
				bytes = f.read(4)

				if not bytes: #pokud v prvnim cteny nejsou zadny data, vyhodi z cyklu, asi bych to mel testovat po kazdym cteni
					break

				chunk_data_length = int.from_bytes(bytes, "big")
				chunk_type = f.read(4)
				chunk_data = f.read(chunk_data_length)
				chunk_crc = int.from_bytes(f.read(4), "big")

				if chunk_crc != zlib.crc32(chunk_type + chunk_data):
					print("error - PNG parse: chunk {},  crc data {} vs. {}".format(chunk_type, chunk_crc, zlib.crc32(chunk_type + chunk_data)))
					return False

				if chunk_type == b"IDAT":
					self.rawdata = self.rawdata + chunk_data
					print("PNG parse: IDAT loaded")
				elif chunk_type == b"IEND":
					self.chunks.append("IEND")
					self.rawdata = zlib.decompress(self.rawdata)
					print("PNG parse: IEND loaded")

					return True 

			return False


