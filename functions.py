import re

from data import ACTORS, LOCATIONS, SHIPS, VEHICLE_TYPES, WEAPONS_FPS, WEAPONS_SHIP


# TODO confirm
RE_ASTEROID = re.compile(r"(?:Rotation|Oscillation)Simple-\d{3}")


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
    """
    Returns: A tuple (preposition, location, type)
    """
    try:
        # todo not all are "at"
        location = LOCATIONS[name.replace("@", "", 1)]
    except KeyError:
        pass
    else:
        if isinstance(location, str):
            return ("at", location, "loc")
        return (location[0], location[1], "loc")

    # Location can also be a ship id
    vehicle_name, vehicle_type, found = get_vehicle(name)
    if found:
        return (
            "in a",
            (vehicle_type + " " if vehicle_type else "") + vehicle_name,
            "ship",
        )

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


def clean_name(name: str) -> tuple[str, bool]:
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

    if RE_ASTEROID.match(name):
        return ("Asteroid", True)

    # or vehicles
    vehicle_name, vehicle_type, found = get_vehicle(name)
    if found:
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

    return (name, False)


def clean_tool(item_class: str, killer: str, killed: str, damage_type: str) -> str:
    if item_class == "Player":
        return "suicide"

    if item_class == "unknown":
        # Ship collision
        if killer == killed:
            return f"suicide by {damage_type}"

        if RE_ASTEROID.match(killer):
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
        # Is it a moving asteroid?...
        asteroid = RE_ASTEROID.match(name)
        if asteroid:
            return ("Asteroid", None, True)
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
