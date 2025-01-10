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
        result = f"{Color.WHITE('hello', bg=Color.BLUE)} there"
        self.assertEqual(result, "\x1b[37;44mhello\x1b[0m there")

    def test_fg_bold_and_bg(self):
        result = f"{Color.WHITE('hello', bold = True, bg = Color.BLUE)} there"
        self.assertEqual(result, "\x1b[97;44mhello\x1b[0m there")

    def test_fg_and_bg_bold(self):
        result = f"{Color.WHITE('hello', bg=Color.BLUE, bg_bold=True)} there"
        self.assertEqual(result, "\x1b[37;104mhello\x1b[0m there")

    def test_rgb(self):
        result = f"{Color.rgb( fg = [1, 2, 3], text = 'hello')} there"
        self.assertEqual(result, "\x1b[38;2;1;2;3mhello\x1b[0m there")

    def test_rgb_bold(self):
        result = f"{Color.rgb( bg = [1, 2, 3 ], text = 'hello')} there"
        self.assertEqual(result, "\x1b[48;2;1;2;3mhello\x1b[0m there")

    def test_inline(self):
        result = f"{Color.BLUE.set(fg = True)}hello{Color.reset()}"
        self.assertEqual(result, Color.BLUE("hello"))

    def test_call(self):
        result = f'{Color.BLUE("hello")} there'
        self.assertEqual(result, "\x1b[34mhello\x1b[0m there")

    def test_parse(self):
        test_strings = [
            Color.parse("This is a test"),
            Color.parse("This is a (Rf)test(X)."),
            Color.parse("This is a (R)test.(X)"),
            Color.parse("This is a (Rf)(Bb)test(X)."),
        ]
        valid_strings = [
            "This is a test",
            f'This is a {Color.RED("test")}.',
            f'This is a {Color.RED("test.")}',
            f"This is a {Color.RED.set()}{Color.BLUE.set( bg = True, fg = False )}test{Color.reset()}.",
        ]
        for parse_str, valid_str in zip(test_strings, valid_strings):
            self.assertEqual(parse_str, valid_str)


if __name__ == "__main__":
    unittest.main()
