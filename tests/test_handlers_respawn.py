import unittest

from handlers import Respawn
from state import State


class TestRespawn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        state = State()
        cls.respawn = Respawn(state)

    def test_respawn(self):
        match = self.respawn.pattern.match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Corpse> Player 'Player-123_Name' <remote client>: DoesLocationContainHospital: Searching landing zone location \"@Stanton1b_Aberdeen_Prison\" for the closest hospital. [Team_ActorTech][Actor]"
        )
        self.assertIsNotNone(match)
        self.assertEqual(len(match.groups()), 3)
        self.assertEqual(match[1], "2024-12-23T00:00:00")
        self.assertEqual(match[2], "Player-123_Name")
        self.assertEqual(match[3], "@Stanton1b_Aberdeen_Prison")
