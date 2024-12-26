#!/usr/bin/env python3
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

    def __call__(self, text: str, fg: bool = True, bold: bool = False, bg: bool = False) -> str:
        color_code = self.value + (30 if fg else 0) + (60 if bold else 0) + (40 if bg else 0)
        return f"\x1b[{color_code}m{text}\x1b[0m"

    def set( self, fg: bool = False, bg: bool = False, bold: bool = False ) -> str:
        color_code = self.value + (30 if fg else 0) + (60 if bold else 0) + (40 if bg else 0)
        return f"\x1b[{color_code}m"

    @staticmethod
    def reset() -> str:
        return f"\x1b[0m"

    @staticmethod
    def rgb(r: int, g: int, b: int, text: str, bg: bool = False) -> str:
        return f"\x1b[{4 if bg else 3}8;2;{r};{g};{b}m{text}\x1b[0m"


# vim: set expandtab ts=4 sw=4
