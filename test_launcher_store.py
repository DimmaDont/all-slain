import unittest

from allslain import AllSlain
from launcher_store import get_log


@unittest.skipUnless(get_log(), "No game logs are available.")
class TestLogReading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = get_log()

    def test_log_decode(self):
        with open(
            self.log, "r", encoding=AllSlain.LOG_ENCODING, newline=AllSlain.LOG_NEWLINE
        ) as f:
            f.read()
