import re

from colorize import Color
from handlers.compatibility import CompatibleAll

from .handler import Handler


class ActorStall(CompatibleAll, Handler):
    header = ("STALL", Color.WHITE, False)
    pattern = re.compile(
        r"\[Notice\] \<Actor stall\> Actor stall detected, Player: ([\w-]+), Type: (?:up|down)stream, Length: (\d+\.\d+)\. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data):
        return f"{data[1]} {data[2]}"
