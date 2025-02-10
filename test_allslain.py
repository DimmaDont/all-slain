import unittest

from allslain import AllSlain
from functions import RE_VEHICLE_NAME, clean_location, clean_name, get_vehicle, strip_id


@unittest.skipUnless(AllSlain.find_game_log(), "No game logs are available.")
class TestLogReading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = AllSlain.find_game_log()

    def test_log_decode(self):
        with open(
            self.log, "r", encoding=AllSlain.LOG_ENCODING, newline=AllSlain.LOG_NEWLINE
        ) as f:
            f.read()


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
