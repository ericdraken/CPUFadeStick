#  Copyright (c) Eric Draken, 2021.
import re
from typing import Text, Final

from exceptions.FadeStickException import FadeStickException

HEX_COLOR_RE: Final = re.compile(r'^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$')

colorDict = {
    'blue': '#0000ff',
    'green': '#008000',
    'purple': '#800080',
    'red': '#ff0000',
    'white': '#ffffff',
    'yellow': '#ffff00',
}

def colorToHex(color: Text) -> Text:
    hexColor = colorDict[color.lower()]
    if hexColor:
        return hexColor
    raise FadeStickException("Color not found")
