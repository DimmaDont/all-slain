import unittest

from handlers.branch import RE_SC_VERSION


class TestBranch(unittest.TestCase):
    def test_versions(self):
        for version in [
            "sc-alpha-3.22.0a",
            "sc-alpha-3.22-tp",
            "sc-alpha-4.0.0",
        ]:
            self.assertIsNotNone(RE_SC_VERSION.match(version))
