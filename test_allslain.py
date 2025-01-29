#!/usr/bin/env python3
import unittest

from allslain import (
    clean_location,
    clean_name,
    find_game_log,
    get_vehicle,
    LOG_ENCODING,
    LOG_NEWLINE,
    RE_VEHICLE_NAME,
    remove_id,
)


@unittest.skipUnless(find_game_log(), "No game logs are available.")
class TestLogReading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = find_game_log()

    def test_log_decode(self):
        with open(self.log, "r", encoding=LOG_ENCODING, newline=LOG_NEWLINE) as f:
            f.read()


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
    def test_pu_ai(self):
        result = RE_VEHICLE_NAME.match(
            "CNOU_Mustang_Delta_PU_AI_NineTails_123456789012"
        )
        self.assertEqual(len(result.groups()), 3)
        self.assertEqual(result[1], "CNOU_Mustang_Delta")
        self.assertEqual(result[2], "PU_AI_NineTails")
        self.assertEqual(result[3], "123456789012")

    def test_regular(self):
        result = RE_VEHICLE_NAME.match("CNOU_Mustang_Delta_123456789012")
        self.assertEqual(len(result.groups()), 3)
        self.assertEqual(result[1], "CNOU_Mustang_Delta")
        self.assertIsNone(result[2])
        self.assertEqual(result[3], "123456789012")

    def test_id_len_13(self):
        result = RE_VEHICLE_NAME.match("MISC_Freelancer_MAX_PU_AI_CRIM_1234567890123")
        self.assertEqual(len(result.groups()), 3)
        self.assertEqual(result[1], "MISC_Freelancer_MAX")
        self.assertEqual(result[2], "PU_AI_CRIM")
        self.assertEqual(result[3], "1234567890123")


class TestGetVehicleNameFunction(unittest.TestCase):
    def test_get_vehicle_salvage(self):
        result = get_vehicle("ANVL_Arrow_Unmanned_Salvage_123456789012")
        self.assertEqual(result[0], "Anvil Arrow (Salvage)")
        self.assertEqual(result[1], True)

    def test_get_vehicle_debris(self):
        result = get_vehicle(
            "SCItem_Debris_123456789012_RSI_Constellation_Andromeda_123456789012"
        )
        self.assertEqual(result[0], "RSI Constellation Andromeda (Debris)")
        self.assertEqual(result[1], True)

    def test_get_vehicle_with_type_debris(self):
        result = get_vehicle(
            "SCItem_Debris_123456789012_RSI_Scorpius_Antares_PU_AI_CRIM_123456789012"
        )
        self.assertEqual(result[0], "RSI Scorpius Antares (Debris)")
        self.assertEqual(result[1], True)

    def test_get_non_vehicle(self):
        result = get_vehicle("invalidvehicle_123456789012")
        self.assertEqual(result[0], "invalidvehicle_123456789012")
        self.assertEqual(result[1], False)


class TestGetLocationName(unittest.TestCase):
    def test_remove_at(self):
        result = clean_location("@Stanton1_Transfer")
        self.assertEqual(result[0], "at")
        self.assertEqual(result[1], "Everus Harbor")

    def test_bunker(self):
        result = clean_location("ObjectContainer-ugf_lta_a_0003")
        self.assertEqual(result[0], "in a")
        self.assertEqual(result[1], "Bunker")

    def test_drug_bunker(self):
        result = clean_location("ObjectContainer-ugf_lta_a_0004_drugs")
        self.assertEqual(result[0], "in a")
        self.assertEqual(result[1], "Drug Bunker")


class TestGetHazardNames(unittest.TestCase):
    def test_radiation_hazard(self):
        result = clean_name("Radiation_Hazard")
        self.assertEqual(result[0], "Radiation Hazard")
        self.assertEqual(result[1], 1)

    def test_water_hazard(self):
        result = clean_name("Water_Hazard")
        self.assertEqual(result[0], "Water Hazard")
        self.assertEqual(result[1], 1)

    def test_numbered_hazard(self):
        result = clean_name("Hazard-003")
        self.assertEqual(result[0], "Environmental Hazard")
        self.assertEqual(result[1], 1)


if __name__ == "__main__":
    unittest.main()
