#  Copyright (c) Eric Draken, 2021.
from __future__ import annotations
from typing import Final

from multipledispatch import dispatch

from constants.FadeStickConsts import FS_SERIAL_INDEX, FS_REPORT_ID
from exceptions.FadeStickColorException import FadeStickColorException
from utils.Colors import invertRGB, colorToHex, hexToRGB
from utils.Types import RGB, USBDevice


class FadeStick(object):
    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        string = "TODO"  # TODO: this
        return string

    serial: str = ""
    device: USBDevice = None
    error_reporting: bool = True
    inverse: bool = False

    def __init__(self, device: USBDevice = None, error_reporting=True):
        self.error_reporting: Final = error_reporting

        if device:
            from core.FadeStickUSB import openUSBDevice, getUSBString
            self.device: Final = device
            openUSBDevice(device)
            self.serial: Final = getUSBString(device, FS_SERIAL_INDEX)

    @dispatch(str)
    def setColor(self, name_or_hex: str) -> RGB:
        try:
            return self.setColor(hexToRGB(colorToHex(name_or_hex)))
        except FadeStickColorException:
            return self.setColor(hexToRGB(name_or_hex))

    @dispatch(int, int, int)
    def setColor(self, red: int, green: int, blue: int) -> RGB:
        return self.setColor(RGB(red, green, blue))

    # noinspection PyBroadException
    @dispatch(RGB)
    def setColor(self, rgb: RGB) -> RGB:
        if self.inverse:
            rgb = invertRGB(rgb)

        control_string = bytes(bytearray([0, rgb.red, rgb.green, rgb.blue]))

        from core.FadeStickUSB import sendControlTransfer
        if self.error_reporting:
            sendControlTransfer(self, 0x20, 0x9, FS_REPORT_ID, 0, control_string)
        else:
            try:
                sendControlTransfer(self, 0x20, 0x9, FS_REPORT_ID, 0, control_string)
            except Exception:
                pass

        return rgb

    def turnOff(self) -> None:
        self.setColor(0, 0, 0)

    def getColor(self) -> RGB:
        from core.FadeStickUSB import sendControlTransfer
        device_bytes = sendControlTransfer(self, 0x80 | 0x20, 0x1, 0x0001, 0, 33)
        rgb = RGB(device_bytes[1], device_bytes[2], device_bytes[3])
        return invertRGB(rgb) if self.inverse else rgb





    # # def _determine_rgb(self, red=0, green=0, blue=0, name=None, hex=None):
    # #
    # #     try:
    # #         if name:
    # #             # Special case for name="random"
    # #             if name == "random":
    # #                 red = randint(0, 255)
    # #                 green = randint(0, 255)
    # #                 blue = randint(0, 255)
    # #             else:
    # #                 red, green, blue = self._name_to_rgb(name)
    # #         elif hex:
    # #             red, green, blue = self._hex_to_rgb(hex)
    # #     except ValueError:
    # #         red = green = blue = 0
    # #
    # #     red, green, blue = _remap_rgb_value([red, green, blue], self.max_rgb_value)
    # #
    # #     # TODO - do smarts to determine input type from red var in case it is not int
    # #
    # #     return red, green, blue
    # #

    # # def _get_color_hex(self, index=0):
    # #     r, g, b = self._get_color_rgb(index)
    # #     return '#%02x%02x%02x' % (r, g, b)
    # #
    # # def get_color(self, index=0, color_format='rgb'):
    # #     """
    # #     Get the current device color in the defined format.
    # #
    # #     Currently supported formats:
    # #
    # #         1. rgb (default) - Returns values as 3-tuple (r,g,b)
    # #         2. hex - returns current device color as hexadecimal string
    # #
    # #         >>> b = FadeStick.find_first()
    # #         >>> b.set_color(red=255,green=0,blue=0)
    # #         >>> (r,g,b) = b.get_color() # Get color as rbg tuple
    # #         (255,0,0)
    # #         >>> hex = b.get_color(color_format='hex') # Get color as hex string
    # #         '#ff0000'
    # #
    # #     @type  index: int
    # #     @param index: the index of the LED
    # #     @type  color_format: str
    # #     @param color_format: "rgb" or "hex". Defaults to "rgb".
    # #
    # #     @rtype: (int, int, int) or str
    # #     @return: Either 3-tuple for R, G and B values, or hex string
    # #     """
    # #
    # #     # Attempt to find a function to return the appropriate format
    # #     get_color_func = getattr(self, "_get_color_%s" % color_format, self._get_color_rgb)
    # #     if isinstance(get_color_func, collections.Callable):
    # #         return get_color_func(index)
    # #     else:
    # #         # Should never get here, as we should always default to self._get_color_rgb
    # #         raise FadeStickException("Could not return current color in format %s" % color_format)
    #
    # def _determine_report_id(self, led_count):
    #     report_id = 9
    #     max_leds = 64
    #
    #     if led_count <= 8 * 3:
    #         max_leds = 8
    #         report_id = 6
    #     elif led_count <= 16 * 3:
    #         max_leds = 16
    #         report_id = 7
    #     elif led_count <= 32 * 3:
    #         max_leds = 32
    #         report_id = 8
    #     elif led_count <= 64 * 3:
    #         max_leds = 64
    #         report_id = 9
    #
    #     return report_id, max_leds
    #
    # # def set_led_data(self, channel, data):
    # #     """
    # #     Send LED data frame.
    # #
    # #     @type  channel: int
    # #     @param channel: the channel which to send data to (R=0, G=1, B=2)
    # #     @type  data: int[0..64*3]
    # #     @param data: The LED data frame in GRB format
    # #     """
    # #
    # #     report_id, max_leds = self._determine_report_id(len(data))
    # #
    # #     report = [0, channel]
    # #
    # #     for i in range(0, max_leds * 3):
    # #         if len(data) > i:
    # #             report.append(data[i])
    # #         else:
    # #             report.append(0)
    # #
    # #     self._usb_ctrl_transfer(0x20, 0x9, report_id, 0, bytes(bytearray(report)))
    # #
    # # def get_led_data(self, count):
    # #     """
    # #     Get LED data frame on the device.
    # #
    # #     @type  count: int
    # #     @param count: How much data to retrieve. Can be in the range of 0..64*3
    # #     @rtype: int[0..64*3]
    # #     @return: LED data currently stored in the RAM of the device
    # #     """
    # #
    # #     report_id, max_leds = self._determine_report_id(count)
    # #
    # #     device_bytes = self._usb_ctrl_transfer(0x80 | 0x20, 0x1, report_id, 0, max_leds * 3 + 2)
    # #
    # #     return device_bytes[2: 2 + count * 3]
    #
    # def get_info_block1(self):
    #     """
    #     Get the infoblock1 of the device.
    #
    #     This is a 32 byte array that can contain any data. It's supposed to
    #     hold the "Name" of the device making it easier to identify rather than
    #     a serial number.
    #
    #     @rtype: str
    #     @return: InfoBlock1 currently stored on the device
    #     """
    #
    #     device_bytes = self._usb_ctrl_transfer(0x80 | 0x20, 0x1, 0x0002, 0, 33)
    #     result = ""
    #     for i in device_bytes[1:]:
    #         if i == 0:
    #             break
    #         result += chr(i)
    #     return result
    #
    # def get_info_block2(self):
    #     """
    #     Get the infoblock2 of the device.
    #
    #     This is a 32 byte array that can contain any data.
    #
    #     @rtype: str
    #     @return: InfoBlock2 currently stored on the device
    #     """
    #     device_bytes = self._usb_ctrl_transfer(0x80 | 0x20, 0x1, 0x0003, 0, 33)
    #     result = ""
    #     for i in device_bytes[1:]:
    #         if i == 0:
    #             break
    #         result += chr(i)
    #     return result
    #
    # def _data_to_message(self, data):
    #     """
    #     Helper method to convert a string to byte array of 32 bytes.
    #
    #     @type  data: str
    #     @param data: The data to convert to byte array
    #
    #     @rtype: byte[32]
    #     @return: It fills the rest of bytes with zeros.
    #     """
    #     bytes = [1]
    #     for c in data:
    #         bytes.append(ord(c))
    #
    #     for i in range(32 - len(data)):
    #         bytes.append(0)
    #
    #     return bytes
    #
    # def set_info_block1(self, data):
    #     """
    #     Sets the infoblock1 with specified string.
    #
    #     It fills the rest of 32 bytes with zeros.
    #
    #     @type  data: str
    #     @param data: InfoBlock1 for the device to set
    #     """
    #     self._usb_ctrl_transfer(0x20, 0x9, 0x0002, 0, self._data_to_message(data))
    #
    # def set_info_block2(self, data):
    #     """
    #     Sets the infoblock2 with specified string.
    #
    #     It fills the rest of 32 bytes with zeros.
    #
    #     @type  data: str
    #     @param data: InfoBlock2 for the device to set
    #     """
    #     self._usb_ctrl_transfer(0x20, 0x9, 0x0003, 0, self._data_to_message(data))
    # #
    # # def set_random_color(self):
    # #     """
    # #     Sets random color to the device.
    # #     """
    # #     self.set_color(name="random")
    # #
    # # def turn_off(self):
    # #     """
    # #     Turns off LED.
    # #     """
    # #     self.set_color()
    # #
    # # def pulse(self, channel=0, index=0, red=0, green=0, blue=0, name=None, hex=None, repeats=1, duration=1000, steps=50):
    # #     """
    # #     Morph to the specified color from black and back again.
    # #
    # #     @type  red: int
    # #     @param red: Red color intensity 0 is off, 255 is full red intensity
    # #     @type  green: int
    # #     @param green: Green color intensity 0 is off, 255 is full green intensity
    # #     @type  blue: int
    # #     @param blue: Blue color intensity 0 is off, 255 is full blue intensity
    # #     @type  name: str
    # #     @param name: Use CSS color name as defined here: U{http://www.w3.org/TR/css3-color/}
    # #     @type  hex: str
    # #     @param hex: Specify color using hexadecimal color value e.g. '#FF3366'
    # #     @type  repeats: int
    # #     @param repeats: Number of times to pulse the LED
    # #     @type  duration: int
    # #     @param duration: Duration for pulse in milliseconds
    # #     @type  steps: int
    # #     @param steps: Number of gradient steps
    # #     """
    # #     r, g, b = self._determine_rgb(red=red, green=green, blue=blue, name=name, hex=hex)
    # #
    # #     self.turn_off()
    # #     for x in range(repeats):
    # #         self.morph(channel=channel, index=index, red=r, green=g, blue=b, duration=duration, steps=steps)
    # #         self.morph(channel=channel, index=index, red=0, green=0, blue=0, duration=duration, steps=steps)
    # #
    # # def blink(self, channel=0, index=0, red=0, green=0, blue=0, name=None, hex=None, repeats=1, delay=500):
    # #     """
    # #     Blink the specified color.
    # #
    # #     @type  red: int
    # #     @param red: Red color intensity 0 is off, 255 is full red intensity
    # #     @type  green: int
    # #     @param green: Green color intensity 0 is off, 255 is full green intensity
    # #     @type  blue: int
    # #     @param blue: Blue color intensity 0 is off, 255 is full blue intensity
    # #     @type  name: str
    # #     @param name: Use CSS color name as defined here: U{http://www.w3.org/TR/css3-color/}
    # #     @type  hex: str
    # #     @param hex: Specify color using hexadecimal color value e.g. '#FF3366'
    # #     @type  repeats: int
    # #     @param repeats: Number of times to pulse the LED
    # #     @type  delay: int
    # #     @param delay: time in milliseconds to light LED for, and also between blinks
    # #     """
    # #     r, g, b = self._determine_rgb(red=red, green=green, blue=blue, name=name, hex=hex)
    # #     ms_delay = float(delay) / float(1000)
    # #     for x in range(repeats):
    # #         if x:
    # #             time.sleep(ms_delay)
    # #         self.set_color(channel=channel, index=index, red=r, green=g, blue=b)
    # #         time.sleep(ms_delay)
    # #         self.set_color(channel=channel, index=index)
    # #
    # # def morph(self, channel=0, index=0, red=0, green=0, blue=0, name=None, hex=None, duration=1000, steps=50):
    # #     """
    # #     Morph to the specified color.
    # #
    # #     @type  red: int
    # #     @param red: Red color intensity 0 is off, 255 is full red intensity
    # #     @type  green: int
    # #     @param green: Green color intensity 0 is off, 255 is full green intensity
    # #     @type  blue: int
    # #     @param blue: Blue color intensity 0 is off, 255 is full blue intensity
    # #     @type  name: str
    # #     @param name: Use CSS color name as defined here: U{http://www.w3.org/TR/css3-color/}
    # #     @type  hex: str
    # #     @param hex: Specify color using hexadecimal color value e.g. '#FF3366'
    # #     @type  duration: int
    # #     @param duration: Duration for morph in milliseconds
    # #     @type  steps: int
    # #     @param steps: Number of gradient steps (default 50)
    # #     """
    # #
    # #     r_end, g_end, b_end = self._determine_rgb(red=red, green=green, blue=blue, name=name, hex=hex)
    # #
    # #     r_start, g_start, b_start = _remap_rgb_value_reverse(self._get_color_rgb(index), self.max_rgb_value)
    # #
    # #     if r_start > 255 or g_start > 255 or b_start > 255:
    # #         r_start = 0
    # #         g_start = 0
    # #         b_start = 0
    # #
    # #     gradient = []
    # #
    # #     steps += 1
    # #     for n in range(1, steps):
    # #         d = 1.0 * n / steps
    # #         r = (r_start * (1 - d)) + (r_end * d)
    # #         g = (g_start * (1 - d)) + (g_end * d)
    # #         b = (b_start * (1 - d)) + (b_end * d)
    # #
    # #         gradient.append((r, g, b))
    # #
    # #     ms_delay = float(duration) / float(1000 * steps)
    # #
    # #     self.set_color(channel=channel, index=index, red=r_start, green=g_start, blue=b_start)
    # #
    # #     for grad in gradient:
    # #         grad_r, grad_g, grad_b = grad
    # #
    # #         self.set_color(channel=channel, index=index, red=grad_r, green=grad_g, blue=grad_b)
    # #         time.sleep(ms_delay)
    # #
    # #     self.set_color(channel=channel, index=index, red=r_end, green=g_end, blue=b_end)
    #
    # def open_device(self, d):
    #     """Open device.
    #     @param d: Device to open
    #     """
    #     if self.device is None:
    #         raise FadeStickException("Could not find FadeStick...")
    #
    #     if self.device.is_kernel_driver_active(0):
    #         try:
    #             self.device.detach_kernel_driver(0)
    #         except usb.core.USBError as e:
    #             raise FadeStickException("Could not detach kernel driver: %s" % str(e))
    #
    #     return True
    #
    # def get_inverse(self):
    #     """
    #     Get the value of inverse mode. This applies only to FadeStick. Please use L{set_mode} for FadeStick Pro
    #     to permanently set the inverse mode to the device.
    #
    #     @rtype: bool
    #     @return: True if inverse mode, otherwise false
    #     """
    #     return self.inverse
    #
    # def set_inverse(self, value):
    #     """
    #     Set inverse mode. This applies only to FadeStick. Please use L{set_mode} for FadeStick Pro
    #     to permanently set the inverse mode to the device.
    #
    #     @type  value: bool
    #     @param value: True/False to set the inverse mode
    #     """
    #     self.inverse = value
    #
    # def set_max_rgb_value(self, value):
    #     """
    #     Set RGB color limit. {set_color} function will automatically remap
    #     the values to maximum supplied.
    #
    #     @type  value: int
    #     @param value: 0..255 maximum value for each R, G and B color
    #     """
    #     self.max_rgb_value = value
    #
    # def get_max_rgb_value(self, max_rgb_value):
    #     """
    #     Get RGB color limit. {set_color} function will automatically remap
    #     the values to maximum set.
    #
    #     @rtype: int
    #     @return: 0..255 maximum value for each R, G and B color
    #     """
    #     return self.max_rgb_value
    #
    # def _name_to_hex(self, name):
    #     """
    #     Convert a color name to a normalized hexadecimal color value.
    #
    #     The color name will be normalized to lower-case before being
    #     looked up, and when no color of that name exists in the given
    #     specification, ``ValueError`` is raised.
    #
    #     Examples:
    #
    #     >>> _name_to_hex('white')
    #     '#ffffff'
    #     >>> _name_to_hex('navy')
    #     '#000080'
    #     >>> _name_to_hex('goldenrod')
    #     '#daa520'
    #     """
    #     normalized = name.lower()
    #     try:
    #         hex_value = self._names_to_hex[normalized]
    #     except KeyError:
    #         raise ValueError("'%s' is not defined as a named color." % (name))
    #     return hex_value
    #
    # def _hex_to_rgb(self, hex_value):
    #     """
    #     Convert a hexadecimal color value to a 3-tuple of integers
    #     suitable for use in an ``rgb()`` triplet specifying that color.
    #
    #     The hexadecimal value will be normalized before being converted.
    #
    #     Examples:
    #
    #     >>> _hex_to_rgb('#fff')
    #     (255, 255, 255)
    #     >>> _hex_to_rgb('#000080')
    #     (0, 0, 128)
    #
    #     """
    #     hex_digits = self._normalize_hex(hex_value)
    #     return tuple([int(s, 16) for s in (hex_digits[1:3], hex_digits[3:5], hex_digits[5:7])])
    #
    # def _normalize_hex(self, hex_value):
    #     """
    #     Normalize a hexadecimal color value to the following form and
    #     return the result::
    #
    #         #[a-f0-9]{6}
    #
    #     In other words, the following transformations are applied as
    #     needed:
    #
    #     * If the value contains only three hexadecimal digits, it is expanded to six.
    #
    #     * The value is normalized to lower-case.
    #
    #     If the supplied value cannot be interpreted as a hexadecimal color
    #     value, ``ValueError`` is raised.
    #
    #     Examples:
    #
    #     >>> _normalize_hex('#0099cc')
    #     '#0099cc'
    #     >>> _normalize_hex('#0099CC')
    #     '#0099cc'
    #     >>> _normalize_hex('#09c')
    #     '#0099cc'
    #     >>> _normalize_hex('#09C')
    #     '#0099cc'
    #     >>> _normalize_hex('0099cc')
    #     Traceback (most recent call last):
    #         ...
    #     ValueError: '0099cc' is not a valid hexadecimal color value.
    #
    #     """
    #     try:
    #         hex_digits = self.HEX_COLOR_RE.match(hex_value).groups()[0]
    #     except AttributeError:
    #         raise ValueError("'%s' is not a valid hexadecimal color value." % hex_value)
    #     if len(hex_digits) == 3:
    #         hex_digits = ''.join([2 * s for s in hex_digits])
    #     return '#%s' % hex_digits.lower()
    #
    # def _name_to_rgb(self, name):
    #     """
    #     Convert a color name to a 3-tuple of integers suitable for use in
    #     an ``rgb()`` triplet specifying that color.
    #
    #     The color name will be normalized to lower-case before being
    #     looked up, and when no color of that name exists in the given
    #     specification, ``ValueError`` is raised.
    #
    #     Examples:
    #
    #     >>> _name_to_rgb('white')
    #     (255, 255, 255)
    #     >>> _name_to_rgb('navy')
    #     (0, 0, 128)
    #     >>> _name_to_rgb('goldenrod')
    #     (218, 165, 32)
    #
    #     """
    #     return self._hex_to_rgb(self._name_to_hex(name))
