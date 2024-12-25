#!/usr/bin/env python3
from io import TextIOWrapper
import os
import re
import sys
import time

from colorize import Color
from data import LOCATIONS, SHIPS, WEAPONS_FPS, WEAPONS_SHIP


LOG_JUMP = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Changing Solar System>.* Client entity ([\w-]*) .* changing system from (\w+) to (\w+) .*"
)
LOG_KILL = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Actor Death> CActor::Kill: '([\w-]+)' \[\d+\] in zone '([\w-]+)' killed by '([\w-]+)' \[\d+\] using '[\w-]+' \[Class ([\w-]+)\] with damage type '([A-Za-z]+)' from direction (.*) \[Team_ActorTech\]\[Actor\]"
)
LOG_VEHICLE_KILL = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([\w-]+)' \[\d+\] in zone '([\w-]+)' \[pos.*\] driven by '([\w-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([\w-]+)' \[[0-9_]+\] with '([A-Za-z]+)' \[Team_VehicleFeatures\]\[Vehicle\]"
)
LOG_RESPAWN = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Corpse> Player '([\w-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital. \[Team_ActorTech\]\[Actor\]"
)
LOG_QUIT = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <\[EALobby\] EALobbyQuit> \[EALobby\]\[CEALobby::RequestQuitLobby\] ([\w-]+) Requesting QuitLobby.*"
)
LOG_INCAP = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> Logged an incap\.! nickname: ([\w-]+), causes: \[(.+)\]"
)
LOG_INCAP_CAUSE = re.compile(r"([\w\d]+) \((\d.\d+) damage\)(?:, )?")

LOG_SPAWNED = re.compile(
    r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[CSessionManager::OnClientSpawned\] Spawned!"
)

RE_VEHICLE_NAME = re.compile(
    r"(.*?)_?(PU_AI_NineTails|PU_AI_CRIM|PU_AI_NT|Unmanned_Salvage)?_(\d{12})"
)


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
        return ("at", LOCATIONS[name])
    except KeyError:
        pass

    # Handle some special cases
    if name.startswith("LocationHarvestableObjectContainer_ab_pyro_"):
        return ("at a", "Remote Asteroid Base (Pyro)")

    # UGF is CIG-ese for what most folks call "Bunkers"
    if "-ugf_" in name.lower():
        return ("in a", "Bunker")

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
    # Some cases from Pyro observed:
    if "Pilot_Criminal_Pilot" in name:
        return ("NPC Pilot", 1)
    if "Pilot_Criminal_Gunner" in name:
        return ("NPC Gunner", 1)
    if "pyro_outlaw" in name:
        return ("NPC Criminal", 1)

    if name == "Hazard-000":
        return ("Environmental Hazard", 1)
    if name.startswith("Quasigrazer_"):
        return ("Quasigrazer", 1)

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
    salvage = vehicle[2] == "Unmanned_Salvage"

    try:
        return SHIPS[vehicle_name] + (" (Salvage)" if salvage else "")
    except KeyError:
        pass

    return name


def main(filepath: str) -> None:
    try:
        f = open(filepath, "r", encoding="utf-8")
        for line in follow(f):
            matches = {
                "pkill": LOG_KILL.match(line),
                "vkill": LOG_VEHICLE_KILL.match(line),
                "respawn": LOG_RESPAWN.match(line),
                "incap": LOG_INCAP.match(line),
                "quits": LOG_QUIT.match(line),
                "spawned": LOG_SPAWNED.match(line),
                "jumps": LOG_JUMP.match(line),
            }
            if any(matches):
                if log := matches["pkill"]:
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
                elif log := matches["vkill"]:
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
                elif log := matches["respawn"]:
                    # datetime, player, location
                    when = log[1].replace("T", " ")
                    whom = Color.GREEN(log[2])
                    lp, where = clean_location(log[3])
                    print(f"{when}{RESPAWN}: {whom} {lp} {Color.YELLOW(where)}")
                elif log := matches["incap"]:
                    # datetime, player, causes
                    when = log[1].replace("T", " ")
                    whom = Color.GREEN(log[2])
                    causes = LOG_INCAP_CAUSE.findall(log[3])
                    print(
                        f"{when}{INCAP}: {whom} from {', '.join([Color.YELLOW(cause[0].replace('Damage', '')) for cause in causes])}"
                    )
                elif log := matches["quits"]:
                    when = log[1].replace("T", " ")
                    whom = Color.GREEN(log[2])
                    print(f"{when}{QUIT}: {whom} has quit the game session.")
                elif log := matches["spawned"]:
                    when = log[1].replace("T", " ")
                    print(f"{when}{SPAWNED}: Spawned!")
                elif log := matches["jumps"]:
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
        print(
            "Run this again from within the game folder after starting the game, or specify a game log to read."
        )
    finally:
        try:
            f.close()
        except UnboundLocalError:
            pass


if __name__ == "__main__":
    print(f"{Color.WHITE('all-slain', True)}: Star Citizen Game Log Reader")
    print(f"{Color.BLUE('https://github.com/DimmaDont/all-slain', True)}\n")

    filename: str = "Game.log"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    if not os.path.isfile(filename):
        filename = r"C:\Program Files\Roberts Space Industries\StarCitizen\4.0_PREVIEW\Game.log"
    main(filename)

# vim: set expandtab ts=4 sw=4
