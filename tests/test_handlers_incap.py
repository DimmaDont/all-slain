import unittest

from src.handlers.incap import LOG_INCAP_CAUSE, Incap
from src.state import State


class TestLogIncapRegexSingleCause(unittest.TestCase):
    incap: Incap

    @classmethod
    def setUpClass(cls):
        state = State()
        cls.incap = Incap(state)

    def setUp(self):
        self.match = self.incap.pattern.match(
            "Logged an incap.! nickname: Player-123_Name, causes: [Bleed (0.350000 damage)]"
        )
        self.assertIsNotNone(self.match)
        assert self.match
        self.cause = LOG_INCAP_CAUSE.findall(self.match[2])

    def test_incap(self):
        assert self.match
        self.assertEqual(len(self.match.groups()), 2)
        self.assertEqual(self.match[1], "Player-123_Name")
        self.assertEqual(self.match[2], "Bleed (0.350000 damage)")

    def test_incap_cause(self):
        self.assertEqual(self.cause[0][0], "Bleed")
        self.assertEqual(self.cause[0][1], "0.350000")


class TestLogIncapRegexMultipleCause(unittest.TestCase):
    incap: Incap

    @classmethod
    def setUpClass(cls):
        state = State()
        cls.incap = Incap(state)

    def setUp(self):
        self.match = self.incap.pattern.match(
            "Logged an incap.! nickname: Player-123_Name, causes: [DepressurizationDamage (3.999999 damage), SuffocationDamage (1.999999 damage)]"
        )
        self.assertIsNotNone(self.match)
        assert self.match
        self.cause = LOG_INCAP_CAUSE.findall(self.match[2])

    def test_incap(self):
        assert self.match
        self.assertEqual(len(self.match.groups()), 2)
        self.assertEqual(self.match[1], "Player-123_Name")
        self.assertEqual(
            self.match[2],
            "DepressurizationDamage (3.999999 damage), SuffocationDamage (1.999999 damage)",
        )

    def test_incap_cause(self):
        self.assertEqual(self.cause[0][0], "DepressurizationDamage")
        self.assertEqual(self.cause[0][1], "3.999999")
        self.assertEqual(self.cause[1][0], "SuffocationDamage")
        self.assertEqual(self.cause[1][1], "1.999999")
