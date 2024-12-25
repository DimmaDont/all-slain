#!/usr/bin/env python3
import unittest

from allslain import (
    clean_name,
    get_vehicle,
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


if __name__ == "__main__":
    unittest.main()
