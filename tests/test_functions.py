import unittest

from functions import RE_VEHICLE_NAME, get_entity, get_location, get_vehicle, strip_id


class TestCleanNameFunction(unittest.TestCase):
    def test_clean_name_debris(self):
        result, _ = get_entity("SCItem_Debris_123456789012")
        self.assertEqual(result, "Debris")


class TestRemoveIdFunction(unittest.TestCase):
    def test_remove_id_tooshort(self):
        result = strip_id("ASDF1234_1234")
        self.assertEqual(result, "ASDF1234_1234")

    def test_remove_id_alpha(self):
        result = strip_id("ASDF1234_a1234")
        self.assertEqual(result, "ASDF1234_a1234")

    def test_remove_id(self):
        result = strip_id("ASDF1234_123456789012")
        self.assertEqual(result, "ASDF1234")


class TestVehicleNameRegex(unittest.TestCase):
    def test_pu_ai(self):
        match = RE_VEHICLE_NAME.match("CNOU_Mustang_Delta_PU_AI_NineTails_123456789012")
        assert match
        self.assertEqual(len(match.groups()), 2)
        self.assertEqual(match[1], "CNOU_Mustang_Delta")
        self.assertEqual(match[2], "PU_AI_NineTails")

    def test_regular(self):
        match = RE_VEHICLE_NAME.match("CNOU_Mustang_Delta_123456789012")
        assert match
        self.assertEqual(len(match.groups()), 2)
        self.assertEqual(match[1], "CNOU_Mustang_Delta")
        self.assertIsNone(match[2])

    def test_id_len_13(self):
        match = RE_VEHICLE_NAME.match("MISC_Freelancer_MAX_PU_AI_CRIM_1234567890123")
        assert match
        self.assertEqual(len(match.groups()), 2)
        self.assertEqual(match[1], "MISC_Freelancer_MAX")
        self.assertEqual(match[2], "PU_AI_CRIM")

    def test_ship_debris(self):
        match = RE_VEHICLE_NAME.findall(
            "SCItem_Debris_1234567890123_ANVL_Hornet_F7CR_PU_AI_CRIM_1234567890123"
        )
        self.assertEqual(len(match), 2)
        self.assertEqual(match[0][0], "SCItem_Debris")
        self.assertEqual(match[0][1], "")
        self.assertEqual(match[1][0], "ANVL_Hornet_F7CR")
        self.assertEqual(match[1][1], "PU_AI_CRIM")


class TestGetVehicleNameFunction(unittest.TestCase):
    def test_get_vehicle_salvage(self):
        result = get_vehicle("ANVL_Arrow_Unmanned_Salvage_123456789012")
        self.assertEqual(result[0], "Anvil Arrow (Salvage)")
        self.assertIsNone(result[1])
        self.assertEqual(result[2], True)

    def test_get_vehicle_debris(self):
        result = get_vehicle(
            "SCItem_Debris_123456789012_RSI_Constellation_Andromeda_123456789012"
        )
        self.assertEqual(result[0], "RSI Constellation Andromeda (Debris)")
        self.assertIsNone(result[1])
        self.assertEqual(result[2], True)

    def test_get_unknown_vehicle_debris(self):
        result = get_vehicle("SCItem_Debris_123456789012_MFG_UnknownShip_123456789012")
        self.assertEqual(result[0], "MFG_UnknownShip (Debris)")
        self.assertIsNone(result[1])
        self.assertEqual(result[2], False)

    def test_get_vehicle_with_type_debris(self):
        result = get_vehicle(
            "SCItem_Debris_123456789012_RSI_Scorpius_Antares_PU_AI_CRIM_1234567890123"
        )
        self.assertEqual(result[0], "RSI Scorpius Antares (Debris)")
        self.assertEqual(result[1], "Criminal")
        self.assertEqual(result[2], True)

    def test_get_non_vehicle(self):
        result = get_vehicle("invalidvehicle_123456789012")
        self.assertEqual(result[0], "invalidvehicle_123456789012")
        self.assertIsNone(result[1])
        self.assertEqual(result[2], False)


class TestGetLocationName(unittest.TestCase):
    def test_remove_at(self):
        result = get_location("@Stanton1_Transfer")
        self.assertEqual(result[0], "at")
        self.assertEqual(result[1], "Everus Harbor")

    def test_bunker(self):
        result = get_location("ObjectContainer-ugf_lta_a_0003")
        self.assertEqual(result[0], "in a")
        self.assertEqual(result[1], "Bunker")

    def test_drug_bunker(self):
        result = get_location("ObjectContainer-ugf_lta_a_0004_drugs")
        self.assertEqual(result[0], "in a")
        self.assertEqual(result[1], "Drug Bunker")


class TestGetHazardNames(unittest.TestCase):
    def test_radiation_hazard(self):
        result = get_entity("Radiation_Hazard")
        self.assertEqual(result[0], "Radiation Hazard")
        self.assertEqual(result[1], True)

    def test_water_hazard(self):
        result = get_entity("Water_Hazard")
        self.assertEqual(result[0], "Water Hazard")
        self.assertEqual(result[1], True)

    def test_numbered_hazard(self):
        result = get_entity("Hazard-003")
        self.assertEqual(result[0], "Environmental Hazard")
        self.assertEqual(result[1], True)


if __name__ == "__main__":
    unittest.main()
