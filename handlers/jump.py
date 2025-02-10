import re

from colorize import Color

from .handler import Handler


class Jump(Handler):
    header = ("JUMP", Color.GREEN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Changing Solar System>.* Client entity ([\w-]*) .* changing system from ([\w-]*) to ([A-Za-z0-9]*) .*"
    )

    def format(self, log: re.Match) -> str:
        whom = Color.GREEN(log[2])
        origin = Color.BLUE(log[3], bold=True)
        dest = Color.BLUE(log[4], bold=True)
        return f"{whom} has departed {origin} for the {dest} system."
