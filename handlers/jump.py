import re

from colorize import Color
from handlers.compatibility import CompatibleAll

from .handler import Handler


class Jump(CompatibleAll, Handler):
    header = ("JUMP", Color.GREEN, False)
    pattern = re.compile(
        r"\[Notice\] <Changing Solar System>.* Client entity ([\w-]*) .* changing system from (\w+) to (\w+) "
    )

    def format(self, data) -> str:
        whom = Color.GREEN(data[1])
        origin = Color.BLUE(data[2], bold=True)
        dest = Color.BLUE(data[3], bold=True)
        return f"{whom} has entered {dest} from the {origin} system."
