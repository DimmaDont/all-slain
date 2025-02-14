import json
import re


def main(game_xml: str, outfile):
    p = re.compile(
        r".*EntityClassDefinition\..*((?:PU|EA)_AI_.*) Category=\"Default\" .*"
    )
    vehicle_types = {}
    with open(game_xml, "r", encoding="latin-1", newline="\r\n") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if match := p.match(line):
                classname = str(match[1])
                vehicle_types[classname] = classname
    vehicle_types = dict(sorted(vehicle_types.items(), key=lambda x: x[0].lower()))
    with open(outfile, "w", encoding="latin-1") as f:
        f.write("VEHICLE_TYPES = " + json.dumps(vehicle_types, indent=4) + "\n")


if __name__ == "__main__":
    main(R"..\\LIVE_EXTRACT\\Data\\Game2.xml", "data\\vehicle_types.py")
