#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pngdecoder

png = pngdecoder.PNGDecoder()
png.parse("sachovnice.png")
png.handleRawData()
