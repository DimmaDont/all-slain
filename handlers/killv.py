import re

from colorize import Color
from functions import clean_location, clean_name, get_vehicle

from .handler import Handler


class KillV(Handler):
    header = ("VKILL", Color.RED, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([\w-]+)' \[\d+\] in zone '([\w-]+)' \[pos.*\] driven by '([\w-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([\w-]+)' \[[0-9_]+\] with '([A-Za-z]+)' \[Team_VehicleFeatures\]\[Vehicle\]"
    )

    def format(self, log: re.Match) -> str:
        # log[2] and log[6] are vehicles, or if the event is a collision, npc/player entities
        vehicle_name, found = get_vehicle(log[2])
        vehicle = Color.GREEN(vehicle_name if found else clean_name(log[2])[0])
        lp, location, _ = clean_location(log[3])
        driver, _ = clean_name(log[4])
        if driver == "unknown":
            driver = ""
        else:
            driver = Color.GREEN(driver) + " in a "
        kill_type = (
            Color.YELLOW("disabled") if log[5] == "1" else Color.RED("destroyed")
        )

        vehicle_name2, found2 = get_vehicle(log[6])
        killer = Color.GREEN(vehicle_name2 if found2 else clean_name(log[6])[0])
        dmgtype = Color.CYAN(log[7])
        return f"{killer} {kill_type} a {driver}{vehicle} with {dmgtype} {lp} {Color.YELLOW(location)}"
