#!/usr/bin/env python3
import unittest

from colorize import Color


class TestNameFunctions(unittest.TestCase):

    def test_fg(self):
        result = f"{Color.BLUE('hello')} there"
        self.assertEqual(result, "\x1b[34mhello\x1b[0m there")

    def test_fg_bold(self):
        result = f"{Color.BLUE('hello', bold = True)} there"
        self.assertEqual(result, "\x1b[94mhello\x1b[0m there")

    def test_bg(self):
        result = f"{Color.BLUE('hello', fg = False, bold = False, bg = True)} there"
        self.assertEqual(result, "\x1b[44mhello\x1b[0m there")

    def test_bg_bold(self):
        result = f"{Color.BLUE('hello', fg = False, bold = True, bg = True)} there"
        self.assertEqual(result, "\x1b[104mhello\x1b[0m there")

    def test_rgb(self):
        result = f"{Color.rgb(1, 2, 3, 'hello')} there"
        self.assertEqual(result, "\x1b[38;2;1;2;3mhello\x1b[0m there")

    def test_rgb_bold(self):
        result = f"{Color.rgb(1, 2, 3, 'hello', bg = True)} there"
        self.assertEqual(result, "\x1b[48;2;1;2;3mhello\x1b[0m there")

    def test_inline(self):
        result = f"{Color.BLUE.set(fg = True)}hello{Color.reset()}"
        self.assertEqual(result, Color.BLUE("hello"))


if __name__ == "__main__":
    unittest.main()
