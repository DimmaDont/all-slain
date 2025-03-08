import unittest

from handlers.corpse import CorpseHospitalLocation
from state import State


class TestRespawn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        state = State()
        cls.respawn = CorpseHospitalLocation(state)

    def test_respawn(self):
        match = self.respawn.pattern.match(
            "[Notice] <Corpse> Player 'Player-123_Name' <remote client>: DoesLocationContainHospital: Searching landing zone location \"@Stanton1b_Aberdeen_Prison\" for the closest hospital. [Team_ActorTech][Actor]"
        )
        self.assertIsNotNone(match)
        self.assertEqual(len(match.groups()), 2)
        self.assertEqual(match[1], "Player-123_Name")
        self.assertEqual(match[2], "@Stanton1b_Aberdeen_Prison")
