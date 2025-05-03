import unittest

from src.allslain import AllSlain
from src.launcher_store import LauncherStoreException, get_log


def check_launcher_store():
    try:
        get_log()
        return True
    except LauncherStoreException:
        return False


@unittest.skipUnless(check_launcher_store(), "No game logs are available.")
class TestLogReading(unittest.TestCase):
    log: str | None

    @classmethod
    def setUpClass(cls):
        cls.log = get_log()

    def test_log_decode(self):
        assert self.log
        with open(
            self.log, "r", encoding=AllSlain.LOG_ENCODING, newline=AllSlain.LOG_NEWLINE
        ) as f:
            f.read()
