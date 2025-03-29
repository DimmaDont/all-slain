import re

from colorize import Color
from handlers.compatibility import CompatibleAll

from .handler import Handler


class Connecting(CompatibleAll, Handler):
    header = ("CONNECT", Color.WHITE, True)
    pattern = re.compile(r"\[CSessionManager::ConnectCmd\] Connect started!")

    def format(self, _) -> str:
        return "Connecting..."
