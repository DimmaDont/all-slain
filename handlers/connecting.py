import re

from colorize import Color

from .handler import Handler


class Connecting(Handler):
    header = ("CONNECT", Color.WHITE, True)
    pattern = re.compile(r"\[CSessionManager::ConnectCmd\] Connect started!")

    def format(self, _) -> str:
        return "Connecting..."
