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


	def parse(self, file):
		if os.path.exists(file) == False:
			return False

		self.file = file 

		with open(self.file, 'rb') as f:
			data = f.read(8)

			#header test
			if data != b'\x89PNG\r\n\x1a\n':
				return False

			#
			# Nactu prvni chunk
			#

			#delka datoveho obsahu
			data = f.read(4)
			delka_dat_chunku = int.from_bytes(data, 'big')

			if delka_dat_chunku != 13: #zkontroluje jestli je delka datave casti IHDR 13B
				return False
			#typ chunku
			data = f.read(4)
			typ_chunku = data

			if typ_chunku == b"IHDR":
				self.chunks.append("IHDR")
			else:
				return False
			#data_chunku
			data_chunku = f.read(delka_dat_chunku)

			#crc_chunku
			crc_chunku = int.from_bytes(f.read(4), "big")

			if crc_chunku != zlib.crc32(typ_chunku + data_chunku):
				return False

			self.settings["width"] = int.from_bytes(data_chunku[0:4], "big")
			self.settings["height"] = int.from_bytes(data_chunku[4:8], "big")
			self.settings["bit_depth"] = data_chunku[8]
			self.settings["colour_type"] = data_chunku[9]
			self.settings["compression_method"] = data_chunku[10]
			self.settings["filter_method"] = data_chunku[11]
			self.settings["interlace_method"] = data_chunku[12]

			print("R: precetl jsem hlavicku")

			#####
			# Nactu dalsi chunk
			#####
			while 1:
				#delka datoveho obsah
				data = f.read(4)

				if not data: #pokud v prvnim cteny nejsou zadny data, vyhodi z cyklu, asi bych to mel testovat po kazdym cteni
					break

				delka_dat_chunku = int.from_bytes(data, "big")

				#typ chunku
				data = f.read(4)
				typ_chunku = data

				#data chunku
				data_chunku = f.read(delka_dat_chunku)

				#crc chunku
				crc_chunku = int.from_bytes(f.read(4), "big")

				if crc_chunku != zlib.crc32(typ_chunku + data_chunku):
					return False

				if typ_chunku == b"IDAT":
					self.rawdata = self.rawdata + zlib.decompress(data_chunku)
					print("R: precetl jsem data")
				elif typ_chunku == b"IEND":
					self.chunks.append("IEND")
					print("R: precetl jsem konec")
					break #za predpokladu ze jsem doopravdy na konci souboru

			return True


