#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pngdecoder
import pngencoder
import brainroller



#bitmap, width, height = brainroller.Brainroller().fromBrainfuckToBitmap(">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.")

#png = pngencoder.PNGEncoder(width, height)
#png.encode(bitmap)

png = pngdecoder.PNGDecoder()

if(png.parse("images/HelloWorld.png")):
	print("PNG file was successfully parsed...")
else:
	print("PNG file could be corrupted. Was not properly parsed. Check errors.")

bitmap = png.handleRawData()

#print("-----")
#for row in bitmap:
#	print(row)

brainfuck = brainroller.Brainroller().fromBitmaptoBrainfuck(bitmap, png.getWidth(), png.getHeight())

print(brainfuck)

if (brainfuck == ">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+."):
	print("MATCH!")
else:
	print("NOT MATCH!")


