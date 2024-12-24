#!/usr/bin/env python3
from io import TextIOWrapper
import os
import re
import sys
import time

from colorize import Color
from data import LOCATIONS, SHIPS, WEAPONS_FPS, WEAPONS_SHIP


LOG_KILL = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Actor Death> CActor::Kill: '([A-Za-z0-9_-]+)' \[\d+\] in zone '([A-Za-z0-9_-]+)' killed by '([A-Za-z0-9_-]+)' \[\d+\] using '[A-Za-z0-9_-]+' \[Class ([A-Za-z0-9_-]+)\] with damage type '([A-Za-z]+)' from direction (.*) \[Team_ActorTech\]\[Actor\]"
)
LOG_VEHICLE_KILL = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([A-Za-z0-9_-]+)' \[\d+\] in zone '([A-Za-z0-9_-]+)' \[pos.*\] driven by '([A-Za-z0-9_-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([A-Za-z0-9_-]+)' \[[0-9_]+\] with '([A-Za-z]+)' \[Team_VehicleFeatures\]\[Vehicle\]"
)
LOG_RESPAWN = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Corpse> Player '([A-Za-z0-9_-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital. \[Team_ActorTech\]\[Actor\]"
)

RE_VEHICLE_NAME = re.compile(
    r"(.*?)_?(PU_AI_NineTails|PU_AI_CRIM|Unmanned_Salvage)?_(\d{12})")

KILL = Color.RED("KILL".rjust(10))
VKILL = Color.RED("VKILL".rjust(10))
RESPAWN = Color.CYAN("RESPAWN".rjust(10))


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


def clean_location(name: str) -> str:
    try:
        return LOCATIONS[name]
    except KeyError:
        pass
    finally:
        # Handle some special cases
        if name.startswith( "LocationHarvestableObjectContainer_ab_pyro_" ):
            return "Remote Asteroid Base (Pyro)"

    # UGF is CIG-ese for what most folks call "Bunkers"
    if "-ugf_" in name.lower():
        return "Bunker"

    if name.startswith("Hangar_"):
        return "Hangar"

    if name.startswith("RastarInteriorGridHost_"):
        return "Unknown Surface Facility"

    # Location can also be a ship id
    vehicle = get_vehicle(name)
    if vehicle != name:
        return vehicle

    if name.startswith("SolarSystem_"):
        return "Space"
    if name.startswith("TransitCarriage_"):
        return "Elevator"

    return name


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
    # Some cases from Pyro observed:
    if 'Pilot_Criminal_Pilot' in name:
        return ("NPC Pilot", 1)
    if 'Pilot_Criminal_Gunner' in name:
        return ("NPC Gunner", 1)
    if 'pyro_outlaw' in name:
        return ("NPC Criminal", 1)

    if name == "Hazard-000":
        return ("Environmental Hazard", 1)

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
    vehicle = RE_VEHICLE_NAME.match(name)
    if not vehicle:
        return name
    vehicle_name = vehicle[1]
    salvage = vehicle[2] == 'Unmanned_Salvage'

    try:
        return SHIPS[vehicle_name] + (" (Salvage)" if salvage else "")
    except KeyError:
        pass

    return name


def main(filepath: str) -> None:
    try:
        f = open(filepath, "r", encoding="utf-8")
        print(Color.RESET, end="")
        for line in follow(f):
            if m := LOG_KILL.match(line):
                when = m[1]

                killed, is_killed_npc = clean_name(m[2])
                location = clean_location(m[3])
                killer, is_killer_npc = clean_name(m[4])
                cause = clean_tool(m[5], killer, killed)
                if 'Space' in location:
                    at='in'
                elif 'Elevator' in location:
                    at='in an'
                else:
                    at='at'
                if is_killer_npc and is_killed_npc:
                    print(
                        f"{when}{KILL}: {Color.BRIGHT_BLACK(killer)} killed {Color.BRIGHT_BLACK(killed)} with a {Color.CYAN(cause)} {at} {Color.YELLOW(location)}"
                    )
                elif cause == "suicide":
                    print(
                        f"{when}{KILL}: {Color.GREEN(killer)} committed {Color.CYAN(cause)} {at} {Color.YELLOW(location)}"
                    )
                else:
                    print(
                        f"{when}{KILL}: {Color.GREEN(killer)} killed {Color.GREEN(killed)} with a {Color.CYAN(cause)} {at} {Color.YELLOW(location)}"
                    )
                continue
            if n := LOG_VEHICLE_KILL.match(line):
                when = n[1]
                # note: vehicle can also be an npc/player entity if it's a collision
                vehicle = Color.GREEN(get_vehicle(n[2]))
                location = Color.YELLOW(clean_location(n[3]))
                driver, _ = clean_name(n[4])
                if driver == "unknown":
                    driver = ""
                else:
                    driver = Color.GREEN(driver) + " in a "
                kill_type = n[5]
                killer = Color.GREEN(get_vehicle(n[6]))
                dmgtype = Color.CYAN(n[7])
                if 'Space' in location:
                    at='in'
                elif 'Elevator' in location:
                    at='in an'
                else:
                    at='at'
                print(
                    f'{when}{VKILL}: {killer} {"disabled" if kill_type == "1" else "destroyed"} a {driver}{vehicle} with {dmgtype} {at} {location}'
                )
                continue
            o = LOG_RESPAWN.match(line)
            if o:
                # datetime, player, location
                when = o[1]
                whom = Color.GREEN(o[2])
                where = Color.YELLOW(clean_location(o[3]))
                print(f"{o[1]}{RESPAWN}: {whom} at? {where}")
                continue
    except KeyboardInterrupt:
        pass
    except FileNotFoundError:
        print(Color.RED(f"Log file {filepath} not found."))
        print(
            "Run this again from within the game folder after starting the game, or specify a game log to read."
        )
    finally:
        f.close()


if __name__ == "__main__":
    filename: str = "Game.log"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    if not os.path.isfile(filename):
        filename = r"C:\Program Files\Roberts Space Industries\StarCitizen\4.0_PREVIEW\Game.log"
    main(filename)

# vim: set expandtab ts=4 sw=4
