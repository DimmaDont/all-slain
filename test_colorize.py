#!/usr/bin/env python3
import unittest

from colorize import Color


class TestNameFunctions(unittest.TestCase):

    def test_fg(self):
        result = f"{Color.BLUE('hello')} there"
        self.assertEqual(result, "\x1b[34mhello\x1b[0m there")

    def test_fg_bold(self):
        result = f"{Color.BLUE('hello', bold = True)} there"
        self.assertEqual(result, "\x1b[64mhello\x1b[0m there")

    def test_bg(self):
        result = f"{Color.WHITE('hello', bg=Color.BLUE)} there"
        self.assertEqual(result, "\x1b[44mhello\x1b[0m there")

    def test_bg_bold(self):
        result = f"{Color.WHITE('hello', bold = True, bg = Color.BLUE)} there"
        self.assertEqual(result, "\x1b[67;44mhello\x1b[0m there")

    def test_rgb(self):
        result = f"{Color.rgb(1, 2, 3, 'hello')} there"
        self.assertEqual(result, "\x1b[38;2;1;2;3mhello\x1b[0m there")

    def test_rgb_bold(self):
        result = f"{Color.rgb(1, 2, 3, 'hello', bg = True)} there"
        self.assertEqual(result, "\x1b[48;2;1;2;3mhello\x1b[0m there")

    def test_inline(self):
        result = f'{Color.BLUE.set(fg = True)}hello{Color.reset()}'
        self.assertEqual( result, Color.BLUE('hello') )

    def test_call( self ):
        result = f'{Color.BLUE("hello")} there'
        self.assertEqual( result,  "\x1b[34mhello\x1b[0m there" )


if __name__ == "__main__":
    unittest.main()
