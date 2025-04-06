import re

from colorize import Color
from functions import LocationType, get_article, get_entity, get_item, get_location
from functions_color import color_cause, color_location

from .compatibility import CompatibleAll
from .handler import PlayerLookupHandler


# 4.0.2 no longer reports kills that don't involve the client player.


class KillP(CompatibleAll, PlayerLookupHandler):
    header = ("KILL", Color.RED, False)
    pattern = re.compile(
        r"\[Notice\] <Actor Death> CActor::Kill: '([\w-]+)' \[\d+\] in zone '([\w-]+)' killed by '([\w-]+)' \[\d+\] using '([\w-]+)' \[Class ([\w-]+)\] with damage type '([A-Za-z]+)' "
    )

    def format(self, data: re.Match[str]) -> str:
        killed, is_killed_npc = get_entity(data[1])
        lp, location, location_type = get_location(data[2])
        location_str = color_location(location, location_type)
        killer, is_killer_npc = get_entity(data[3])
        cause = get_item(data[5], data[3], data[1], data[6])
        cause_str = color_cause(cause)
        killer_str = self.format_player(killer, is_killer_npc)

        if cause.startswith("suicide"):
            return f"{killer_str} committed {cause_str} {lp} {location_str}"

        cause_a = get_article(cause)
        killed_str = self.format_player(killed, is_killed_npc)

        if location_type == LocationType.SHIP:
            return f"{killer_str} killed {killed_str} {lp} {location_str} with {cause_a} {cause_str}"
        return f"{killer_str} killed {killed_str} with {cause_a} {cause_str} {lp} {location_str}"
