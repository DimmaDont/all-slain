import re
import sys
import time


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
	try:
		f = open(filepath, "r")
		for line in follow(f):
			m = LOG_KILL.match(line)
			if m:
				# datetime, killed, location, killer, killed_using
				killed = clean_name(m[2])
				if "NPC" in killed:
					if show_npc_victims:
						print( f'{m[1]}    KILL: {clean_name(m[4])} {clean_tool(m[5])} {killed} at {clean_location(m[3])}' )
						continue
					else:
						continue
				else:
					print( f'{m[1]}   KILL: {clean_name(m[4])} {clean_tool(m[5])} {killed} at {clean_location(m[3])}' )
					continue
			n = LOG_VEHICLE_KILL.match(line)
			if n:
				# datetime, vehicle, location, driver, caused_by, damage_type
				print( f'{n[1]}  VKILL: {clean_location(n[3])} {n[4]} {clean_location(n[2])} {n[5]} {n[6]}' )
				continue
			o = LOG_RESPAWN.match(line)
			if o:
				# datetime, player, location
				print( f'{o[1]} RESPAWN: {o[2]} {o[3]}' )
				continue
	except KeyboardInterrupt:
		f.close()
	except FileNotFoundError:
		print("Run this again from within the game folder after starting the game, or specify a game log to read.")


if __name__ == '__main__':
	filename = "Game.log"
	if len(sys.argv) >= 2:
		filename = sys.argv[1]
	show_npc_victims = True
	main(filename, show_npc_victims)
