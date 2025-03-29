import re

from colorize import Color
from functions import clean_location, clean_name, get_vehicle
from handlers.compatibility import CompatibleAll

from .handler import PlayerLookupHandler


def format_vehicle(vehicle_name: str, vehicle_type: str | None):
    return f"{Color.CYAN(vehicle_type, True) + ' ' if vehicle_type else ''}{Color.GREEN(vehicle_name)}"


class KillV(CompatibleAll, PlayerLookupHandler):
    header = ("VKILL", Color.RED, False)
    pattern = re.compile(
        r"\[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([\w-]+)' \[\d+\] in zone '([\w-]+)' \[pos.*\] driven by '([\w-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([\w-]+)' \[[0-9_]+\] with '([A-Za-z]+)' "
    )

    def format(self, data) -> str:
        # Always a vehicle
        vehicle_name, vehicle_type, found = get_vehicle(data[1])
        if found:
            vehicle = format_vehicle(vehicle_name, vehicle_type)
        else:
            # clean up the vehicle name if not in db
            vehicle = Color.GREEN(clean_name(data[1])[0])

        lp, location, _ = clean_location(data[2])

        # always unknown since 4.0?
        driver, _ = clean_name(data[3])
        if driver == "unknown":
            driver = ""
        else:
            driver = " driven by " + Color.GREEN(driver)

        kill_type = (
            Color.YELLOW("disabled") if data[4] == "1" else Color.RED("destroyed")
        )

        # ship, player, or unknown
        vehicle_name2, vehicle_type2, found2 = get_vehicle(data[5])
        if found2:
            killer_text = format_vehicle(vehicle_name2, vehicle_type2)
        else:
            killer_text = self.format_player(*clean_name(data[5]))

        if data[6] == "SelfDestruct":
            # SelfDestruct always destroys the vehicle
            if found2:
                # destruction caused by ship
                # TODO A/An
                return f"A {vehicle} {Color.RED('self destructed')} {lp} {Color.YELLOW(location)}"
            # caused by player
            return f"{killer_text} {Color.RED('self destructed')} a {vehicle} {lp} {Color.YELLOW(location)}"

        # Combat, SelfDestruct, Collision, BoundaryViolation, Ejection, Hazard, GameRules
        match data[6]:
            case "Combat":
                dmgtypep = "in"
            case "Ejection":
                dmgtypep = "with an"
            case _:
                dmgtypep = "with a"

        dmgtype = Color.CYAN(data[6])

        return f"{killer_text} {kill_type} a {vehicle}{driver} {dmgtypep} {dmgtype} {lp} {Color.YELLOW(location)}"
