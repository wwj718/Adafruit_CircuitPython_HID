# The MIT License (MIT)
#
# Copyright (c) 2017 Dan Halbert
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""
:mod:`adafruit_hid.mouse.Mouse`
====================================================

* Author(s): Dan Halbert
"""
# import usb_hid
import pyb

class Mouse:
    """Send USB HID mouse reports."""

    LEFT_BUTTON = 1
    """Left mouse button."""
    RIGHT_BUTTON = 2
    """Right mouse button."""
    MIDDLE_BUTTON = 4
    """Middle mouse button."""

    def __init__(self):
        """Create a Mouse object that will send USB mouse HID reports."""
        self.hid_mouse = None
        '''
        for device in usb_hid.devices:
            if device.usage_page == 0x1 and device.usage == 0x02:
                self.hid_mouse = device
                break
        if not self.hid_mouse:
            raise IOError("Could not find an HID mouse device.")
        '''
        self.hid_mouse = pyb.USB_HID()
        # Reuse this bytearray to send mouse reports.
        # report[0] buttons pressed (LEFT, MIDDLE, RIGHT)
        # report[1] x movement
        # report[2] y movement
        # report[3] wheel movement
        self.report = bytearray(4)


    def press(self, buttons):
        """Press the given mouse buttons.

        :param buttons: a bitwise-or'd combination of ``LEFT_BUTTON``,
            ``MIDDLE_BUTTON``, and ``RIGHT_BUTTON``.

        Examples::

            # Press the left button.
            m.press(Mouse.LEFT_BUTTON)

            # Press the left and right buttons simultaneously.
            m.press(Mouse.LEFT_BUTTON | Mouse.RIGHT_BUTTON)
        """
        self.report[0] |= buttons
        self.move(0, 0, 0)

    def release(self, buttons):
        """Release the given mouse buttons.

        :param buttons: a bitwise-or'd combination of ``LEFT_BUTTON``,
            ``MIDDLE_BUTTON``, and ``RIGHT_BUTTON``.
        """
        self.report[0] &= ~buttons
        self.move(0, 0, 0)

    def release_all(self):
        """Release all the mouse buttons."""
        self.report[0] = 0
        self.move(0, 0, 0)

    def click(self, buttons):
        """Press and release the given mouse buttons.

        :param buttons: a bitwise-or'd combination of ``LEFT_BUTTON``,
            ``MIDDLE_BUTTON``, and ``RIGHT_BUTTON``.

        Examples::

            # Click the left button.
            m.click(Mouse.LEFT_BUTTON)

            # Double-click the left button.
            m.click(Mouse.LEFT_BUTTON)
            m.click(Mouse.LEFT_BUTTON)
        """

        self.press(buttons)
        self.release(buttons)

    def move(self, x=0, y=0, wheel=0):
        """Move the mouse and turn the wheel as directed.

        :param x: Move the mouse along the x axis. Negative is to the left, positive
            is to the right.
        :param y: Move the mouse along the y axis. Negative is upwards on the display,
            positive is downwards.
        :param wheel: Rotate the wheel this amount. Negative is toward the user, positive
            is away from the user. The scrolling effect depends on the host.
        :raises ValueError: if any argument is not in the range -127 to 127 inclusive.

        Examples::

            # Move 100 to the left. Do not move up and down. Do not roll the scroll wheel.
            m.move(-100, 0, 0)
            # Same, with keyword arguments.
            m.move(x=-100)

            # Move diagonally to the upper right.
            m.move(50, 20)
            # Same.
            m.move(x=50, y=-20)

            # Roll the mouse wheel away from the user.
            m.move(wheel=1)
        """
        if (self._distance_ok(x)
                and self._distance_ok(y)
                and self._distance_ok(wheel)):
            self.report[1] = x
            self.report[2] = y
            self.report[3] = wheel
            #self.hid_mouse.send_report(self.report)
            self.hid_mouse.send(self.report)
        else:
            raise ValueError('All arguments must be >= -127 and <= 127')

    @staticmethod
    def _distance_ok(dist):
        """Return True if dist is in the range [-127,127]"""
        return -127 <= dist <= 127
