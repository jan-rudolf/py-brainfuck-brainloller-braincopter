#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pngdecoder
import pngencoder
import brainroller



bitmap, width, height = brainroller.Brainroller().fromBrainfuckToBitmap(">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.")

png = pngencoder.PNGEncoder(width, height)
png.encode(bitmap)

png = pngdecoder.PNGDecoder()

if(png.parse("mujobrazek.png")):
	print("PNG file was successfully parsed...")
else:
	print("PNG file could be corrupted. Was not properly parsed. Check errors.")

bitmap = png.handleRawData()

brainfuck = brainroller.Brainroller().fromBitmaptoBrainfuck(bitmap, width, height)

if (brainfuck == ">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+."):
	print("MATCH!")
else:
	print("NOT MATCH!")


