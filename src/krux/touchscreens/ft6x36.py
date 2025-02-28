# The MIT License (MIT)

# Copyright (c) 2021-2022 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# pylint: disable=W0231

# FT6x36 specs:
# Max sample rate: 100 samples per second

from . import Touchscreen
import board
from machine import I2C

FT_DEVICE_MODE = 0x00
GEST_ID = 0x01
TD_STATUS = 0x02
PN_XH = 0x03
FT_ID_G_MODE = 0xA4
FT_ID_G_THGROUP = 0x80
FT_ID_SR_PERIODACTIVE = 0x88
FT6X36_ADDR = 0x38

TOUCH_THRESHOLD = 22  # Default 22


class FT6X36(Touchscreen):
    """FT6X36 is a minimal wrapper around a I2C connection to setup and get
    data from FT6X36 touchscreen IC, part of Sipeed's Maix Amigo device"""

    def __init__(self):
        self.addr = FT6X36_ADDR
        self.i2c = I2C(
            I2C.I2C0,
            freq=100000,
            scl=board.config["krux"]["pins"]["I2C_SCL"],
            sda=board.config["krux"]["pins"]["I2C_SDA"],
        )
        """Setup registers"""
        # Device mode
        self.write_reg(FT_DEVICE_MODE, 0)
        # Threshold for touch detection
        self.write_reg(FT_ID_G_THGROUP, TOUCH_THRESHOLD)
        # Mode = 0 = polling mode
        self.write_reg(FT_ID_G_MODE, 0)

    def write_reg(self, reg_addr, buf):
        """Writes buffer content to a register address"""
        self.i2c.writeto_mem(self.addr, reg_addr, buf, mem_size=8)

    def read_reg(self, reg_addr, buf_len):
        """Reads from a register address"""
        return self.i2c.readfrom_mem(self.addr, reg_addr, buf_len, mem_size=8)

    def current_point(self):
        """If touch is pressed, returns x and y points"""
        try:
            data = self.read_reg(TD_STATUS, 1)
            # if touch points==1
            if data is not None and data[0] == 0x1:
                # Read Xhigh, Xlow, Yhigh and Ylow
                data_buf = self.read_reg(PN_XH, 4)
                x = ((data_buf[0] & 0x0F) << 8) | (data_buf[1])
                y = ((data_buf[2] & 0x0F) << 8) | (data_buf[3])
                return (x, y)
        except Exception as e:
            return e  # debug
        return None
