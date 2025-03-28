import unittest

from handlers.branch import RE_SC_VERSION


class TestBranch(unittest.TestCase):
    def test_version_regular(self):
        result = RE_SC_VERSION.match("sc-alpha-4.0.0")
        self.assertIsNotNone(result)
        self.assertEqual(len(result.groups()), 2)
        self.assertEqual(result[1], "4.0.0")
        self.assertIsNone(result[2])

    def test_version_patch_letter(self):
        result = RE_SC_VERSION.match("sc-alpha-3.22.0a")
        self.assertEqual(result[1], "3.22.0")
        self.assertEqual(result[2], "a")

    def test_version_no_patch_with_prerelease(self):
        result = RE_SC_VERSION.match("sc-alpha-3.22-tp")
        self.assertEqual(result[1], "3.22-tp")
        self.assertIsNone(result[2])
