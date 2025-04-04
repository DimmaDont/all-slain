import re

from colorize import Color
from functions import strip_id
from handlers.compatibility import CompatibleAll

from .handler import Handler


# TODO:
# 890
# Carrack
# Terrapin Medic


MEDICAL_BED_NAMES = {
    "bed_hospital": "Hospital Bed",
    "Bed_Single": "Medical Bed",
    # Cutlass Red
    "DRAK_Cutlass_Red_Med_Bed_right": "Right Medical Bed",
    "DRAK_Cutlass_Red_Med_Bed_Left": "Left Medical Bed",
    # Polaris
    # "Bed_Single_Medical_RSI_T2_Left",
    # "Bed_Single_Medical_RSI_T2_Left-001",
    # "Bed_Single_Medical_RSI_T2_Left-002",
    # "Bed_Single_Medical_RSI_T2_Left-003",
}


def get_bed_name(med_bed_name: str) -> str:
    for k, v in MEDICAL_BED_NAMES.items():
        if k in med_bed_name:
            return v
    return med_bed_name


SHIPS = {
    "RSI_URSA_Medivac": "RSI Ursa Medivac",
    "DRAK_Cutlass_Red": "Drake Cutlass Red",
    "ANVL_C8R_Pisces_Rescue": "Anvil C8R Pisces Rescue",
    "RSI_Polaris": "RSI Polaris",
}


class MedBedHeal(CompatibleAll, Handler):
    header = ("MED BED", Color.RED, False)
    pattern = re.compile(
        r"\[Notice\] <MED BED HEAL> Actor: [\w-]+ \(Non-Authoritative CLIENT: [\w-]+\) \| \[CEntityComponentMedBed::HandleComponentEvent:\d+\] \| -> Perform surgery event \w+(?#Success), med bed name: ([\w-]+), vehicle name: ([@\w-]+), head: (true|false) torso: (true|false) leftArm: (true|false) rightArm: (true|false) leftLeg: (true|false) rightLeg: (true|false) \[Team_ActorFeatures\]\[Actor\]"
    )

    def format(self, data):
        med_bed_name = data[1]
        # med_bed_name = get_bed_name(data[1])
        if data[2] == "none":
            vehicle = ""
        else:
            vehicle_id = strip_id(data[2]).lstrip("@vehicle_Name")
            vehicle = " in a " + Color.YELLOW(SHIPS.get(vehicle_id, vehicle_id))

        # Event fires when a limb injury is treated or attempted to be treated.
        parts = {
            "head": data[3] == "true",
            "torso": data[4] == "true",
            "left arm": data[5] == "true",
            "right arm": data[6] == "true",
            "left leg": data[7] == "true",
            "right leg": data[8] == "true",
        }
        parts_healed = [Color.GREEN(k) for k, v in parts.items() if v]
        if not parts_healed:
            parts_healed_str = ""
        elif len(parts_healed) < 3:
            parts_healed_str = " and ".join(parts_healed) + " "
        else:
            parts_healed_str = (
                ", ".join(parts_healed[:-1]) + ", and " + parts_healed[-1] + " "
            )

        return f"Healed {parts_healed_str}in a {Color.YELLOW(med_bed_name)}{vehicle}"
