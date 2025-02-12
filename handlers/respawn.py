import re

from colorize import Color
from functions import clean_location

from .handler import Handler


class Respawn(Handler):
    header = ("RESPAWN", Color.CYAN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Corpse> Player '([\w-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, log: re.Match) -> str:
        # datetime, player, location
        whom = Color.GREEN(log[2])
        _, where, _ = clean_location(log[3])
        return f"{whom} from {Color.YELLOW(where)}"
