#!/usr/bin/env python3
import unittest

from allslain import (
    clean_name,
    remove_id,
    LOG_KILL,
    LOG_RESPAWN,
    LOG_VEHICLE_KILL,
)


class TestNameFunctions(unittest.TestCase):

    def test_clean_name(self):
        result, _ = clean_name(
            "NPC_Archetypes-Human-Blacjac-Guard-Male-Heavy_01_123456789012"
        )
        self.assertEqual(result, "Blacjac_Guard_Male_Heavy")

        result, _ = clean_name(
            "NPC_Archetypes-Male-Human-Cheesecake_soldier_123456789012"
        )
        self.assertEqual(result, "Cheesecake_soldier")

        result, _ = clean_name(
            "NPC_Archetypes-Male-Human-distributioncentre_soldier_123456789012"
        )
        self.assertEqual(result, "distributioncentre_soldier")

        result, _ = clean_name(
            "NPC_Archetypes-Male-Human-Civilians-Utilitarian-Technician_Utilitarian_01_123456789012"
        )
        self.assertEqual(result, "Technician_Utilitarian_01")

        result, _ = clean_name(
            "NPC_Archetypes-Male-Human-Guards_UGF_BlacjacSecurity_Light_123456789012"
        )
        self.assertEqual(result, "Guards_UGF_BlacjacSecurity_Light")

        result, _ = clean_name("PU_Human-Faction-Guard-Male-Grunt_02_123456789012")
        self.assertEqual(result, "Faction_Guard_Male_Grunt")

        result, _ = clean_name(
            "PU_Human_Enemy_GroundCombat_NPC_Faction_Class_123456789012"
        )
        self.assertEqual(result, "Faction_Class")

        result, _ = clean_name("Kopion_Headhunter_pet_123456789012")
        self.assertEqual(result, "Kopion")

        result, _ = clean_name("AIModule_Unmanned_PU_SecurityNetwork_123456789012")
        self.assertEqual(result, "NPC Security")

        result, _ = clean_name(
            "PU_Human-Populace-Civilian-Female-Pyro-Frontier_01_123456789012"
        )
        self.assertEqual(result, "Populace_Civilian_Female_Pyro")

        result, _ = clean_name("PU_Pilots-Human-Criminal-Gunner_Light_123456789012")
        self.assertEqual(result, "Pilot_Criminal_Gunner_Light")

    def test_remove_id(self):
        result = remove_id("ASDF1234_1234")
        self.assertEqual(result, "ASDF1234_1234")

        result = remove_id("ASDF1234_a1234")
        self.assertEqual(result, "ASDF1234_a1234")

        result = remove_id("ASDF1234_123456789012")
        self.assertEqual(result, "ASDF1234")

    def test_log_kill_regex(self):
        result = LOG_KILL.match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Actor Death> CActor::Kill: 'PU_Human-NineTails-Grunt-Male-Grunt_10_123456789012' [123456789012] in zone 'OOC_Stanton_3a_Lyria' killed by 'PlayerName' [123456789012] using 'GATS_BallisticGatling_Mounted_S1_123456789012' [Class GATS_BallisticGatling_Mounted_S1] with damage type 'Bullet' from direction x: -0.123456, y: -0.123456, z: 0.123456 [Team_ActorTech][Actor]"
        )
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

    def test_log_vkill_regex(self):
        result = LOG_VEHICLE_KILL.match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle 'MRAI_Guardian_QI_123456789012' [123456789012] in zone 'OOC_Stanton_3a_Lyria' [pos x: -200000.000000, y: 100000.000000, z: 60000.000000 vel x: 0.000000, y: 0.000000, z: 0.000000] driven by 'unknown' [0] advanced from destroy level 1 to 2 caused by 'PlayerName' [123456789012] with 'Combat' [Team_VehicleFeatures][Vehicle]"
        )
        self.assertEqual(len(result.groups()), 7)
        self.assertEqual(result[1], "2024-12-23T00:00:00")
        self.assertEqual(result[2], "MRAI_Guardian_QI_123456789012")
        self.assertEqual(result[3], "OOC_Stanton_3a_Lyria")
        self.assertEqual(result[4], "unknown")
        self.assertEqual(result[5], "2")
        self.assertEqual(result[6], "PlayerName")
        self.assertEqual(result[7], "Combat")

    def test_log_respawn_regex(self):
        result = LOG_RESPAWN.match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Corpse> Player 'PlayerName' <remote client>: DoesLocationContainHospital: Searching landing zone location \"@Stanton1b_Aberdeen_Prison\" for the closest hospital. [Team_ActorTech][Actor]"
        )
        self.assertEqual(len(result.groups()), 3)
        self.assertEqual(result[1], "2024-12-23T00:00:00")
        self.assertEqual(result[2], "PlayerName")
        self.assertEqual(result[3], "@Stanton1b_Aberdeen_Prison")


if __name__ == "__main__":
    unittest.main()
