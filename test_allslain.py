#!/usr/bin/env python3
import unittest

from allslain import (
    clean_name,
    get_vehicle,
    LOG_INCAP_CAUSE,
    LOG_INCAP,
    LOG_JUMP,
    LOG_KILL,
    LOG_RESPAWN,
    LOG_VEHICLE_KILL,
    RE_VEHICLE_NAME,
    remove_id,
)


class TestCleanNameFunction(unittest.TestCase):
    def test_clean_name_npc_arch_blacjac(self):
        result, _ = clean_name(
            "NPC_Archetypes-Human-Blacjac-Guard-Male-Heavy_01_123456789012"
        )
        self.assertEqual(result, "Blacjac_Guard_Male_Heavy")

    def test_clean_name_npc_arch_cheesecake(self):
        result, _ = clean_name(
            "NPC_Archetypes-Male-Human-Cheesecake_soldier_123456789012"
        )
        self.assertEqual(result, "Cheesecake_soldier")

    def test_clean_name_npc_arch_distro(self):
        result, _ = clean_name(
            "NPC_Archetypes-Male-Human-distributioncentre_soldier_123456789012"
        )
        self.assertEqual(result, "distributioncentre_soldier")

    def test_clean_name_npc_arch_civ(self):
        result, _ = clean_name(
            "NPC_Archetypes-Male-Human-Civilians-Utilitarian-Technician_Utilitarian_01_123456789012"
        )
        self.assertEqual(result, "Technician_Utilitarian_01")

    def test_clean_name_npc_arch_ugf_blacjac(self):
        result, _ = clean_name(
            "NPC_Archetypes-Male-Human-Guards_UGF_BlacjacSecurity_Light_123456789012"
        )
        self.assertEqual(result, "Guards_UGF_BlacjacSecurity_Light")

    def test_clean_name_pu_human_faction(self):
        result, _ = clean_name("PU_Human-Faction-Guard-Male-Grunt_02_123456789012")
        self.assertEqual(result, "Faction_Guard_Male_Grunt")

    def test_clean_name_pu_human_enemy(self):
        result, _ = clean_name(
            "PU_Human_Enemy_GroundCombat_NPC_Faction_Class_123456789012"
        )
        self.assertEqual(result, "Faction_Class")

    def test_clean_name_kopion(self):
        result, _ = clean_name("Kopion_Headhunter_pet_123456789012")
        self.assertEqual(result, "Kopion")

    def test_clean_name_aimodule(self):
        result, _ = clean_name("AIModule_Unmanned_PU_SecurityNetwork_123456789012")
        self.assertEqual(result, "NPC Security")

    def test_clean_name_pu_human_populace(self):
        result, _ = clean_name(
            "PU_Human-Populace-Civilian-Female-Pyro-Frontier_01_123456789012"
        )
        self.assertEqual(result, "Populace_Civilian_Female_Pyro")

    def test_clean_name_pu_pilots(self):
        result, _ = clean_name("PU_Pilots-Human-Criminal-Gunner_Light_123456789012")
        self.assertEqual(result, "Pilot_Criminal_Gunner_Light")


class TestRemoveIdFunction(unittest.TestCase):
    def test_remove_id_tooshort(self):
        result = remove_id("ASDF1234_1234")
        self.assertEqual(result, "ASDF1234_1234")

    def test_remove_id_alpha(self):
        result = remove_id("ASDF1234_a1234")
        self.assertEqual(result, "ASDF1234_a1234")

    def test_remove_id(self):
        result = remove_id("ASDF1234_123456789012")
        self.assertEqual(result, "ASDF1234")


class TestLogKillRegex(unittest.TestCase):
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


class TestLogVKillRegex(unittest.TestCase):
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


class TestLogRespawnRegex(unittest.TestCase):
    def test_log_respawn_regex(self):
        result = LOG_RESPAWN.match(
            "<2024-12-23T00:00:00.000Z> [Notice] <Corpse> Player 'PlayerName' <remote client>: DoesLocationContainHospital: Searching landing zone location \"@Stanton1b_Aberdeen_Prison\" for the closest hospital. [Team_ActorTech][Actor]"
        )
        self.assertEqual(len(result.groups()), 3)
        self.assertEqual(result[1], "2024-12-23T00:00:00")
        self.assertEqual(result[2], "PlayerName")
        self.assertEqual(result[3], "@Stanton1b_Aberdeen_Prison")


class TestVehicleNameRegex(unittest.TestCase):
    def test_re_vehicle_name_pu_ai(self):
        result = RE_VEHICLE_NAME.match(
            "CNOU_Mustang_Delta_PU_AI_NineTails_123456789012"
        )
        self.assertEqual(len(result.groups()), 3)
        self.assertEqual(result[1], "CNOU_Mustang_Delta")
        self.assertEqual(result[2], "PU_AI_NineTails")
        self.assertEqual(result[3], "123456789012")

    def test_re_vehicle_name_regular(self):
        result = RE_VEHICLE_NAME.match("CNOU_Mustang_Delta_123456789012")
        self.assertEqual(len(result.groups()), 3)
        self.assertEqual(result[1], "CNOU_Mustang_Delta")
        self.assertIsNone(result[2])
        self.assertEqual(result[3], "123456789012")

    def test_re_vehicle_name_salvage(self):
        result = RE_VEHICLE_NAME.match("ANVL_Arrow_Unmanned_Salvage_123456789012")
        self.assertEqual(len(result.groups()), 3)
        self.assertEqual(result[1], "ANVL_Arrow")
        self.assertEqual(result[2], "Unmanned_Salvage")
        self.assertEqual(result[3], "123456789012")


class TestGetVehicleNameFunction(unittest.TestCase):
    def test_get_vehicle_salvage(self):
        result = get_vehicle("ANVL_Arrow_Unmanned_Salvage_123456789012")
        self.assertEqual(result, "Anvil Arrow (Salvage)")


class TestLogIncapRegexSingleCause(unittest.TestCase):
    def setUp(self):
        self.result = LOG_INCAP.match(
            "<2024-12-18T00:00:00.000Z> Logged an incap.! nickname: PlayerName-_012345, causes: [Bleed (0.350000 damage)]"
        )
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
        self.result = LOG_INCAP.match(
            "<2024-12-22T00:00:00.000Z> Logged an incap.! nickname: Player-123_Name, causes: [DepressurizationDamage (3.999999 damage), SuffocationDamage (1.999999 damage)]"
        )
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


class TestLogJump(unittest.TestCase):
    def test_log_jump_regex(self):
        result = LOG_JUMP.match(
            "<2024-12-22T00:00:00.000Z> [Notice] <Changing Solar System> CEntityComponentJumpTunnelHost::RmChangeSolarSystem | CL12345 NOT AUTH | Pyro | JumpTunnelHost_123456789012 [123456789012] | Client entity Player-123_Name was found in tunnel zone JumpTunnelHost_123456789012, changing system from Pyro to Stanton [Team_VehicleFeatures][JumpSystem]"
        )
        self.assertIsNotNone(result)
        self.assertEqual(len(result.groups()), 4)
        self.assertEqual(result[1], "2024-12-22T00:00:00")
        self.assertEqual(result[2], "Player-123_Name")
        self.assertEqual(result[3], "Pyro")
        self.assertEqual(result[4], "Stanton")


if __name__ == "__main__":
    unittest.main()
