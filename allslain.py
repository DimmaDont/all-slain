#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import timedelta
from io import TextIOWrapper
import os
import re
import time
from collections.abc import Generator
from typing import Any, NoReturn

from colorize import Color
from data import ACTORS, LOCATIONS, SHIPS, WEAPONS_FPS, WEAPONS_SHIP, VEHICLE_TYPES
from log_parser import SCLogParser


LOADED_ITEM = {
    "pu": "PU",
    "pyro": "Pyro",
    "Frontend_Main": "Main Menu",
}


LOG_INCAP_CAUSE = re.compile(r"([\w\d]+) \((\d.\d+) damage\)(?:, )?")

RE_VEHICLE_NAME = re.compile(r"(.*?)_?((?:PU|EA)_AI_.*)?_(\d{12,})")
RE_SHIP_DEBRIS = re.compile(r"SCItem_Debris_\d{12,}_(.*?)(?:_(?:PU|EA)_.*)?_\d{12,}")
RE_DEBRIS = re.compile(r"SCItem_Debris_\d{12,}")
RE_HAZARD = re.compile(r"(Radiation|Water)_Hazard")
RE_HAZARD_NUM = re.compile(r"Hazard-\d{3}")
# Seen: 000, 002, 003, 004
# there's also a "Hazard_Area18" at Area 18

RE_ASTEROID = re.compile(r"OscillationSimple-\d{3}")


INCAP = Color.YELLOW("INCAP".rjust(10))
JUMP = Color.GREEN("JUMP".rjust(10))
KILL = Color.RED("KILL".rjust(10))
QUIT = Color.CYAN("QUIT".rjust(10))
RESPAWN = Color.CYAN("RESPAWN".rjust(10))
SPAWNED = Color.WHITE("SPAWNED".rjust(10), bold=True)
VKILL = Color.RED("VKILL".rjust(10))
CONNECT = Color.WHITE("CONNECT".rjust(10), bold=True)
LOAD = Color.WHITE("LOAD".rjust(10), bold=True)
QUANTUM = Color.BLACK("QUANTUM".rjust(10), bold=True)


def follow(f: TextIOWrapper) -> Generator[str, Any, NoReturn]:
    while True:
        if line := f.readline():
            yield line
        else:
            time.sleep(1)
            continue


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


def clean_location(name: str) -> tuple[str, str, str]:
    try:
        # todo not all are "at"
        return ("at", LOCATIONS[name.replace("@", "")], "loc")
    except KeyError:
        pass

    # Handle some special cases
    if name.startswith("LocationHarvestableObjectContainer_ab_pyro_"):
        return ("at a", "Remote Asteroid Base, Pyro", "loc")

    # UGF is CIG-ese for what most folks call "Bunkers"
    if "-ugf_" in name.lower():
        return ("in a", ("Drug " if name.endswith("_drugs") else "") + "Bunker", "loc")

    if name.startswith("Hangar_"):
        return ("in a", "Hangar", "loc")

    if name.startswith("RastarInteriorGridHost_"):
        return ("in an", "Unknown Surface Facility", "loc")

    # Location can also be a ship id
    vehicle_name, found = get_vehicle(name)
    if found:
        return ("in a", vehicle_name, "ship")

    if name.startswith("SolarSystem_"):
        return ("in", "Space", "loc")
    if name.startswith("TransitCarriage_"):
        return ("in an", "Elevator", "loc")

    return ("at", name, "loc")


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

    # fun fact, kill messages aren't logged for maroks

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


LOG_ENCODING = "latin-1"
LOG_NEWLINE = "\r\n"


