import re
import sys
import time
import colorize as C


LOG_KILL = re.compile(r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Actor Death> CActor::Kill: '([A-Za-z0-9_-]+)' \[\d+\] in zone '([A-Za-z0-9_-]+)' killed by '([A-Za-z0-9_-]+)' \[\d+\] using '[A-Za-z0-9_-]+' \[Class ([A-Za-z0-9_-]+)\] with damage type '([A-Za-z]+)' from direction (.*) \[Team_ActorTech\]\[Actor\]")
LOG_VEHICLE_KILL = re.compile(r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([A-Za-z0-9_-]+)' \[\d+\] in zone '([A-Za-z0-9_-]+)' \[pos.*\] driven by '([A-Za-z0-9_-]+)' \[\d+\] advanced from destroy level \d to \d caused by '([A-Za-z0-9_-]+)' \[[0-9_]+\] with '([A-Za-z]+)' \[Team_VehicleFeatures\]\[Vehicle\]")
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
        name_split = name.split("_")
        return "_".join(name_split[0:1])
    except IndexError:
        return name


def main(filepath, show_npc_victims):
    KILL=f'{C.FG("RED", bold = True )}{"KILL":>10}{C.reset()}'
    VKILL=f'{C.FG("RED", bold = True )}{"VKILL":>10}{C.reset()}'
    RESPAWN=f'{C.FG("CYAN", bold = True )}{"RESPAWN":>10}{C.reset()}'

    try:
        f = open(filepath, "r")
        print( C.reset() )
        for line in follow(f):
            if m := LOG_KILL.match(line):
                # datetime, killed, location, killer, killed_using
                when = m[1]
                killed = C.color( clean_name(m[2]), 'GREEN' )
                location = C.color( clean_location(m[3]), 'YELLOW', True )
                killer = C.color( clean_name(m[4]), 'GREEN' )
                cause = C.color( clean_tool(m[5]).capitalize(), 'CYAN' )
                if "NPC" in killed and not show_npc_victims:
                    continue
                else:
                    if 'Suicide' not in cause:
                        print( f'{when}{KILL}: {killer} killed {killed} with a {cause} at {location}' )
                    else:
                        print( f'{when}{KILL}: {killer} committed {cause} at {location}' )
                    continue
            if n := LOG_VEHICLE_KILL.match(line):
                # datetime, vehicle, location, driver, caused_by, damage_type
                when = n[1]
                vehicle = C.color( clean_location(n[2]), 'GREEN' )
                location = C.color( clean_location(n[3]), 'YELLOW', True )
                driver = C.color( clean_name(n[4]), 'GREEN' ) # the killer
                cause = clean_tool(n[5]).capitalize()
                dmgtype = C.color( n[6], 'CYAN' )
                print( f'{when}{VKILL}: {driver} in a {vehicle} killed by {dmgtype} at {location}' )
                continue
            o = LOG_RESPAWN.match(line)
            if o:
                # datetime, player, location
                when = o[1]
                whom = C.color( o[2], 'GREEN' )
                where = C.color( o[3], 'YELLOW', True )
                print( f'{o[1]}{RESPAWN}: {whom} at {where}' )
                continue
    except KeyboardInterrupt:
        f.close()
    except FileNotFoundError:
        print(f'{C.FG("RED", bold = True)}Log file {filename} not found.{C.reset()}\nRun this again from within the game folder after starting the game, or specify a game log to read.')


if __name__ == '__main__':
    filename = "Game.log"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    show_npc_victims = True
    main(filename, show_npc_victims)

# vim: set expandtab ts=4 sw=4
