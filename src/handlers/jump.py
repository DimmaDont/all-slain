import re

from ..colorize import Color
from ..functions_color import color_player_default
from .compatibility import V410AndBelow
from .handler import Handler


class Jump(V410AndBelow, Handler):
    header = ("JUMP", Color.GREEN, False)
    pattern = re.compile(
        r"\[Notice\] <Changing Solar System>.* Client entity ([\w-]*) .* changing system from (\w+) to (\w+) "
    )

    def format(self, data) -> str:
        whom = color_player_default(data[1])
        origin = Color.BLUE(data[2], bold=True)
        dest = Color.BLUE(data[3], bold=True)
        return f"{whom} has entered {dest} from the {origin} system."