def main(filepath: str) -> None:
    is_prev_line_cet = False
    try:
        f = open(filepath, "r", encoding=LOG_ENCODING, newline=LOG_NEWLINE)
        for line in follow(f):
            if match := SCLogParser.find_match(line):
                log_type = match[0]
                log = match[1]
                when = log[1].replace("T", " ")
                if log_type == "CET":
                    step_num = log[5]
                    which = (
                        (
                            Color.GREEN("Complete") if step_num == "15" else "Complete",
                            "in",
                        )
                        if log[2] == "ContextEstablisherTaskFinished"
                        else (Color.YELLOW("Busy".rjust(8)), "for")
                    )
                    taskname = log[3]
                    step = log[4]
                    running_time = int(float(log[6]))
                    running_time_color = (
                        "RED"
                        if running_time > 300
                        else ("YELLOW" if running_time > 150 else "CYAN")
                    )
                    running_time_text = Color[running_time_color](
                        str(timedelta(seconds=running_time))
                    )
                    if is_prev_line_cet:
                        # Move cursor up one line and clear it
                        print("\x1b[1A\x1b[2K", end="")
                    print(
                        f"{when}{LOAD}: {which[0]}: {step_num.rjust(2)}/15 {Color.CYAN(step)}:{Color.CYAN(taskname)} {which[1]} {running_time_text}"
                    )
                    is_prev_line_cet = True
                    continue

                if log_type == "KILLP":
                    killed, is_killed_npc = clean_name(log[2])
                    lp, location, location_type = clean_location(log[3])
                    is_ship = "ship" == location_type
                    killer, is_killer_npc = clean_name(log[4])
                    cause = clean_tool(log[5], log[4], log[2], log[6])
                    if cause.startswith("suicide"):
                        print(
                            f"{when}{KILL}: {Color.GREEN(killer)} committed {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
                        )
                    elif is_killer_npc and is_killed_npc:
                        if is_ship:
                            print(
                                f"{when}{KILL}: {Color.BLACK(killer, bold = True)} killed {Color.BLACK(killed, bold = True)} {lp} {Color.YELLOW(location)} with a {Color.CYAN(cause)}"
                            )
                        else:
                            print(
                                f"{when}{KILL}: {Color.BLACK(killer, bold = True)} killed {Color.BLACK(killed, bold = True)} with a {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
                            )
                    else:
                        if is_ship:
                            print(
                                f"{when}{KILL}: {Color.GREEN(killer)} killed {Color.GREEN(killed)} {lp} {Color.YELLOW(location)} with a {Color.CYAN(cause)}"
                            )
                        else:
                            print(
                                f"{when}{KILL}: {Color.GREEN(killer)} killed {Color.GREEN(killed)} with a {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
                            )
                elif log_type == "KILLV":
                    # log[2] and log[6] are vehicles, or if the event is a collision, npc/player entities
                    vehicle_name, found = get_vehicle(log[2])
                    vehicle = Color.GREEN(
                        vehicle_name if found else clean_name(log[2])[0]
                    )
                    lp, location, _ = clean_location(log[3])
                    driver, _ = clean_name(log[4])
                    if driver == "unknown":
                        driver = ""
                    else:
                        driver = Color.GREEN(driver) + " in a "
                    kill_type = (
                        Color.YELLOW("disabled")
                        if log[5] == "1"
                        else Color.RED("destroyed")
                    )

                    vehicle_name2, found2 = get_vehicle(log[6])
                    killer = Color.GREEN(
                        vehicle_name2 if found2 else clean_name(log[6])[0]
                    )
                    dmgtype = Color.CYAN(log[7])
                    print(
                        f"{when}{VKILL}: {killer} {kill_type} a {driver}{vehicle} with {dmgtype} {lp} {Color.YELLOW(location)}"
                    )
                elif log_type == "RESPAWN":
                    # datetime, player, location
                    whom = Color.GREEN(log[2])
                    _, where, _ = clean_location(log[3])
                    print(f"{when}{RESPAWN}: {whom} from {Color.YELLOW(where)}")
                elif log_type == "INCAP":
                    # datetime, player, causes
                    whom = Color.GREEN(log[2])
                    causes = LOG_INCAP_CAUSE.findall(log[3])
                    print(
                        f"{when}{INCAP}: {whom} from {', '.join([Color.YELLOW(cause[0].replace('Damage', '')) for cause in causes])}"
                    )
                elif log_type == "QUITLOBBY":
                    whom = Color.GREEN(log[2])
                    print(f"{when}{QUIT}: {whom} has quit the game session.")
                elif log_type == "SPAWN":
                    print(f"{when}{SPAWNED}: Character spawned!")
                elif log_type == "JUMP":
                    whom = Color.GREEN(log[2])
                    origin = Color.BLUE(log[3], bold=True)
                    dest = Color.BLUE(log[4], bold=True)
                    print(
                        f"{when}{JUMP}: {whom} has departed {origin} for the {dest} system."
                    )
                elif log_type == "CONNECTING":
                    print(f"{when}{CONNECT}: Connecting...")
                elif log_type == "CONNECTED":
                    print(f"{when}{CONNECT}: Connected!")
                elif log_type == "LOADING":
                    print(f"{when}{LOAD}: Loading...")
                elif log_type == "LOADED":
                    what = Color.GREEN(LOADED_ITEM.get(log[2], log[2]))
                    running_time_text = Color.GREEN(
                        str(timedelta(seconds=float(log[3]))).rstrip("0")
                    )
                    print(
                        f"{when}{LOAD}: Loaded! {what} took {running_time_text} to load."
                    )
                elif log_type == "QUIT":
                    print(f"{when}{QUIT}: Game quit.")
                elif log_type == "QUANTUM":
                    name = Color.GREEN(log[2])
                    dest = Color.YELLOW(clean_location(log[3])[1])
                    print(f"{when}{QUANTUM}: {name} started quantum travel to {dest}")
                else:
                    continue
                is_prev_line_cet = False
    except KeyboardInterrupt:
        pass
    except FileNotFoundError:
        print(Color.RED(f'Log file "{filepath}" not found.'))
    finally:
        try:
            f.close()
        except UnboundLocalError:
            pass


TRY_FILES = [
    "Game.log",
    R"C:\Program Files\Roberts Space Industries\StarCitizen\HOTFIX\Game.log",
    R"C:\Program Files\Roberts Space Industries\StarCitizen\LIVE\Game.log",
]


def find_game_log() -> str | None:
    for file in TRY_FILES:
        if os.path.isfile(file):
            return file
    return None


if __name__ == "__main__":
    # Set window title and cursor shape
    print("\x1b]0;all-slain\x07\x1b[2\x20q", end="")

    print(f"{Color.WHITE('all-slain', bold = True)}: Star Citizen Game Log Reader")
    print(f"{Color.BLUE('https://github.com/DimmaDont/all-slain', bold = True)}\n")

    parser = ArgumentParser()
    parser.add_argument("file", nargs="?")
    args = parser.parse_args()

    if filename := args.file if args.file else find_game_log():
        print(f'Reading "{Color.CYAN(filename)}"\n')
        main(filename)
    else:
        print(Color.RED("No log files found in the default locations."))
        print(
            "Run this again from within the game folder after starting the game, or specify a game log to read."
        )

# vim: set expandtab ts=4 sw=4
