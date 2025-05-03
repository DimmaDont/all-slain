import unittest

from src.handlers.branch import RE_SC_VERSION


class TestBranch(unittest.TestCase):
    def test_version_regular(self):
        match = RE_SC_VERSION.match("sc-alpha-4.0.0")
        self.assertIsNotNone(match)
        assert match
        self.assertEqual(len(match.groups()), 2)
        self.assertEqual(match[1], "4.0.0")
        self.assertIsNone(match[2])

    def test_version_patch_letter(self):
        match = RE_SC_VERSION.match("sc-alpha-3.22.0a")
        assert match
        self.assertEqual(match[1], "3.22.0")
        self.assertEqual(match[2], "a")

    def test_version_no_patch_with_prerelease(self):
        match = RE_SC_VERSION.match("sc-alpha-3.22-tp")
        assert match
        self.assertEqual(match[1], "3.22-tp")
        self.assertIsNone(match[2])
