import unittest

from allslain import *


class TestNameFunctions(unittest.TestCase):

    def test_npc_archetypes(self):
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


if __name__ == "__main__":
    unittest.main()
