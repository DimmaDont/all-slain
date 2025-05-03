import logging
import re

from ..colorize import Color
from ..functions import strip_id
from ..functions_color import color_vehicle, not_found
from .compatibility import CompatibleAll
from .handler import Handler


# TODO:
# 890
# Carrack


logger = logging.getLogger("allslain").getChild("medbed")


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
    # Terrapin Medic
    # "Bed_Single_Medical_Terrapin",
    # 890
    # "Bed_Single_Medical_890Jump-001"  # Hijacked 890
}


def get_bed_name(med_bed_name: str) -> str:
    for k, v in MEDICAL_BED_NAMES.items():
        if k in med_bed_name:
            return v
    return med_bed_name


SHIPS = {
    "ANVL_C8R_Pisces_Rescue": ("a", "Anvil C8R Pisces Rescue"),
    "ANVL_Terrapin_Medic": ("an", "Anvil Terrapin Medic"),
    "DRAK_Cutlass_Red": ("a", "Drake Cutlass Red"),
    "ORIG_890Jump_Hijacked": ("a", "Hijacked Origin 890 Jump"),
    "RSI_Polaris": ("an", "RSI Polaris"),
    # ursa is uppercase, unlike in ships.py
    "RSI_URSA_Medivac": ("an", "RSI Ursa Medivac"),
}


class MedBedHeal(CompatibleAll, Handler):
    header = ("MED BED", Color.RED, False)
    pattern = re.compile(
        r"\[Notice\] <MED BED HEAL> Actor: [\w-]+ \(Non-Authoritative CLIENT: [\w-]+\) \| \[CEntityComponentMedBed::HandleComponentEvent:\d+\] \| -> Perform surgery event \w+(?#Success), med bed name: ([\w-]+), vehicle name: ([@\w-]+), head: (true|false) torso: (true|false) leftArm: (true|false) rightArm: (true|false) leftLeg: (true|false) rightLeg: (true|false) \[Team_ActorFeatures\]\[Actor\]"
    )

    def format(self, data):
        med_bed_name = get_bed_name(data[1])
        if data[2] == "none":
            vehicle_str = ""
        else:
            vehicle_id = strip_id(data[2]).lstrip("@vehicle_Name")
            vehicle = SHIPS.get(vehicle_id, None)
            vehicle_str = (
                f" in {vehicle[0]} {color_vehicle(vehicle[1], as_location=True)}"
                if vehicle
                else f" in a {not_found(color_vehicle(vehicle_id, as_location=True))}"
            )

        logger.debug(data[1])
        logger.debug(data[2])

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

        return (
            f"Healed {parts_healed_str}in a {Color.YELLOW(med_bed_name)}{vehicle_str}"
        )
