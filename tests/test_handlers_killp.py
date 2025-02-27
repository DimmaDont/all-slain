import unittest

from handlers import KillP
from state import State


class TestKillP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        state = State()
        cls.killp = KillP(state)

    def test_killp(self):
        match = self.killp.pattern.match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Actor Death> CActor::Kill: 'PU_Human-NineTails-Grunt-Male-Grunt_10_123456789012' [123456789012] in zone 'OOC_Stanton_3a_Lyria' killed by 'Player-123_Name' [123456789012] using 'GATS_BallisticGatling_Mounted_S1_123456789012' [Class GATS_BallisticGatling_Mounted_S1] with damage type 'Bullet' from direction x: -0.123456, y: -0.123456, z: 0.123456 [Team_ActorTech][Actor]"
        )
        self.assertIsNotNone(match)
        self.assertEqual(len(match.groups()), 8)
        self.assertEqual(match[1], "2024-12-23T00:00:00")
        self.assertEqual(
            match[2], "PU_Human-NineTails-Grunt-Male-Grunt_10_123456789012"
        )
        self.assertEqual(match[3], "OOC_Stanton_3a_Lyria")
        self.assertEqual(match[4], "Player-123_Name")
        self.assertEqual(match[6], "GATS_BallisticGatling_Mounted_S1")
        self.assertEqual(match[7], "Bullet")
        self.assertEqual(match[8], "x: -0.123456, y: -0.123456, z: 0.123456")

    def test_killp_vehicledestruction(self):
        match = self.killp.pattern.match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Actor Death> CActor::Kill: 'PU_Human-NineTails-Gunner-Male-Light_01_1234567890123' [1234567890123] in zone 'ANVL_Valkyrie_PU_AI_NT_QIG_1234567890123' killed by 'Player-123_Name' [123456789012] using 'BEHR_LaserCannon_S5_1234567890123' [Class unknown] with damage type 'VehicleDestruction' from direction x: 0.000000, y: 0.000000, z: 0.000000 [Team_ActorTech][Actor]"
        )
        self.assertIsNotNone(match)
        self.assertEqual(len(match.groups()), 8)
        self.assertEqual(match[1], "2024-12-23T00:00:00")
        self.assertEqual(
            match[2], "PU_Human-NineTails-Gunner-Male-Light_01_1234567890123"
        )
        self.assertEqual(match[3], "ANVL_Valkyrie_PU_AI_NT_QIG_1234567890123")
        self.assertEqual(match[4], "Player-123_Name")
        self.assertEqual(match[6], "unknown")
        self.assertEqual(match[7], "VehicleDestruction")
        self.assertEqual(match[8], "x: 0.000000, y: 0.000000, z: 0.000000")
