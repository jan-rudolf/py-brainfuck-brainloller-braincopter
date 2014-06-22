#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zlib

class PNGEncoder():

	def __init__(self, width, height):
		self.settings = {"width": width, "height": height, "bit_depth": 8, "colour_type": 2, "compression_method": 0, "filter_method": 0, "interlace_method": 0}
		self.bitmap_in_png = list() 
		self.IDAT = b''
		self.IHDR = b'IHDR' + width.to_bytes(4, 'big') + height.to_bytes(4, 'big') + bit_depth.to_bytes(1, 'big') + colour_type.to_bytes(1, 'big') + compression_method.to_bytes(1, 'big') + filter_method.to_bytes(1, 'big') + interlace_method.to_bytes(1, 'big')
		self.IHDR = b'\x00\x00\x00\r' + self.IHDR + zlib.crc32(self.IHDR).to_bytes(4, 'big')
		self.IEND = b'\x00\x00\x00\x00' + b'IEND' + b'' +  b'\xaeB`\x82'

	def encode(self, pixels, output_file = ""):
		"""
		Parameters:
			self <class>  - instance of the class
			pixels <list> - encoded Brainroller into pixels 
			output_file <string> - output file, if is desired
		Returns: <bytes> bytes of encoded png file
		"""
		#adding info about fitration method
		for row in pixels:
			self.bitmap_in_png.append([self.settings["filter_method"], row])

		#converting list into bytes
		for row in self.bitmap_in_png:
			self.IDAT += row[0].to_bytes(1, 'big')

			for pixel in row[1]:
				self.IDAT += pixel[0].to_bytes(1, 'big')
				self.IDAT += pixel[1].to_bytes(1, 'big')
				self.IDAT += pixel[2].to_bytes(1, 'big')

		compressed_data = zlib.compress(self.IDAT)

		self.IDAT = len(compressed_data).to_bytes(4, 'big') + b'IDAT' + compressed_data + zlib.crc32(b'IDAT' + compressed_data).to_bytes(4, 'big')

		png_header = b'\x89PNG\r\n\x1a\n'
		png = png_header + self.IHDR + self.IDAT + self.IEND

		if len(output_file):
			with open(output_file, "wb") as f:
				f.write(png)

		return png
	


