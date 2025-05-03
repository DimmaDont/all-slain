import re

from ..colorize import Color
from ..functions_color import color_player_default
from .compatibility import CompatibleAll
from .handler import Handler


LOG_INCAP_CAUSE = re.compile(r"([\w\d]+) \((\d.\d+) damage\)(?:, )?")


class Incap(CompatibleAll, Handler):
    header = ("INCAP", Color.YELLOW, False)
    pattern = re.compile(r"Logged an incap\.! nickname: ([\w-]+), causes: \[(.+)\]")

    def format(self, data) -> str:
        # datetime, player, causes
        whom = color_player_default(data[1])
        causes = LOG_INCAP_CAUSE.findall(data[2])
        damage_types = [
            Color.YELLOW(cause[0].replace("Damage", "")) for cause in causes
        ]
        return f"{whom} from {', '.join(damage_types)}"
