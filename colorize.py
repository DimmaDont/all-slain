#!/usr/bin/env python3
import re
from enum import IntEnum

class Color(IntEnum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

    def __call__(self, text: str, fg=None, bg=None, bold: bool = False ) -> str:
        """Colorizes text.

        Args:
            text: str   The text to colorize
            fg: Color   The foreground color.  Defaults to self.
            bg: Color   The background color.  Defaults to None
            bold: bool  Whether to make the text bold

        Returns:
            The colorized text
        """
        color_codes = []

        if not any( [fg, bg, bold] ):
            return f'{self.set()}{text}{self.reset()}'

        if fg is not None:
            color_codes.append( str( fg.value + 30 + ( 60 if bold else 0 ) ) )
        elif bold:
            color_codes.append( str( self.value + 60 ) ) # Bold only

        if bg is not None:
            color_codes.append( str( bg.value + 40 ) )

        if not color_codes:
            return text
        else:
            return f'\x1b[{";".join( color_codes )}m{text}\x1b[0m'

    def set( self, fg: bool = True, bg: bool = False, bold: bool = False ) -> str:
        color_code = self.value + (30 if fg else 0) + (60 if bold else 0) + (40 if bg else 0)
        return f"\x1b[{color_code}m"

    @staticmethod
    def reset() -> str:
        return f"\x1b[0m"

    @staticmethod
    def rgb(r: int, g: int, b: int, text: str, bg: bool = False) -> str:
        return f"\x1b[{4 if bg else 3}8;2;{r};{g};{b}m{text}\x1b[0m"


# vim: set expandtab ts=4 sw=4
