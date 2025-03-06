import re

from colorize import Color
from functions import clean_location, clean_name, get_vehicle

from .handler import PlayerLookupHandler


def format_vehicle(vehicle_name: str, vehicle_type: str | None):
    return f"{Color.CYAN(vehicle_type, True) + ' ' if vehicle_type else ''}{Color.GREEN(vehicle_name)}"


class KillV(PlayerLookupHandler):
    header = ("VKILL", Color.RED, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([\w-]+)' \[\d+\] in zone '([\w-]+)' \[pos.*\] driven by '([\w-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([\w-]+)' \[[0-9_]+\] with '([A-Za-z]+)' \[Team_VehicleFeatures\]\[Vehicle\]"
    )

    def format(self, data) -> str:
        # Always a vehicle
        vehicle_name, vehicle_type, found = get_vehicle(data[2])
        if found:
            vehicle = format_vehicle(vehicle_name, vehicle_type)
        else:
            # clean up the vehicle name if not in db
            vehicle = Color.GREEN(clean_name(data[2])[0])

        lp, location, _ = clean_location(data[3])

        # always unknown since 4.0?
        driver, _ = clean_name(data[4])
        if driver == "unknown":
            driver = ""
        else:
            driver = " driven by " + Color.GREEN(driver)

        kill_type = (
            Color.YELLOW("disabled") if data[5] == "1" else Color.RED("destroyed")
        )

        # ship, player, or unknown
        vehicle_name2, vehicle_type2, found2 = get_vehicle(data[6])
        if found2:
            killer_text = format_vehicle(vehicle_name2, vehicle_type2)
        else:
            killer_text = self.format_player(*clean_name(data[6]))

        if data[7] == "SelfDestruct":
            # SelfDestruct always destroys the vehicle
            if found2:
                # destruction caused by ship
                # TODO A/An
                return f"A {vehicle} {Color.RED('self destructed')} {lp} {Color.YELLOW(location)}"
            # caused by player
            return f"{killer_text} {Color.RED('self destructed')} a {vehicle} {lp} {Color.YELLOW(location)}"

        # Combat, SelfDestruct, Collision, BoundaryViolation, Ejection, Hazard, GameRules
        match data[7]:
            case "Combat":
                dmgtypep = "in"
            case "Ejection":
                dmgtypep = "with an"
            case _:
                dmgtypep = "with a"

        dmgtype = Color.CYAN(data[7])

        return f"{killer_text} {kill_type} a {vehicle}{driver} {dmgtypep} {dmgtype} {lp} {Color.YELLOW(location)}"
