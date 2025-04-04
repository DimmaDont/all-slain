import re

from colorize import Color
from functions import clean_location, clean_name, clean_tool
from handlers.compatibility import SinceV402, V401AndBelow

from .handler import PlayerLookupHandler


class KillP(V401AndBelow, PlayerLookupHandler):
    header = ("KILL", Color.RED, False)
    pattern = re.compile(
        r"\[Notice\] <Actor Death> CActor::Kill: '([\w-]+)' \[\d+\] in zone '([\w-]+)' killed by '([\w-]+)' \[\d+\] using '([\w-]+)' \[Class ([\w-]+)\] with damage type '([A-Za-z]+)' "
    )

    def format(self, data: re.Match[str]) -> str:
        killed, is_killed_npc = clean_name(data[1])
        lp, location, location_type = clean_location(data[2])
        killer, is_killer_npc = clean_name(data[3])
        cause = clean_tool(data[5], data[3], data[1], data[6])

        if cause.startswith("suicide"):
            return f"{Color.GREEN(killer)} committed {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"

        if is_killer_npc and is_killed_npc:
            if location_type == "ship":
                return f"{Color.BLACK(killer, bold = True)} killed {Color.BLACK(killed, bold = True)} {lp} {Color.YELLOW(location)} with a {Color.CYAN(cause)}"
            return f"{Color.BLACK(killer, bold = True)} killed {Color.BLACK(killed, bold = True)} with a {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"

        killer_text = self.format_player(killer, is_killer_npc)
        killed_text = self.format_player(killed, is_killed_npc)

        if location_type == "ship":
            return f"{killer_text} killed {killed_text} {lp} {Color.YELLOW(location)} with a {Color.CYAN(cause)}"
        return f"{killer_text} killed {killed_text} with a {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"


class KillP402(SinceV402, KillP):
    # 4.0.2 no longer reports kills that don't involve the client player.
    def format(self, data: re.Match[str]) -> str:
        killed, is_killed_npc = clean_name(data[1])
        lp, location, location_type = clean_location(data[2])
        killer, is_killer_npc = clean_name(data[3])
        cause = clean_tool(data[5], data[3], data[1], data[6])

        if cause.startswith("suicide"):
            return f"{Color.GREEN(killer)} committed {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"

        cause_a = (
            "an"
            if any(cause.lower().startswith(v) for v in ["a", "e", "i", "o", "u"])
            else "a"
        )

        killer_text = self.format_player(killer, is_killer_npc)
        killed_text = self.format_player(killed, is_killed_npc)

        if location_type == "ship":
            return f"{killer_text} killed {killed_text} {lp} {Color.YELLOW(location)} with {cause_a} {Color.CYAN(cause)}"
        return f"{killer_text} killed {killed_text} with {cause_a} {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
