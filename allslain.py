#!/usr/bin/env python3
from argparse import ArgumentParser
from io import TextIOWrapper
import os
import re
import time

from colorize import Color
from data import LOCATIONS, SHIPS, WEAPONS_FPS, WEAPONS_SHIP
from log_parser import SCLogParser

LOG_INCAP_CAUSE = re.compile(r"([\w\d]+) \((\d.\d+) damage\)(?:, )?")

RE_VEHICLE_NAME = re.compile(
    r"(.*?)_?(PU_AI_NineTails|PU_AI_CRIM(?:_QIG|_ScatterGun)?|PU_AI_NT)?_(\d{12})"
)
RE_SHIP_DEBRIS = re.compile(r"SCItem_Debris_\d{12}_(.+)_\d{12}")
RE_HAZARD = re.compile(r"Hazard-\d{3}")


INCAP = Color.YELLOW("INCAP".rjust(10))
JUMP = Color.GREEN("JUMP".rjust(10))
KILL = Color.RED("KILL".rjust(10))
QUIT = Color.CYAN("QUIT".rjust(10))
RESPAWN = Color.CYAN("RESPAWN".rjust(10))
SPAWNED = Color.CYAN("SPAWNED".rjust(10))
VKILL = Color.RED("VKILL".rjust(10))


def follow(f: TextIOWrapper):
    while True:
        if line := f.readline():
            yield line
        else:
            time.sleep(1)
            continue


def remove_id(name: str) -> str:
    try:
        i = name.rindex("_")
        entity_id = name[i + 1 :]

        # ids are 12 digits
        if len(entity_id) != 12:
            raise ValueError("invalid entity id length")
        int(entity_id)
        # Has id
        return name[:i]
    except ValueError:
        # No id or invalid id
        pass
    return name


def clean_location(name: str) -> tuple[str, str]:
    try:
        # todo not all are "at"
        return ("at", LOCATIONS[name.replace("@", "")])
    except KeyError:
        pass

    # Handle some special cases
    if name.startswith("LocationHarvestableObjectContainer_ab_pyro_"):
        return ("at a", "Remote Asteroid Base (Pyro)")

    # UGF is CIG-ese for what most folks call "Bunkers"
    if "-ugf_" in name.lower():
        return ("in a", ("Drug " if name.endswith("_drugs") else "") + "Bunker")

    if name.startswith("Hangar_"):
        return ("in a", "Hangar")

    if name.startswith("RastarInteriorGridHost_"):
        return ("in an", "Unknown Surface Facility")

    # Location can also be a ship id
    vehicle = get_vehicle(name)
    if vehicle != name:
        return ("in a", vehicle)

    if name.startswith("SolarSystem_"):
        return ("in", "Space")
    if name.startswith("TransitCarriage_"):
        return ("in an", "Elevator")

    return ("at", name)


def clean_name(name: str) -> tuple[str, int]:
    if name == "unknown":
        return (name, 1)
    if name.startswith("PU_Human_Enemy_"):
        name_split = name.split("_")
        return ("_".join(name_split[5:7]), 1)
    if name.startswith("PU_Human-"):
        name_split = re.split(r"[_-]+", name)
        return ("_".join(name_split[2:6]), 1)
    if name.startswith("NPC_Archetypes-Human-"):
        name_split = re.split(r"[_-]+", name)
        return ("_".join(name_split[3:7]), 1)
    if name.startswith("NPC_Archetypes-"):
        return (name[: name.rindex("_")].split("-")[-1].replace("-", "_"), 1)
    if name.startswith("Kopion_"):
        return ("Kopion", 1)
    if name.startswith("PU_Pilots-"):
        name_split = re.split(r"[_-]+", name)
        return ("_".join(["Pilot", *name_split[3:6]]), 1)
    if name.startswith("AIModule_Unmanned_PU_SecurityNetwork_"):
        return ("NPC Security", 1)
    if name.startswith("AIModule_Unmanned_PU_Advocacy_"):
        return ("NPC UEE Security", 1)
    # Some cases from Pyro observed:
    if "Pilot_Criminal_Pilot" in name:
        return ("NPC Pilot", 1)
    if "Pilot_Criminal_Gunner" in name:
        return ("NPC Gunner", 1)
    if "pyro_outlaw" in name:
        return ("NPC Criminal", 1)

    if RE_HAZARD.match(name):
        return ("Environmental Hazard", 1)
    if name == "Nova-01":
        return ("Nova", 1)
    if name.startswith("Quasigrazer_"):
        return ("Quasigrazer", 1)
    # fun fact, kill messages aren't logged for maroks

    # killer can be weapons too
    # KILL: behr_gren_frag_01_123456789012 killed Contestedzones_sniper with a unknown at
    # KILL: behr_pistol_ballistic_01_123456789012 killed Headhunters_techie NPC with a unknown in an Unknown Surface Facility

    return (name, 0)


