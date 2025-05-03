import re
from enum import IntEnum
from typing import NamedTuple

from .data import (
    ACTORS,
    LOCATIONS,
    LOCATIONS_RESPAWN,
    SHIPS,
    VEHICLE_TYPES,
    WEAPONS_FPS,
    WEAPONS_SHIP,
)


# Things that rotate, like asteroids or station rings
# or oscillate
RE_SIMPLE = re.compile(r"(?:Rotation|Oscillation)Simple-\d{3}")


PATTERN_ID = re.compile(r"([\w-]+)_\d{12,}")


def strip_id(name: str) -> str:
    """
    Returns the entity name without its 12 or 13-digit id.

    Args:
        name: The full entity id

    Returns:
        A string with the id removed
    """
    if match := PATTERN_ID.match(name):
        return match.group(1)
    return name


PATTERN_ACTOR_VARIANT = re.compile(r"([\w-]+)_\d{2}")


def strip_actor_variant(name: str) -> str:
    """
    Returns the actor name without it actor variant id.

    Args:
        name: The actor name

    Returns:
        A string with the variant id removed
    """
    if match := PATTERN_ACTOR_VARIANT.match(name):
        return match.group(1)
    return name


class LocationType(IntEnum):
    UNKNOWN = 0
    LOCATION = 1
    SHIP = 2


class Location(NamedTuple):
    preposition: str
    name: str
    type_: LocationType = LocationType.LOCATION


LOCATIONS_STARTSWITH: dict[str, Location] = {
    "LocationHarvestableObjectContainer_ab_pyro_": Location(
        "at a", "Remote Asteroid Base, Pyro"
    ),
    "Hangar_": Location("in a", "Hangar"),
    "RastarInteriorGridHost_": Location("in an", "Unknown Surface Facility"),
    "SolarSystem_": Location("in", "Space"),
    "TransitCarriage_": Location("in an", "Elevator"),
}


def get_location(name: str) -> Location:
    """
    Retrieves a user-friendly representation of the location.
    `name` is not unique, as locations may be reused.
    Non-unique zones will return "a" or "an" as part of its preposition.

    Args:
        name: The name of the zone.

    Returns:
        A `Location` tuple (preposition, location, type)
    """
    try:
        location = LOCATIONS[name]
    except KeyError:
        pass
    else:
        if isinstance(location, str):
            return Location("at", location)
        return Location(location[0], location[1])

    # Location can also be a ship id
    vehicle_name, vehicle_type, found = get_vehicle(name)
    if found:
        return Location(
            "in a",
            (vehicle_type + " " if vehicle_type else "") + vehicle_name,
            LocationType.SHIP,
        )

    # UGF is CIG-ese for what most folks call "Bunkers"
    if "-ugf_" in name.lower():
        return Location("in a", ("Drug " if name.endswith("_drugs") else "") + "Bunker")

    # Handle some special cases
    for loc_name_sw, location_data in LOCATIONS_STARTSWITH.items():
        if name.startswith(loc_name_sw):
            return location_data

    return Location("at", name, LocationType.UNKNOWN)


def get_respawn_location(name: str) -> tuple[str, LocationType]:
    """
    Retrieves a user-friendly representation of the respawn location.

    Args:
        name: The id of the respawn destination.

    Returns:
        A string
    """
    try:
        return (LOCATIONS_RESPAWN[name.replace("@", "", 1)], LocationType.LOCATION)
    except KeyError:
        return (name, LocationType.UNKNOWN)


RE_DEBRIS = re.compile(r"SCItem_Debris_\d{12,}")
RE_HAZARD = re.compile(r"(Radiation|Water)_Hazard")
RE_HAZARD_NUM = re.compile(r"Hazard-\d{3}")
# Seen: 000, 002, 003, 004
# there's also a "Hazard_Area18" at Area 18


