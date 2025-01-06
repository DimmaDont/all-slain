#!/usr/bin/env python3
import re
from enum import IntEnum


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

    def __call__(self, text: str, fg=None, bg=None, bold: bool = False) -> str:
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

        if not any([fg, bg, bold]):
            return f"{self.set()}{text}{self.reset()}"

        if fg is not None:
            color_codes.append(str(fg.value + 30 + (60 if bold else 0)))
        elif bold:
            color_codes.append(str(self.value + 60))  # Bold only

        if bg is not None:
            color_codes.append(str(bg.value + 40))

        if not color_codes:
            return text
        else:
            return f'\x1b[{";".join( color_codes )}m{text}\x1b[0m'

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

    @staticmethod
    def reset() -> str:
        """
        Resets the terminal colors to default.

        Returns:
            The ANSI escape sequence for resetting colors.
        """
        return f"\x1b[0m"

    @staticmethod
    def rgb(
        fg: list[int | None] = None,
        bg: list[int | None] = None,
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

        if not color_codes:
            return text
        else:
            return f'\x1b[{";".join(color_codes)}m{text}\x1b[0m'


# vim: set expandtab ts=4 sw=4
