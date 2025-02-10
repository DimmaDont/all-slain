import re

from data import ACTORS, LOCATIONS, SHIPS, VEHICLE_TYPES, WEAPONS_FPS, WEAPONS_SHIP


RE_ASTEROID = re.compile(r"OscillationSimple-\d{3}")


PATTERN_ID = re.compile(r"([\w-]+)_\d{12,}")


def strip_id(name: str) -> str:
    if match := PATTERN_ID.match(name):
        return match.group(1)
    return name


PATTERN_ACTOR_VARIANT = re.compile(r"([\w-]+)_\d{2}")


def strip_actor_variant(name: str) -> str:
    if match := PATTERN_ACTOR_VARIANT.match(name):
        return match.group(1)
    return name


LOCATIONS_STARTSWITH = {
    "LocationHarvestableObjectContainer_ab_pyro_": (
        "at a",
        "Remote Asteroid Base, Pyro",
        "loc",
    ),
    "Hangar_": ("in a", "Hangar", "loc"),
    "RastarInteriorGridHost_": ("in an", "Unknown Surface Facility", "loc"),
    "SolarSystem_": ("in", "Space", "loc"),
    "TransitCarriage_": ("in an", "Elevator", "loc"),
}


def clean_location(name: str) -> tuple[str, str, str]:
    try:
        # todo not all are "at"
        return ("at", LOCATIONS[name.replace("@", "")], "loc")
    except KeyError:
        pass

    # Location can also be a ship id
    vehicle_name, found = get_vehicle(name)
    if found:
        return ("in a", vehicle_name, "ship")

    # UGF is CIG-ese for what most folks call "Bunkers"
    if "-ugf_" in name.lower():
        return ("in a", ("Drug " if name.endswith("_drugs") else "") + "Bunker", "loc")

    # Handle some special cases
    for location, data in LOCATIONS_STARTSWITH.items():
        if name.startswith(location):
            return data

    return ("at", name, "loc")


RE_DEBRIS = re.compile(r"SCItem_Debris_\d{12,}")
RE_HAZARD = re.compile(r"(Radiation|Water)_Hazard")
RE_HAZARD_NUM = re.compile(r"Hazard-\d{3}")
# Seen: 000, 002, 003, 004
# there's also a "Hazard_Area18" at Area 18


def clean_name(name: str) -> tuple[str, int]:
    """
    Returns:
        A tuple (name, npc), where:
        - name: name of the entity
        - npc: whether the entity is an npc (if name matched a pattern below)
    """
    if name == "unknown":
        return (name, 1)

    try:
        actor_name = strip_actor_variant(strip_id(name))
        return (ACTORS[actor_name], 1)
    except KeyError:
        pass

    if hazard := RE_HAZARD.match(name):
        return (f"{hazard[1]} Hazard", 1)
    if RE_HAZARD_NUM.match(name):
        return ("Environmental Hazard", 1)

    if name == "Nova-01":
        return ("Nova", 1)

    # fun fact, kill messages aren't logged for maroks. birds aren't real

    if RE_ASTEROID.match(name):
        return ("Asteroid", 1)

    # or vehicles
    vehicle_name, found = get_vehicle(name)
    if found:
        return (vehicle_name, 1)

    # killer can be weapons too
    # KILL: behr_gren_frag_01_123456789012 killed Contestedzones_sniper with a unknown at
    # KILL: behr_pistol_ballistic_01_123456789012 killed Headhunters_techie NPC with a unknown in an Unknown Surface Facility
    try:
        if (fps_name := strip_id(name)) != name:
            return (WEAPONS_FPS[fps_name], 1)
    except KeyError:
        pass

    if RE_DEBRIS.match(name):
        return ("Debris", 1)

    return (name, 0)


def clean_tool(name: str, killer: str, killed: str, damage_type: str) -> str:
    if name == "Player":
        return "suicide"

    if name == "unknown":
        # Ship collision
        if killer == killed:
            return f"suicide by {damage_type}"

        if RE_ASTEROID.match(killer):
            return "skill check"

        return damage_type

    try:
        return WEAPONS_FPS[name]
    except KeyError:
        pass

    try:
        return WEAPONS_SHIP[name]
    except KeyError:
        pass

    return name


def get_vehicle_type(name: str) -> str:
    return VEHICLE_TYPES.get(name, name)


RE_VEHICLE_NAME = re.compile(r"(.*?)_?((?:PU|EA)_AI_.*)?_(\d{12,})")
RE_SHIP_DEBRIS = re.compile(r"SCItem_Debris_\d{12,}_(.*?)(?:_(?:PU|EA)_.*)?_\d{12,}")


def get_vehicle(name: str) -> tuple[str, bool]:
    """
    Returns:
        A tuple (name, found) where:
        - name: the name of the ship if found
        - found: whether the vehicle was found
    """
    match = RE_VEHICLE_NAME.match(name)
    if not match:
        # Is it a moving asteroid?...
        asteroid = RE_ASTEROID.match(name)
        if asteroid:
            return ("Asteroid", True)
        return (name, False)
    vehicle_name = match[1]
    vehicle_type = get_vehicle_type(match[2]) + " " if match[2] else ""

    try:
        return (vehicle_type + SHIPS[vehicle_name], True)
    except KeyError:
        pass

    # Is it debris?
    debris = RE_SHIP_DEBRIS.match(name)
    if debris:
        try:
            return (SHIPS[debris[1]] + " (Debris)", True)
        except KeyError:
            pass

    return (name, False)
