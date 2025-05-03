import re


RE_TIME = re.compile(r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)> (.*)")

RE_EVENT = re.compile(r"(?:\[SPAM \d+\])?(.*?>)")

KNOWN_EVENTS: list[str] = [
    "[Notice] <Actor Death>",
]

SEEN = []


def main(channel: str = "LIVE"):
    with open(Rf"..\{channel}\Game.log", encoding="latin-1", newline="\r\n") as f:
        for line in f.readlines():
            logtime = RE_TIME.match(line)
            if not logtime:
                continue

            match = RE_EVENT.match(logtime[2])
            if not match:
                # print(logtime[2])
                continue

            if match[1] in KNOWN_EVENTS:
                continue

            if match[1] in SEEN:
                continue

            print(match[1])
            SEEN.append(match[1])
            # input()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
