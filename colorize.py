#!/usr/bin/env python3
from enum import IntEnum


class Color(IntEnum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    def __call__(self, text: str, bold: bool = False, bg: bool = False) -> str:
        color_code = self.value + (60 if bold else 0) + (10 if bg else 0)
        return f"\x1b[{color_code}m{text}\x1b[0m"

    @staticmethod
    def rgb(r: int, g: int, b: int, text: str, bg: bool = False) -> str:
        return f"\x1b[{4 if bg else 3}8;2;{r};{g};{b}m{text}\x1b[0m"


# vim: set expandtab ts=4 sw=4
