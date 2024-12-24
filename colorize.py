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

    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97

    def __call__(self, text) -> str:
        return f"\x1b[{self}m{text}{Color.RESET}"

    @staticmethod
    def rgb(r: int, g: int, b: int, text: str) -> str:
        return f"\x1b[38;2;{r};{g};{b}m{text}{Color.RESET}"


Color.RESET = "\x1b[0m"


# vim: set expandtab ts=4 sw=4