def get_entity(name: str) -> tuple[str, bool]:
    """
    Returns:
        A tuple (name, npc), where:
        - name: name of the entity
        - npc: whether the entity is an npc (if name matched a pattern below)
    """
    if name == "unknown":
        return (name, True)

    try:
        actor_name = strip_actor_variant(strip_id(name))
        return (ACTORS[actor_name], True)
    except KeyError:
        pass

    if hazard := RE_HAZARD.match(name):
        return (f"{hazard[1]} Hazard", True)
    if RE_HAZARD_NUM.match(name):
        return ("Environmental Hazard", True)

    if name == "Nova-01":
        return ("Nova", True)

    # fun fact, kill messages aren't logged for maroks. birds aren't real

    if RE_SIMPLE.match(name):
        return (name, True)

    # or vehicles
    vehicle_name, vehicle_type, vehicle_found = get_vehicle(name)
    if vehicle_found:
        return ((vehicle_type + " " if vehicle_type else "") + vehicle_name, True)

    # killer can be weapons
    # KILL: behr_gren_frag_01_123456789012 killed Contestedzones_sniper with a unknown at
    # KILL: behr_pistol_ballistic_01_123456789012 killed Headhunters_techie NPC with a unknown in an Unknown Surface Facility
    # and items too, usually by Collision
    # note: don't bother dumping the item list.
    # there are a lot of items, and this only happens rarely.
    try:
        if (fps_name := strip_id(name)) != name:
            return (WEAPONS_FPS[fps_name], True)
    except KeyError:
        pass

    if RE_DEBRIS.match(name):
        return ("Debris", True)

    if name == "Hazard_hangar_medfrnt_dungeon_exec_rund":
        return ("Executive Hangar Door Hazard", True)

    if name == "GameRules":
        return ("GameRules", True)

    # Player handles are max 20 characters
    if len(name) > 20:
        return (name, True)

    return (name, False)


def get_item(item_class: str, killer: str, killed: str, damage_type: str) -> str:
    if item_class == "Player":
        return "suicide"

    if item_class == "unknown":
        # Ship collision
        if killer == killed:
            return f"suicide by {damage_type}"

        if RE_SIMPLE.match(killer):
            return "skill check"

        return damage_type

    try:
        return WEAPONS_FPS[item_class]
    except KeyError:
        pass

    try:
        return WEAPONS_SHIP[item_class]
    except KeyError:
        pass

    return item_class


def get_vehicle_type(name: str) -> str:
    return VEHICLE_TYPES.get(name, name)


RE_VEHICLE_NAME = re.compile(r"_?(.*?)(?:_((?:PU|EA)_AI_.*))?_\d{12,}")


def get_vehicle(name: str) -> tuple[str, str | None, bool]:
    """
    Returns:
        A tuple (name, vtype, found) where:
        - name: the name of the ship if found
        - vtype: the type of ship if any if found
        - found: whether the vehicle was found
    """
    matches = RE_VEHICLE_NAME.findall(name)
    if not matches:
        if RE_SIMPLE.match(name):
            return (name, None, False)
        if name == "ORIG_300i-003":
            return ("Origin 300i", "Hijacked 890 Jump", True)
        return (name, None, False)

    if len(matches) == 2 and matches[0][0] == "SCItem_Debris":
        # Is it debris?
        vehicle_type = get_vehicle_type(matches[1][1]) if matches[1][1] else None
        try:
            return (SHIPS[matches[1][0]] + " (Debris)", vehicle_type, True)
        except KeyError:
            return (matches[1][0] + " (Debris)", vehicle_type, False)

    vehicle_name = matches[0][0]
    vehicle_type = get_vehicle_type(matches[0][1]) if matches[0][1] else None

    try:
        return (SHIPS[vehicle_name], vehicle_type, True)
    except KeyError:
        pass

    return (name, None, False)


def get_article(noun: str) -> str:
    if noun[0].lower() == "r":
        if len(noun) > 1 and noun[1].lower() in ["a", "e", "i", "o", "u", "y"]:
            # r is a consonant here, probably
            return "a"
        # eg "RSI"
        return "an"
    return (
        "an"
        if any(noun.lower().startswith(v) for v in ["a", "e", "i", "o", "u"])
        else "a"
    )
