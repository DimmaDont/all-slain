import re

from colorize import Color

from .handler import Handler


class Jump(Handler):
    header = ("JUMP", Color.GREEN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Changing Solar System>.* Client entity ([\w-]*) .* changing system from (\w+) to (\w+) .*"
    )

    def format(self, data) -> str:
        whom = Color.GREEN(data[2])
        origin = Color.BLUE(data[3], bold=True)
        dest = Color.BLUE(data[4], bold=True)
        return f"{whom} has entered {dest} from the {origin} system."
