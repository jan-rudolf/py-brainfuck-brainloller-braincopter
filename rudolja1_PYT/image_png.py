#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zlib

#
# Exceptions
#


class PNGWrongHeaderError(Exception):
    """Exception - loaded file is not probably PNG image."""
    pass


class PNGNotImplementedError(Exception):
    """Exception - PNG structure we cannot handle."""
    pass


class PNGReadingError(Exception):
    """Exception - error reading data."""
    pass


class PNGFilterError(Exception):
    """Exception - error parsing data."""
    pass

#
# Classes
#

class PNGReader():
    """Class to transform raw bytes of the PNG image into a list of pixels."""
    
    def __init__(self, filepath):
        # image RGB data is list of list of lines
        # every pixel on the list is a triple (R, G, B)
        self.rgb = []

        # settings of the image
        self.settings = dict()

        # image rawdata
        self.rawdata = b''

        with open(filepath, "rb") as f:
            data = f.read(8)

            # PNG header test
            if data != b'\x89PNG\r\n\x1a\n':
                raise PNGWrongHeaderError()

            # get IHDR
            bytes_ = f.read(4)

            chunk_data_length = int.from_bytes(bytes_, 'big')

            if chunk_data_length != 13:
                # if it's not 13 bytes, it's not the IHDR chunk or a valid IHDR chunk
                raise PNGReadingError()

            chunk_type = f.read(4)
    
            if chunk_type != b"IHDR":
                raise PNGReadingError("did not find IHDR")
    
            chunk_data = f.read(chunk_data_length)

            chunk_crc = int.from_bytes(f.read(4), "big")

            if chunk_crc != zlib.crc32(chunk_type + chunk_data):
                raise PNGReadingError()

            self.settings["width"] = int.from_bytes(chunk_data[0:4], "big")
            self.settings["height"] = int.from_bytes(chunk_data[4:8], "big")
            self.settings["bit_depth"] = chunk_data[8]
            self.settings["colour_type"] = chunk_data[9]
            self.settings["compression_method"] = chunk_data[10]
            self.settings["filter_method"] = chunk_data[11]
            self.settings["interlace_method"] = chunk_data[12]

            if (
                self.settings["bit_depth"] != 8 or
                self.settings["colour_type"] != 2 or
                self.settings["compression_method"] != 0 or
                self.settings["filter_method"] != 0 or
                self.settings["interlace_method"] != 0
            ):
                raise PNGNotImplementedError()

            while 1:
                # reading other chunks
                bytes_ = f.read(4)

                if not bytes_:
                    break

                chunk_data_length = int.from_bytes(bytes_, "big")
                chunk_type = f.read(4)
                chunk_data = f.read(chunk_data_length)
                chunk_crc = int.from_bytes(f.read(4), "big")

                if chunk_crc != zlib.crc32(chunk_type + chunk_data):
                    raise PNGReadingError("check sum does not match")

                if chunk_type == b"IDAT":
                    self.rawdata += chunk_data

                elif chunk_type == b"IEND":
                    self.rawdata = zlib.decompress(self.rawdata)

            self.rgb = self.handle_raw_data()

    def filter_4_paeth(self, a, b, c):
        """The Paeth PNG filter (http://www.w3.org/TR/PNG-Filters.html)."""
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

    def handle_raw_data(self):
        bitmap = list()

        # list of rows
        row = list()
        row_counter = 0
        row_size = (self.settings["width"] * 3) + 1

        # list of pixels
        pixel = list()
        pixel_counter = 1

        # type of the filter
        # https://www.w3.org/TR/PNG-Filters.html
        filter_ = 0

        for byte in self.rawdata:
            if row_counter % row_size == 0:
                if len(row) != 0:
                    bitmap.append(row)

                row = list()

                filter_ = byte

            else:
                if pixel_counter % 3 == 0:

                    pixel.append(byte)
                
                    if filter_ == 1:
                        # filter type: Sub
                        a_index = len(row) - 1
                        if a_index < 0:
                            a = [0, 0, 0]
                        else:
                            a = row[a_index]

                        pixel[0] = (a[0] + pixel[0]) % 256
                        pixel[1] = (a[1] + pixel[1]) % 256
                        pixel[2] = (a[2] + pixel[2]) % 256

                    elif filter_ == 2:
                        # filter type: Up
                        b_index = len(bitmap) - 1
                        if b_index < 0:
                            b = [0, 0, 0]
                        else:
                            b = bitmap[b_index][len(row)]

                        pixel[0] = (b[0] + pixel[0]) % 256
                        pixel[1] = (b[1] + pixel[1]) % 256
                        pixel[2] = (b[2] + pixel[2]) % 256
                    elif filter_ == 3:
                        # filter type: Average
                        a_index = len(row) - 1
                        if a_index < 0:
                            a = [0, 0, 0]
                        else:
                            a = row[a_index]

                        b_index = len(bitmap) - 1
                        if b_index < 0:
                            b = [0, 0, 0]
                        else:
                            b = bitmap[b_index][len(row)]

                        pixel[0] = (pixel[0] + (a[0] + b[0]) // 2) % 256
                        pixel[1] = (pixel[1] + (a[1] + b[1]) // 2) % 256
                        pixel[2] = (pixel[2] + (a[2] + b[2]) // 2) % 256
                    elif filter_ == 4:
                        # filter type: Paeth
                        a_index = len(row) - 1
                        if a_index < 0:
                            a = [0, 0, 0]
                        else:
                            a = row[a_index]

                        b_index = len(bitmap) - 1
                        if b_index < 0:
                            b = [0, 0, 0]
                        else:
                            b = bitmap[b_index][len(row)]

                        c_index = [len(bitmap) - 1, len(row) - 1]
                        if c_index[0] < 0 or c_index[1] < 0:
                            c = [0, 0, 0]
                        else:
                            c = bitmap[c_index[0]][c_index[1]]

                        p = [
                            self.filter_4_paeth(a[0], b[0], c[0]),
                            self.filter_4_paeth(a[1], b[1], c[1]),
                            self.filter_4_paeth(a[2], b[2], c[2])
                        ]

                        pixel[0] = (p[0] + pixel[0]) % 256
                        pixel[1] = (p[1] + pixel[1]) % 256
                        pixel[2] = (p[2] + pixel[2]) % 256
                    
                    row.append(tuple(pixel))

                    pixel = list()

                else:
                    pixel.append(byte)

                pixel_counter += 1

            row_counter += 1

        if len(row) != 0:
            bitmap.append(row)

        return bitmap


class PNGWriter():
    """Class to construct a PNG image from a list of pixels."""
    def __init__(self, bitmap, output_file):
        width = len(bitmap[0])
        height = len(bitmap)

        # setting of the image
        self.settings = {
            "width": width,
            "height": height,
            "bit_depth": 8,
            "colour_type": 2,
            "compression_method": 0,
            "filter_method": 0,
            "interlace_method": 0
        }

        self.bitmap = list()

        # PNG headers
        self.IDAT = b''
        self.IHDR = b'IHDR' + \
                    self.settings["width"].to_bytes(4, 'big') + \
                    self.settings["height"].to_bytes(4, 'big') + \
                    self.settings["bit_depth"].to_bytes(1, 'big') + \
                    self.settings["colour_type"].to_bytes(1, 'big') + \
                    self.settings["compression_method"].to_bytes(1, 'big') + \
                    self.settings["filter_method"].to_bytes(1, 'big') + \
                    self.settings["interlace_method"].to_bytes(1, 'big')
        self.IHDR = b'\x00\x00\x00\r' + self.IHDR + zlib.crc32(self.IHDR).to_bytes(4, 'big')
        self.IEND = b'\x00\x00\x00\x00' + b'IEND' + b'' + b'\xaeB`\x82'

        # adding info about the filter type
        for row in bitmap:
            self.bitmap.append([self.settings["filter_method"], row])

        # converting list into bytes
        for row in self.bitmap:
            self.IDAT += row[0].to_bytes(1, 'big')

            for pixel in row[1]:
                self.IDAT += pixel[0].to_bytes(1, 'big')
                self.IDAT += pixel[1].to_bytes(1, 'big')
                self.IDAT += pixel[2].to_bytes(1, 'big')

        compressed_data = zlib.compress(self.IDAT)

        # construct of the IDAT header
        self.IDAT = len(compressed_data).to_bytes(4, 'big') + \
                    b'IDAT' + \
                    compressed_data + \
                    zlib.crc32(b'IDAT' + compressed_data).to_bytes(4, 'big')

        png_header = b'\x89PNG\r\n\x1a\n'
        png = png_header + self.IHDR + self.IDAT + self.IEND

        if len(output_file):
            with open(output_file, "wb") as f:
                f.write(png)

        





