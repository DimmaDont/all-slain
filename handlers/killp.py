import re

from colorize import Color
from functions import clean_location, clean_name, clean_tool

from .handler import Handler


class KillP(Handler):
    header = ("KILL", Color.RED, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Actor Death> CActor::Kill: '([\w-]+)' \[\d+\] in zone '([\w-]+)' killed by '([\w-]+)' \[\d+\] using '([\w-]+)' \[Class ([\w-]+)\] with damage type '([A-Za-z]+)' from direction (.*) \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data) -> str:
        killed, is_killed_npc = clean_name(data[2])
        lp, location, location_type = clean_location(data[3])
        killer, is_killer_npc = clean_name(data[4])
        cause = clean_tool(data[6], data[4], data[2], data[7])
        if cause.startswith("suicide"):
            return f"{Color.GREEN(killer)} committed {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
        if is_killer_npc and is_killed_npc:
            if location_type == "ship":
                return f"{Color.BLACK(killer, bold = True)} killed {Color.BLACK(killed, bold = True)} {lp} {Color.YELLOW(location)} with a {Color.CYAN(cause)}"
            return f"{Color.BLACK(killer, bold = True)} killed {Color.BLACK(killed, bold = True)} with a {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
        if location_type == "ship":
            return f"{Color.GREEN(killer)} killed {Color.GREEN(killed)} {lp} {Color.YELLOW(location)} with a {Color.CYAN(cause)}"
        return f"{Color.GREEN(killer)} killed {Color.GREEN(killed)} with a {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"


class KillP402(KillP):
    # 4.0.2 no longer reports kills that don't involve the client player.
    def format(self, data) -> str:
        killed, _ = clean_name(data[2])
        lp, location, location_type = clean_location(data[3])
        is_ship = location_type == "ship"
        killer, _ = clean_name(data[4])
        cause = clean_tool(data[6], data[4], data[2], data[7])
        if cause.startswith("suicide"):
            return f"{Color.GREEN(killer)} committed {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
        if is_ship:
            return f"{Color.GREEN(killer)} killed {Color.GREEN(killed)} {lp} {Color.YELLOW(location)} with a {Color.CYAN(cause)}"
        return f"{Color.GREEN(killer)} killed {Color.GREEN(killed)} with a {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