def clean_tool(name: str, killer: str, killed: str) -> str:
    if name == "Player":
        return "suicide"

    if name == "unknown":
        # Ship collision
        if killer == killed:
            return "suicide"
        return name

    try:
        return WEAPONS_FPS[name]
    except KeyError:
        pass

    try:
        return WEAPONS_SHIP[name]
    except KeyError:
        pass

    return name


def get_vehicle(name: str) -> str:
    match = RE_VEHICLE_NAME.match(name)
    if not match:
        return name
    vehicle_name = match[1]

    try:
        return SHIPS[vehicle_name]
    except KeyError:
        pass

    # Is it debris?
    debris = RE_SHIP_DEBRIS.match(name)
    if debris:
        try:
            return SHIPS[debris[1]] + " (Debris)"
        except KeyError:
            pass

    return name


def main(filepath: str) -> None:
    try:
        f = open(filepath, "r", encoding="utf-8")
        for line in follow(f):
            if match := SCLogParser.find_match(line):
                if log := match.get("KILLP"):
                    when = log[1].replace("T", " ")
                    killed, is_killed_npc = clean_name(log[2])
                    lp, location = clean_location(log[3])
                    killer, is_killer_npc = clean_name(log[4])
                    cause = clean_tool(log[5], killer, killed)
                    if cause == "suicide":
                        print(
                            f"{when}{KILL}: {Color.GREEN(killer)} committed {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
                        )
                    elif is_killer_npc and is_killed_npc:
                        print(
                            f"{when}{KILL}: {Color.BLACK(killer, True)} killed {Color.BLACK(killed, True)} with a {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
                        )
                    else:
                        print(
                            f"{when}{KILL}: {Color.GREEN(killer)} killed {Color.GREEN(killed)} with a {Color.CYAN(cause)} {lp} {Color.YELLOW(location)}"
                        )
                elif log := match.get("KILLV"):
                    when = log[1].replace("T", " ")
                    # note: vehicle can also be an npc/player entity if it's a collision
                    vehicle = Color.GREEN(get_vehicle(log[2]))
                    lp, location = clean_location(log[3])
                    driver, _ = clean_name(log[4])
                    if driver == "unknown":
                        driver = ""
                    else:
                        driver = Color.GREEN(driver) + " in a "
                    kill_type = log[5]

                    # note: killer can also be an npc entity
                    killer = Color.GREEN(get_vehicle(log[6]))
                    dmgtype = Color.CYAN(log[7])
                    print(
                        f'{when}{VKILL}: {killer} {Color.YELLOW("disabled") if kill_type == "1" else Color.RED("destroyed")} a {driver}{vehicle} with {dmgtype} {lp} {Color.YELLOW(location)}'
                    )
                elif log := match.get("RESPAWN"):
                    # datetime, player, location
                    when = log[1].replace("T", " ")
                    whom = Color.GREEN(log[2])
                    _, where = clean_location(log[3])
                    print(f"{when}{RESPAWN}: {whom} from {Color.YELLOW(where)}")
                elif log := match.get("INCAP"):
                    # datetime, player, causes
                    when = log[1].replace("T", " ")
                    whom = Color.GREEN(log[2])
                    causes = LOG_INCAP_CAUSE.findall(log[3])
                    print(
                        f"{when}{INCAP}: {whom} from {', '.join([Color.YELLOW(cause[0].replace('Damage', '')) for cause in causes])}"
                    )
                elif log := match.get("QUIT"):
                    when = log[1].replace("T", " ")
                    whom = Color.GREEN(log[2])
                    print(f"{when}{QUIT}: {whom} has quit the game session.")
                elif log := match.get("SPAWN"):
                    when = log[1].replace("T", " ")
                    print(f"{when}{SPAWNED}: Character spawned!")
                elif log := match.get("JUMP"):
                    when = log[1].replace("T", " ")
                    whom = Color.GREEN(log[2])
                    origin = Color.BLUE(log[3])
                    dest = Color.BLUE(log[4])
                    print(
                        f"{when}{JUMP}: {whom} haѕ departed {origin} for the {dest} system."
                    )
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
    R"C:\Program Files\Roberts Space Industries\StarCitizen\4.0_PREVIEW\Game.log",
    R"C:\Program Files\Roberts Space Industries\StarCitizen\LIVE\Game.log",
]


def find_game_log() -> str | None:
    for file in TRY_FILES:
        if os.path.isfile(file):
            return file
    return None


if __name__ == "__main__":
    print(f"{Color.WHITE('all-slain', True)}: Star Citizen Game Log Reader")
    print(f"{Color.BLUE('https://github.com/DimmaDont/all-slain', True)}\n")

    parser = ArgumentParser()
    parser.add_argument('file', nargs='?')
    args = parser.parse_args()

    if filename := args.file if args.file else find_game_log():
        print(f"Reading \"{Color.CYAN(filename)}\"\n")
        main(filename)
    else:
        print(Color.RED("No log files found in the default locations."))
        print(
            "Run this again from within the game folder after starting the game, or specify a game log to read."
        )

# vim: set expandtab ts=4 sw=4
