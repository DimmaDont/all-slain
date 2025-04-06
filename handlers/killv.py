import re

from colorize import Color
from functions import get_article, get_entity, get_location, get_vehicle
from functions_color import color_location, color_vehicle, not_found
from handlers.compatibility import CompatibleAll

from .handler import PlayerLookupHandler


class KillV(CompatibleAll, PlayerLookupHandler):
    header = ("VKILL", Color.RED, False)
    pattern = re.compile(
        r"\[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([\w-]+)' \[\d+\] in zone '([\w-]+)' \[pos.*\] driven by '([\w-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([\w-]+)' \[[0-9_]+\] with '([A-Za-z]+)' "
    )

    def format(self, data) -> str:
        # Always a vehicle
        vehicle_name, vehicle_type, found = get_vehicle(data[1])
        vehicle = color_vehicle(vehicle_name, vehicle_type)
        if not found:
            vehicle = not_found(vehicle)

        lp, location, location_type = get_location(data[2])

        location_str = color_location(location, location_type)

        # always unknown since 4.0?
        driver, _ = get_entity(data[3])
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
            killer_str = color_vehicle(vehicle_name2, vehicle_type2)
        else:
            killer_str = self.format_player(*get_entity(data[5]))

        vehicle_article = get_article(vehicle)

        if data[6] == "SelfDestruct":
            # SelfDestruct always destroys the vehicle
            if found2:
                # destruction caused by ship
                return f"{vehicle_article.title()} {vehicle} {Color.RED('self destructed')} {lp} {location_str}"
            # caused by player
            return f"{killer_str} {Color.RED('self destructed')} a {vehicle} {lp} {location_str}"

        # Combat, SelfDestruct, Collision, BoundaryViolation, Ejection, Hazard, GameRules
        match data[6]:
            case "Combat":
                dmgtypep = "in"
            case "Ejection":
                dmgtypep = "with an"
            case _:
                dmgtypep = "with a"

        dmgtype = Color.CYAN(data[6])

        return f"{killer_str} {kill_type} {vehicle_article} {vehicle}{driver} {dmgtypep} {dmgtype} {lp} {location_str}"
