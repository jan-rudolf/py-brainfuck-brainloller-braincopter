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
    """Testing behavior of the Brainfuck interpreter."""
    
    def setUp(self):
        self.BF = brainx.Brainfuck
        #hide stdout
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
   
    def test_bf_01(self):
        """Null actual memory cell."""
        program = self.BF('[-]', memory=b'\x03\x02', memory_pointer=1)
        self.assertEqual(program.get_memory(), b'\x03\x00')
    
    def test_bf_02(self):
        """Null each memory cell from actual to the left."""
        program = self.BF('[[-]<]', memory=b'\x03\x03\x00\x02\x02', memory_pointer=4)
        self.assertEqual(program.get_memory(), b'\x03\x03\x00\x00\x00')
    
    def test_bf_03(self):
        """Move to the first not null memory cell on left."""
        program = self.BF('[<]', memory=b'\x03\x03\x00\x02\x02', memory_pointer=4)
        self.assertEqual(program.memory_pointer, 2)
    
    def test_bf_04(self):
        """Move to the first not null memory cell on right."""
        program = self.BF('[>]', memory=b'\x03\x03\x00\x02\x02')
        self.assertEqual(program.memory_pointer, 2)
    
    def test_bf_05(self):
        """Destructive addition of the actual memory cell to the next one."""
        program = self.BF('[>+<-]', memory=b'\x03\x03')
        self.assertEqual(program.get_memory(), b'\x00\x06')
    
    def test_bf_06(self):
        """Nondestructive addition of actual memory cell to the next one."""
        program = self.BF('[>+>+<<-]>>[<<+>>-]', memory=b'\x03\x03')
        self.assertEqual(program.get_memory(), b'\x03\x06\x00')
    
    def test_bf_07(self):
        """Destructive subtraction of the actual memory cell from the next one."""
        program = self.BF('[>-<-]', memory=b'\x03\x05')
        self.assertEqual(program.get_memory(), b'\x00\x02')
    
    def test_bf_11(self):
        r"""HelloWorld with \n."""
        with open('test_data/hello1.b', encoding='ascii' ) as stream:
            data = stream.read()
        program = self.BF(data)
        self.assertEqual(program.output, 'Hello World!\n')
    
    def test_bf_12(self):
        r"""HelloWorld without \n."""
        with open( 'test_data/hello2.b', encoding='ascii' ) as stream:
            data = stream.read()
        program = self.BF(data)
        self.assertEqual(program.output, 'Hello World!')


class TestBrainfuckWithInput(unittest.TestCase):
    """Testing behavior of the Brainfuck interpreter for programs with an input."""
    
    def setUp(self):
        self.BF = brainx.Brainfuck
        # hide stdout
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
    
    def test_bf_input_2(self):
        """numwarp.b for input '123'."""
        with open('test_data/numwarp_input.b', encoding='ascii') as stream:
            data = stream.read()
        
        program = self.BF(data)
        self.assertEqual(program.output, '    /\\\n     /\\\n  /\\  /\n   / \n \\ \\/\n  \\\n   \n')


class TestPNG(unittest.TestCase):
    """Testing of correct loading of a subset of PNG images."""
    
    def setUp(self):
        self.png = image_png.PNGReader
        # hide stdout
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
    
    def test_png_01(self):
        """We can do only PNG test."""
        self.assertRaises(image_png.PNGWrongHeaderError, self.png, 'test_data/sachovnice.jpg')
    
    def test_png_02(self):
        """We can do only some PNGs test."""
        self.assertRaises(image_png.PNGNotImplementedError, self.png, 'test_data/sachovnice_paleta.png')
    
    def test_png_03(self):
        """Loading of a simple PNG image test."""
        image = self.png('test_data/sachovnice.png')
        self.assertEqual(image.rgb,
                         [
                             [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
                             [(255, 255, 255), (127, 127, 127), (0, 0, 0)],
                             [(255, 255, 0), (255, 0, 255), (0, 255, 255)]
                         ])


class TestBrainloller(unittest.TestCase):
    """Testing behavior of the Brainloller interpreter."""
    
    def setUp(self):
        self.BF = brainx.Brainfuck
        self.BL = brainx.Brainloller
        # hide stdout
        self.out = sys.stdout
        sys.stdout = FakeStdOut()
    
    def tearDown(self):
        sys.stdout = self.out
    
    def test_bl_1a(self):
        """Loading of data from HelloWorld.png."""
        bl = self.BL('test_data/HelloWorld.png')
        self.assertEqual(
            bl.brainfuck_source_code,
            '>+++++++++[<++++++++>-]<.>+++++++[<++++>'
            '-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>'
            '>>++++++++++[<+++++++++>-]<---.<<<<.+++.--'
            '----.--------.>>+.'
        )
    
    def test_bl_1b(self):
        """Run program from HelloWorld.png."""
        bl = self.BL('test_data/HelloWorld.png')
        self.assertEqual(bl.program.output, 'Hello World!')


#
# ensure to be able to run the script from command line
#

if __name__ == '__main__':
    unittest.main()
