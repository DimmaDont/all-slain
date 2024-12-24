#!/usr/bin/env python3
import unittest

from colorize import *


class TestNameFunctions(unittest.TestCase):

    def test_fg(self):
        result = f"{Color.BLUE("hello")} there"
        self.assertEqual(result, f"\x1b[34mhello\x1b[0m there")


if __name__ == "__main__":
    unittest.main()
