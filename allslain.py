import os
import re
import sys
import time

from colorize import Color
from data import SHIPS, WEAPONS_FPS, WEAPONS_SHIP


LOG_KILL = re.compile(r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Actor Death> CActor::Kill: '([A-Za-z0-9_-]+)' \[\d+\] in zone '([A-Za-z0-9_-]+)' killed by '([A-Za-z0-9_-]+)' \[\d+\] using '[A-Za-z0-9_-]+' \[Class ([A-Za-z0-9_-]+)\] with damage type '([A-Za-z]+)' from direction (.*) \[Team_ActorTech\]\[Actor\]")
LOG_VEHICLE_KILL = re.compile(r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([A-Za-z0-9_-]+)' \[\d+\] in zone '([A-Za-z0-9_-]+)' \[pos.*\] driven by '([A-Za-z0-9_-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([A-Za-z0-9_-]+)' \[[0-9_]+\] with '([A-Za-z]+)' \[Team_VehicleFeatures\]\[Vehicle\]")
LOG_RESPAWN = re.compile(r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Corpse> Player '([A-Za-z0-9_-]+)' <remote client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital. \[Team_ActorTech\]\[Actor\]")


def follow(f):
    while True:
        if line := f.readline():
            yield line
        else:
            time.sleep(1)
            continue


def clean_location(name):
    name_split = name.split("_")
    if name[0] == "RastarInteriorGridHost":
        return name[0]
    short_name = []
    if 'ugf' in name.lower():
        return "Bunker" # UGF is CIG-ese for what most folks call "Bunkers"
    for i in name_split:
        try:
            int(i)
        except:
            short_name.append(i)
    return "_".join(short_name)


def clean_name(name):
    if name.startswith("PU_Human_Enemy"):
        name_split = name.split("_")
        return "_".join(["NPC", *name_split[5:6]])
    if name.startswith("PU_Human-"):
        name_split = name.split("-")
        return "_".join(["NPC", *name_split[1:3]])
    if name.startswith("NPC_Archetypes-"):
        name_split = name.split("-")
        return "_".join(["NPC", *name_split[3].split("_")[0:1], name_split[1]])
    if name.startswith("Kopion_"):
        return "_".join(["NPC", "Kopion"])
    return name


def clean_tool(name):
    if name == 'Player':
        return 'suicide'
    if name == "unknown":
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


def get_vehicle(name) -> str:
    # Remove vehicle id
    try:
        i = name.rindex("_")
        vehicle_id = name[i + 1:]
        int(vehicle_id)
        # has vehicle id
        name = name[:i]
        name = name.replace("_PU_AI_CRIM", "")
    except ValueError:
        # No vehicle ID
        pass

    try:
        return SHIPS[name]
    except KeyError:
        return name


KILL = Color.RED("KILL".rjust(10))
VKILL = Color.RED("VKILL".rjust(10))
RESPAWN = Color.CYAN("RESPAWN".rjust(10))


def main(filepath, show_npc_victims):
    try:
        f = open(filepath, "r")
        print(Color.RESET, end='')
        for line in follow(f):
            if m := LOG_KILL.match(line):
                # datetime, killed, location, killer, killed_using
                when = m[1]
                killed = clean_name(m[2])
                location = clean_location(m[3])
                killer = clean_name(m[4])
                cause = clean_tool(m[5])
                if "NPC" in killed and not show_npc_victims:
                    continue
                elif 'suicide' in cause:
                    print( f'{when}{KILL}: {Color.GREEN(killer)} committed {Color.CYAN(cause)} at {Color.YELLOW(location)}' )
                else:
                    print( f'{when}{KILL}: {Color.GREEN(killer)} killed {Color.GREEN(killed)} with a {Color.CYAN(cause)} at {Color.YELLOW(location)}' )
                continue
            if n := LOG_VEHICLE_KILL.match(line):
                # datetime, vehicle, location, driver, caused_by, damage_type
                when = n[1]
                vehicle = Color.GREEN(get_vehicle(n[2]))
                location = Color.YELLOW(clean_location(n[3]))
                driver = clean_name(n[4])
                if driver == 'unknown':
                    driver = ''
                else:
                    driver = Color.GREEN(driver) + " in a "
                kill_type = n[5]
                cause = Color.GREEN(get_vehicle(n[6]))
                dmgtype = Color.CYAN(n[7])
                print( f'{when}{VKILL}: {cause} {"soft" if kill_type == '1' else "hard"} killed {driver}{vehicle} with {dmgtype} at {location}' )
                continue
            o = LOG_RESPAWN.match(line)
            if o:
                # datetime, player, location
                when = o[1]
                whom = Color.GREEN(o[2])
                where = Color.YELLOW(o[3])
                print(f'{o[1]}{RESPAWN}: {whom} at? {where}')
                continue
    except KeyboardInterrupt:
        f.close()
    except FileNotFoundError:
        print(Color.RED(f"Log file {filepath} not found."))
        print("Run this again from within the game folder after starting the game, or specify a game log to read.")


if __name__ == '__main__':
    filename = "Game.log"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    if not os.path.isfile(filename):
        filename = r"C:\Program Files\Roberts Space Industries\StarCitizen\4.0_PREVIEW\Game.log"
    show_npc_victims = True
    main(filename, show_npc_victims)

# vim: set expandtab ts=4 sw=4
