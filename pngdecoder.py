#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import zlib

class PNGDecoder:
	def __init__(self):
		self.file = ""
		self.chunks = list()
		self.rawdata = b""
		self.bitmap = list()
		self.settings = {"width": 0, "height": 0, "bit_depth": 0, "colour_type": 0, "compression_method": 0, "filter_method": 0, "interlace_method": 0}

	def getWidth(self):
		return self.settings["width"]

	def getHeight(self):
		return self.settings["height"]

	def getBitmap(self):
		return self.bitmap

	def handleRawData(self):
		row_counter = 0
		row_size = (self.settings["width"] * 3) + 1 
		row = list()
		pixel = list()
		pixel_counter = 1
		skiped_filter = False

		for byte in self.rawdata:
			if row_counter % row_size == 0:
				if len(row) != 0:
					self.bitmap.append(row)

				row = list()
			else:
				if pixel_counter % 3 == 0:
					pixel.append(byte)
					row.append(pixel)
					pixel = list()
				else:
					pixel.append(byte)

				pixel_counter = pixel_counter + 1

			row_counter = row_counter + 1

		self.bitmap.append(row)

		return self.bitmap


	def parse(self, png_file):
		self.file = png_file

		if os.path.exists(self.file) == False:
			print("error - PNG parse: file {} doesn't exist".format(self.file))
			return False

		with open(self.file, 'rb') as f:
			data = f.read(8)

			#png header test
			if data != b'\x89PNG\r\n\x1a\n':
				print("error - PNG parse: header error, it's not a png file")
				return False

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

				if (chunk_type == b'IDAT'):
					chunk_data = zlib.decompress(chunk_data)

				chunk_crc = int.from_bytes(f.read(4), "big")

				if chunk_crc != zlib.crc32(chunk_type + chunk_data):
					print("error - PNG parse: chunk {},  crc data {} vs. {}".format(chunk_type, chunk_crc, zlib.crc32(chunk_type + chunk_data)))
					return False

				if chunk_type == b"IDAT":
					self.rawdata = self.rawdata + chunk_data
					print("PNG parse: IDAT loaded")
				elif chunk_type == b"IEND":
					self.chunks.append("IEND")
					print("PNG parse: IEND loaded")

					return True 

			return False


