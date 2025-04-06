from __future__ import annotations

from typing import TYPE_CHECKING

from colorize import Color
from functions import LocationType


if TYPE_CHECKING:
    from data_providers.provider import Org, Player


def not_found(s: str) -> str:
    return f"{Color.RED('(?)')} {s}"


def color_cause(cause: str) -> str:
    return Color.CYAN(cause)


def color_info(info: str) -> str:
    return Color.CYAN(info)


def color_location(location_name: str, location_type: LocationType) -> str:
    if location_type == LocationType.UNKNOWN:
        return not_found(Color.YELLOW(location_name))
    return Color.YELLOW(location_name)


def color_player_default(player: str | Player) -> str:
    return Color.GREEN(player)


def color_player_npc(name: str) -> str:
    return Color.BLACK(name, True)


def color_player_with_org(player: Player, main_org: str | Org) -> str:
    return f"{color_player_default(player)} {Color.BLACK('(', True)}{main_org}{Color.BLACK(')', True)}"


def color_vehicle(
    name: str, vtype: str | None = None, as_location: bool = False
) -> str:
    vehicle_type_str = Color.CYAN(vtype, True) + " " if vtype is not None else ""
    vehicle_name_str = Color["YELLOW" if as_location else "GREEN"](name)
    return vehicle_type_str + vehicle_name_str
