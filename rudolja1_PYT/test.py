#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import unittest

import brainx
import image_png


class FakeStdOut:
    def write(self, *args, **kwargs):
        pass

    def flush(self):
        pass


#
# Classes for testing
#

class TestBrainfuck(unittest.TestCase):
    """testing behavior of Brainfuck interpreter"""
    
    def setUp(self):
        self.BF = brainx.BrainFuck
        #hide stdout
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
   
    def test_bf_01(self):
        """null actual memory cell"""
        program = self.BF('[-]', memory=b'\x03\x02', memory_pointer=1)
        self.assertEqual(program.get_memory(), b'\x03\x00')
    
    def test_bf_02(self):
        """null each memory cell from actual to the left"""
        program = self.BF('[[-]<]', memory=b'\x03\x03\x00\x02\x02', memory_pointer=4)
        self.assertEqual(program.get_memory(), b'\x03\x03\x00\x00\x00')
    
    def test_bf_03(self):
        """move to the first not null memory cell on left"""
        program = self.BF('[<]', memory=b'\x03\x03\x00\x02\x02', memory_pointer=4)
        self.assertEqual(program.memory_pointer, 2)
    
    def test_bf_04(self):
        """move to the first not null memory cell on right"""
        program = self.BF('[>]', memory=b'\x03\x03\x00\x02\x02')
        self.assertEqual(program.memory_pointer, 2)
    
    def test_bf_05(self):
        """destructive addition of the actual memory cell to the next one"""
        program = self.BF('[>+<-]', memory=b'\x03\x03')
        self.assertEqual(program.get_memory(), b'\x00\x06')
    
    def test_bf_06(self):
        """nondestructive addition of actual memory cell to the next one"""
        program = self.BF('[>+>+<<-]>>[<<+>>-]', memory=b'\x03\x03')
        self.assertEqual(program.get_memory(), b'\x03\x06\x00')
    
    def test_bf_07(self):
        """destructive subtraction of the actual memory cell from the next one"""
        program = self.BF('[>-<-]', memory=b'\x03\x05')
        self.assertEqual(program.get_memory(), b'\x00\x02')
    
    def test_bf_11(self):
        r"""HelloWorld with \n"""
        with open( 'test_data/hello1.b', encoding='ascii' ) as stream:
            data = stream.read()
        program = self.BF(data)
        self.assertEqual(program.output, 'Hello World!\n')
    
    def test_bf_12(self):
        r"""HelloWorld without \n"""
        with open( 'test_data/hello2.b', encoding='ascii' ) as stream:
            data = stream.read()
        program = self.BF(data)
        self.assertEqual(program.output, 'Hello World!')


class TestBrainfuckWithInput(unittest.TestCase):
    """testing of behavior of Brainfuck interpreter for programs with an input"""
    
    def setUp(self):
        self.BF = brainx.BrainFuck
        # hide stdout
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
    
    def test_bf_input_2(self):
        """numwarp.b for input '123'"""
        with open('test_data/numwarp_input.b', encoding='ascii') as stream:
            data = stream.read()
        
        program = self.BF(data)
        self.assertEqual(program.output, '    /\\\n     /\\\n  /\\  /\n   / \n \\ \\/\n  \\\n   \n')


class TestPNG(unittest.TestCase):
    """testing of correct loading of a subset of PNG images"""
    
    def setUp(self):
        self.png = image_png.PngReader
        # hide stdout
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
    
    def test_png_01(self):
        """we can do only PNG"""
        self.assertRaises(image_png.PNGWrongHeaderError, self.png, 'test_data/sachovnice.jpg')
    
    def test_png_02(self):
        """we can do only some PNGs"""
        self.assertRaises(image_png.PNGNotImplementedError, self.png, 'test_data/sachovnice_paleta.png')
    
    def test_png_03(self):
        """loading of simple PNG image"""
        image = self.png('test_data/sachovnice.png')
        self.assertEqual(image.rgb,
                         [
                             [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
                             [(255, 255, 255), (127, 127, 127), (0, 0, 0)],
                             [(255, 255, 0), (255, 0, 255), (0, 255, 255)]
                         ])


class TestBrainloller(unittest.TestCase):
    """testing behavior of Brainloller interpret"""
    
    def setUp(self):
        self.BF = brainx.BrainFuck
        self.BL = brainx.BrainLoller
        # hide stdout
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
    
    def test_bl_1a(self):
        """loading of data from HelloWorld.png"""
        objekt = self.BL('test_data/HelloWorld.png')
        self.assertEqual(
            objekt.data,
            '>+++++++++[<++++++++>-]<.>+++++++[<++++>'
            '-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>'
            '>>++++++++++[<+++++++++>-]<---.<<<<.+++.--'
            '----.--------.>>+.'
        )
    
    def test_bl_1b(self):
        """run program from HelloWorld.png"""
        objekt = self.BL('test_data/HelloWorld.png')
        self.assertEqual(objekt.program.output, 'Hello World!')


#
# ensure to be able to run the script from command line
#
if __name__ == '__main__':
    unittest.main()
