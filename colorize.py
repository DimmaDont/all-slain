#!/usr/bin/env python3
"""
This module provides a class for colorizing terminal output using virtual
terminal sequences.

Classes:
    Color: Class containing methods to colorize text.

Methods:
    __call__: Colorizes text.
    set: Returns a terminal sequence for setting the specified color and
        attributes.
    parse: Parses a string containing color tags and replaces them with the
        appropriate terminal sequences.
    reset: Returns a terminal sequence to reset colors to default.
    rgb: Colorizes text using RGB color values.
"""

from enum import IntEnum
import re

try:
    from typing import Self  # 3.11+
except ImportError:
    from typing_extensions import Self


class Color(IntEnum):
    """
    Represents colors for terminal output.

    Provides methods for colorizing text, setting color codes, and resetting
    terminal colors. Also includes a static method for using RGB color values.

    Attributes:
        BLACK: Represents the color black.
        RED: Represents the color red.
        GREEN: Represents the color green.
        YELLOW: Represents the color yellow.
        BLUE: Represents the color blue.
        MAGENTA: Represents the color magenta.
        CYAN: Represents the color cyan.
        WHITE: Represents the color white.
    """

    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

    def __call__(
        self,
        text: str,
        bold: bool = False,
        bg: Self | None = None,
        bg_bold: bool = False,
    ) -> str:
        """Colorizes text.

        Args:
            text: The text to colorize.
            bold: Whether to make the foreground text bold.
            bg: The background color.
            bg_bold: Whether to make the background color bold.

        Returns:
            The colorized text
        """

        if not any([bold, bg, bg_bold]):
            return f"{self.set()}{text}{self.reset()}"

        color_codes = [str(self.value + 30 + (60 if bold else 0))]

        if bg:
            color_codes.append(str(bg.value + 40 + (60 if bg_bold else 0)))

        return f'\x1b[{";".join(color_codes)}m{text}\x1b[0m'

    def set(self, fg: bool = True, bg: bool = False, bold: bool = False) -> str:
        """
        Sets the color codes for the current Color instance.

        Args:
            fg: Whether to include foreground color. Defaults to True.
            bg: Whether to include background color. Defaults to False.
            bold: Whether to include bold attribute. Defaults to False.

        Returns:
            The ANSI escape sequence for setting the specified colors.
        """
        color_code = (
            self.value + (30 if fg else 0) + (60 if bold else 0) + (40 if bg else 0)
        )
        return f"\x1b[{color_code}m"

    @classmethod
    def parse(cls, text: str) -> str:
        """Parses a string for color tags and replaces them with ANSI escape codes.

        This method searches for tags in the format `(C)` or `(Cb)`, where `C` is a
        single character representing a color (K=Black, R=Red, G=Green, Y=Yellow,
        B=Blue, M=Magenta, C=Cyan, W=White) and `b` indicates a background color.
        The tag `(X)` resets the color to default.

        Args:
            text: The string to parse for color tags.

        Returns:
            The string with color tags replaced by ANSI escape codes, or the
            original string if no valid tags are found.

        Example:
            >>> Color.parse('(Rb)Red background (G)Green text (X) Back to normal')
            '\x1b[41mRed background \x1b[32mGreen text \x1b[0m Back to normal'
        """
        color_map = {
            "K": cls.BLACK,
            "R": cls.RED,
            "G": cls.GREEN,
            "Y": cls.YELLOW,
            "B": cls.BLUE,
            "M": cls.MAGENTA,
            "C": cls.CYAN,
            "W": cls.WHITE,
        }
        tags = re.findall(r"\(([XKRGYBMCW][fb]?)\)", text)
        for tag in tags:
            if tag[0] == "X":
                text = text.replace(f"({tag})", cls.reset())
            else:
                c = color_map[tag[0]]
                if len(tag) == 2 and tag[1] == "b":
                    text = text.replace(f"({tag})", c.set(fg=False, bg=True))
                else:
                    text = text.replace(f"({tag})", c.set())
        return text

    @staticmethod
    def reset() -> str:
        """
        Resets the terminal colors to default.

        Returns:
            The ANSI escape sequence for resetting colors.
        """
        return "\x1b[0m"

    @staticmethod
    def rgb(
        fg: list[int | None] | None = None,
        bg: list[int | None] | None = None,
        bold: bool = False,
        text: str = "",
    ) -> str:
        """
        Colorizes the given text using RGB color values.

        Args:
            fg: A list containing the red, green, and blue components of the foreground color.
                If None, no foreground color is set.
            bg: A list containing the red, green, and blue components of the background color.
                If None, no background color is set.
            bold: Whether to make the text bold. Defaults to False.
            text: The text to be colorized. Defaults to an empty string.

        Raises:
            ValueError: If neither fg nor bg is provided.

        Returns:
            The colorized text string using RGB color values.
        """
        if not any([fg, bg]):
            raise ValueError("rgb() called without specifying either fg or bg")
        color_codes = []
        if fg is not None:
            if not (
                fg == [None, None, None]
                or (all(isinstance(x, int) for x in fg) and len(fg) == 3)
            ):
                raise ValueError(f"fg must be a list of 3 integers.  {fg=}")
            if fg != [None, None, None]:
                color_codes.append(f"38;2;{fg[0]};{fg[1]};{fg[2]}")
        if bg is not None:
            if not (
                bg == [None, None, None]
                or (all(isinstance(x, int) for x in bg) and len(bg) == 3)
            ):
                raise ValueError(f"bg must be a list of 3 integers.  {bg=}")
            if bg != [None, None, None]:
                color_codes.append(f"48;2;{bg[0]};{bg[1]};{bg[2]}")
        if bold:
            color_codes.append("1")

        if color_codes:
            return f'\x1b[{";".join(color_codes)}m{text}\x1b[0m'
        return text


# vim: set expandtab ts=4 sw=4
