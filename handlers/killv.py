import re

from colorize import Color
from functions import clean_location, clean_name, get_vehicle

from .handler import Handler


def format_vehicle(vehicle_name: str, vehicle_type: str | None):
    return f"{Color.CYAN(vehicle_type, True) + ' ' if vehicle_type else ''}{Color.GREEN(vehicle_name)}"


class KillV(Handler):
    header = ("VKILL", Color.RED, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([\w-]+)' \[\d+\] in zone '([\w-]+)' \[pos.*\] driven by '([\w-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([\w-]+)' \[[0-9_]+\] with '([A-Za-z]+)' \[Team_VehicleFeatures\]\[Vehicle\]"
    )

    def format(self, data) -> str:
        # log[2] and log[6] are vehicles, or if the event is a collision, npc/player entities
        vehicle_name, vehicle_type, found = get_vehicle(data[2])
        if found:
            vehicle = format_vehicle(vehicle_name, vehicle_type)
        else:
            # clean up the vehicle name if not in db
            vehicle = Color.GREEN(clean_name(data[2])[0])

        lp, location, _ = clean_location(data[3])
        driver, _ = clean_name(data[4])
        if driver == "unknown":
            driver = ""
        else:
            driver = Color.GREEN(driver) + " in a "
        kill_type = (
            Color.YELLOW("disabled") if data[5] == "1" else Color.RED("destroyed")
        )

        vehicle_name2, vehicle_type2, found2 = get_vehicle(data[6])
        if found2:
            killer = format_vehicle(vehicle_name2, vehicle_type2)
        else:
            killer = clean_name(data[6])[0]
        dmgtype = Color.CYAN(data[7])
        return f"{killer} {kill_type} a {driver}{vehicle} with {dmgtype} {lp} {Color.YELLOW(location)}"
