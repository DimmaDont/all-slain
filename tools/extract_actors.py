import json
import re


def main(game_xml: str, outfile):
    p = re.compile(
        r".*EntityClassDefinition\.(.*?)(?:_\d\d)? Category=\"Actors\" .*\/(.*?)(?:_\d\d)?\.xml.*"
    )
    actors = {}
    with open(game_xml, "r", encoding="latin-1", newline="\r\n") as f:
        while line := f.readline():
            match = p.match(line)
            if not match:
                continue

            classname = str(match[1])
            if any(
                [
                    classname.startswith("AIShip_CrewProfiles"),
                    classname.startswith("FeatureTest_"),
                    "MissionGivers" in classname,
                    "Test" in classname,
                    "TEST" in classname,
                    "TEMPLATE" in classname,
                    "Debug" in classname,
                ]
            ):
                continue

            for index in range(len(classname)):
                if match[2][index] == "-":
                    classname = classname[:index] + "-" + classname[index + 1 :]

            name = (
                str(match[1])
                .replace("_", "-")
                .replace("-", " ")
                .replace(" Civilians ", " Civilian ")
                .replace(" Female ", " ")
                .replace(" GroundCombat ", " ")
                .replace(" Guards ", " ")
                .replace(" Human ", " ")
                .replace(" Male ", " ")
                .replace(" Populace ", " ")
                .replace(" Pyro ", " ")
                .removeprefix("PU Enemy ")
                .removeprefix("PU Pilots ")
                .removeprefix("PU ")
                .removeprefix("NPC Archetypes ")
                .removeprefix("NPC Archetype ")
                .removeprefix("NPC ")
                .replace(" NewBabbage ", " New Babbage ")
                .removesuffix(" Area18")
                .removesuffix(" NewBabbage")
                .removesuffix(" Orison")
                .removesuffix(" Pyro")
                .removesuffix(" Reststop")
                .removesuffix(" Stanton")
                .removesuffix(" Utilitarian")
                .replace("Boss Boss", "Boss")
                .replace("Contestedzones", "CZ")
                .replace("contestedzones", "CZ")
                .replace("xenothreat", "XenoThreat")
                .replace("Xenothreat", "XenoThreat")
                .replace("captain", "Captain")
                .replace("cqc", "CQC")
                .replace("grunt", "Grunt")
                .replace("juggernaut", "Juggernaut")
                .replace("sniper", "Sniper")
                .replace("soldier", "Soldier")
                .replace("techie", "Techie")
                .replace("pyro outlaw", "Outlaw")
                .replace("Grunt Grunt", "Grunt")
                .replace("distributioncentre ", "DC ")
                .replace("vlk", "Valakkar")
                .replace("Ninetails", "NineTails")
                .strip()
            )
            actors[classname] = name
    with open(outfile, "w", encoding="latin-1") as f:
        f.write("ACTORS = " + json.dumps(actors, indent=4) + "\n")


if __name__ == "__main__":
    main("../LIVE_EXTRACT/Data/Game2.xml", "src/data/actors.py")
