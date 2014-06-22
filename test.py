#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pngdecoder
import pngencoder
import brainloller
import braincopter
import brainfuck



#bitmap, width, height = brainroller.Brainroller().fromBrainfuckToBitmap(">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.")

#png = pngencoder.PNGEncoder(width, height)
#png.encode(bitmap)

"""
png = pngdecoder.PNGDecoder("images/HelloWorld_braincopter.png")

brainfuck_code = braincopter.BrainCopter().fromBitmaptoBrainFuck(png.bitmap)

hello = ">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+."

print(brainfuck_code)

if hello == brainfuck_code:
	print("MATH!")
else: 
	print("NOT MATCH!")
"""

brainfuck_code = ""

with open("source/squares.txt", "r", encoding = "ascii") as f:
	lines = f.readlines()

for line in lines:
	brainfuck_code += line

program = brainfuck.BrainFuck(",>,< [ > [ >+ >+ << -] >> [- << + >>] <<< -] >>")

print("")

program.print_debug()
