import json
import re


def main(game_xml: str, outfile):
    p = re.compile(
        r"\s+\<EntityClassDefinition\.(\w+) Category=\"Default\" Icon=\"Default.bmp\" Invisible=\"0\" BBoxSelection=\"\d\" entityDensityClass=\".*?\" __type=\"EntityClassDefinition\" __ref=\".*?\" __path=\"libs/foundry/records/entities/spaceships/"
    )
    ships = []
    with open(game_xml, "r", encoding="latin-1", newline="\r\n") as f:
        while True:
            if not (line := f.readline()):
                break
            if match := p.match(line):
                ships.append(match[1])
    with open(outfile, "w", encoding="latin-1") as f:
        f.write("SHIPS = " + json.dumps(ships, indent=4) + "\n")


if __name__ == "__main__":
    main("../LIVE_EXTRACT/Data/Game2.xml", "src/data/ships_all.py")
