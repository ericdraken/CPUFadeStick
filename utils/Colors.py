#  Copyright (c) Eric Draken, 2021.
import re
from typing import Final, Dict

from exceptions.FadeStickColorException import FadeStickColorException
from utils.Types import RGB

HEX_COLOR_RE: Final = re.compile(r'^0x([a-fA-F0-9]{6})$')

COLOR_DICT: Final[Dict[str, str]] = {
    'off': '0x000000',
    'black': '0x000000',
    'blue': '0x0000ff',
    'green': '0x00ff00',
    'purple': '0x800080',
    'red': '0xff0000',
    'white': '0xffffff',
    'yellow': '0xffff00',
}

def colorToHex(color: str) -> str:
    if color:
        hexColor = COLOR_DICT.get(color.lower())
        if hexColor:
            return hexColor
    raise FadeStickColorException(f"Color '{color}' not found")

def hexToRGB(hex_str: str) -> RGB:
    if not hex_str:
        raise FadeStickColorException("Hex string missing or None")

    if len(hex_str) != 8:
        raise FadeStickColorException(f"Hex string {hex_str} must be of the format 0xNNNNNN")

    try:
        hex_octets: Final = HEX_COLOR_RE.match(hex_str).groups()[0]
    except AttributeError:
        raise ValueError(f"'{hex_str}' is not a valid hexadecimal color value.")

    hex_lower = hex_octets.lower()
    return RGB(int(hex_lower[0:2], 16), int(hex_lower[2:4], 16), int(hex_lower[4:6], 16))

def intsToRGB(red: int = 0, green: int = 0, blue: int = 0) -> RGB:
    if not all([
        0 <= red <= 255,
        0 <= green <= 255,
        0 <= blue <= 255,
    ]):
        raise FadeStickColorException(f"One ore more colors are "
                                      f"below 0 or above 255. Given {red}, {green}, {blue}.")
    return RGB(red, green, blue)

def invertRGB(rgb: RGB) -> RGB:
    return RGB(255 - rgb.red, 255 - rgb.green, 255 - rgb.blue)
