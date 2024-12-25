#!/usr/bin/env python3
import unittest

from allslain import LOG_INCAP_CAUSE
from log_parser import SCLogParser


class TestLogKillRegex(unittest.TestCase):
    def test_log_kill_regex(self):
        result = SCLogParser.find_match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Actor Death> CActor::Kill: 'PU_Human-NineTails-Grunt-Male-Grunt_10_123456789012' [123456789012] in zone 'OOC_Stanton_3a_Lyria' killed by 'PlayerName' [123456789012] using 'GATS_BallisticGatling_Mounted_S1_123456789012' [Class GATS_BallisticGatling_Mounted_S1] with damage type 'Bullet' from direction x: -0.123456, y: -0.123456, z: 0.123456 [Team_ActorTech][Actor]"
        )["KILLP"]
        self.assertEqual(len(result.groups()), 7)
        self.assertEqual(result[1], "2024-12-23T00:00:00")
        self.assertEqual(
            result[2], "PU_Human-NineTails-Grunt-Male-Grunt_10_123456789012"
        )
        self.assertEqual(result[3], "OOC_Stanton_3a_Lyria")
        self.assertEqual(result[4], "PlayerName")
        self.assertEqual(result[5], "GATS_BallisticGatling_Mounted_S1")
        self.assertEqual(result[6], "Bullet")
        self.assertEqual(result[7], "x: -0.123456, y: -0.123456, z: 0.123456")


class TestLogVKillRegex(unittest.TestCase):
    def test_log_vkill_regex(self):
        result = SCLogParser.find_match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle 'MRAI_Guardian_QI_123456789012' [123456789012] in zone 'OOC_Stanton_3a_Lyria' [pos x: -200000.000000, y: 100000.000000, z: 60000.000000 vel x: 0.000000, y: 0.000000, z: 0.000000] driven by 'unknown' [0] advanced from destroy level 1 to 2 caused by 'PlayerName' [123456789012] with 'Combat' [Team_VehicleFeatures][Vehicle]"
        )["KILLV"]
        self.assertEqual(len(result.groups()), 7)
        self.assertEqual(result[1], "2024-12-23T00:00:00")
        self.assertEqual(result[2], "MRAI_Guardian_QI_123456789012")
        self.assertEqual(result[3], "OOC_Stanton_3a_Lyria")
        self.assertEqual(result[4], "unknown")
        self.assertEqual(result[5], "2")
        self.assertEqual(result[6], "PlayerName")
        self.assertEqual(result[7], "Combat")


class TestLogRespawnRegex(unittest.TestCase):
    def test_log_respawn_regex(self):
        result = SCLogParser.find_match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Corpse> Player 'PlayerName' <remote client>: DoesLocationContainHospital: Searching landing zone location \"@Stanton1b_Aberdeen_Prison\" for the closest hospital. [Team_ActorTech][Actor]"
        )["RESPAWN"]
        self.assertEqual(len(result.groups()), 3)
        self.assertEqual(result[1], "2024-12-23T00:00:00")
        self.assertEqual(result[2], "PlayerName")
        self.assertEqual(result[3], "@Stanton1b_Aberdeen_Prison")


class TestLogIncapRegexSingleCause(unittest.TestCase):
    def setUp(self):
        self.result = SCLogParser.find_match(
            "<2024-12-18T00:00:00.000Z> Logged an incap.! nickname: PlayerName-_012345, causes: [Bleed (0.350000 damage)]"
        )["INCAP"]
        self.cause = LOG_INCAP_CAUSE.findall(self.result[3])

    def test_incap(self):
        self.assertEqual(len(self.result.groups()), 3)
        self.assertEqual(self.result[1], "2024-12-18T00:00:00")
        self.assertEqual(self.result[2], "PlayerName-_012345")
        self.assertEqual(self.result[3], "Bleed (0.350000 damage)")

    def test_incap_cause(self):
        self.assertEqual(self.cause[0][0], "Bleed")
        self.assertEqual(self.cause[0][1], "0.350000")


class TestLogIncapRegexMultipleCause(unittest.TestCase):
    def setUp(self):
        self.result = SCLogParser.find_match(
            "<2024-12-22T00:00:00.000Z> Logged an incap.! nickname: Player-123_Name, causes: [DepressurizationDamage (3.999999 damage), SuffocationDamage (1.999999 damage)]"
        )["INCAP"]
        self.cause = LOG_INCAP_CAUSE.findall(self.result[3])

    def test_incap(self):
        self.assertEqual(len(self.result.groups()), 3)
        self.assertEqual(self.result[1], "2024-12-22T00:00:00")
        self.assertEqual(self.result[2], "Player-123_Name")
        self.assertEqual(
            self.result[3],
            "DepressurizationDamage (3.999999 damage), SuffocationDamage (1.999999 damage)",
        )

    def test_incap_cause(self):
        self.assertEqual(self.cause[0][0], "DepressurizationDamage")
        self.assertEqual(self.cause[0][1], "3.999999")
        self.assertEqual(self.cause[1][0], "SuffocationDamage")
        self.assertEqual(self.cause[1][1], "1.999999")


if __name__ == "__main__":
    unittest.main()
