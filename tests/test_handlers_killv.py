import unittest

from handlers import KillV
from state import State


class TestKillV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        state = State()
        cls.killv = KillV(state)

    def test_killv(self):
        match = self.killv.pattern.match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle 'MRAI_Guardian_QI_123456789012' [123456789012] in zone 'OOC_Stanton_3a_Lyria' [pos x: -200000.000000, y: 100000.000000, z: 60000.000000 vel x: 0.000000, y: 0.000000, z: 0.000000] driven by 'unknown' [0] advanced from destroy level 1 to 2 caused by 'Player-123_Name' [123456789012] with 'Combat' [Team_VehicleFeatures][Vehicle]"
        )
        self.assertIsNotNone(match)
        self.assertEqual(len(match.groups()), 7)
        self.assertEqual(match[1], "2024-12-23T00:00:00")
        self.assertEqual(match[2], "MRAI_Guardian_QI_123456789012")
        self.assertEqual(match[3], "OOC_Stanton_3a_Lyria")
        self.assertEqual(match[4], "unknown")
        self.assertEqual(match[5], "2")
        self.assertEqual(match[6], "Player-123_Name")
        self.assertEqual(match[7], "Combat")
