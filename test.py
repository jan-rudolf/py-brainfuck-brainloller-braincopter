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
	print("Povedlo se vyparsovat")
else:
	print("Nepovedlo se vyparsovat")

bitmap = png.handleRawData()

brainfuck = brainroller.Brainroller().fromBitmaptoBrainfuck(bitmap, width, height)

if (brainfuck == ">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+."):
	print("SHODUJE!")
else:
	print("Neshoduje!")


