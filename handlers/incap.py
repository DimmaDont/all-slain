import re

from colorize import Color

from .handler import Handler


LOG_INCAP_CAUSE = re.compile(r"([\w\d]+) \((\d.\d+) damage\)(?:, )?")


class Incap(Handler):
    header = ("INCAP", Color.YELLOW, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> Logged an incap\.! nickname: ([\w-]+), causes: \[(.+)\]"
    )

    def format(self, log: re.Match) -> str:
        # datetime, player, causes
        whom = Color.GREEN(log[2])
        causes = LOG_INCAP_CAUSE.findall(log[3])
        damage_types = [
            Color.YELLOW(cause[0].replace("Damage", "")) for cause in causes
        ]
        return f"{whom} from {', '.join(damage_types)}"
