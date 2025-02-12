import re

from colorize import Color

from .handler import Handler


class Connecting(Handler):
    header = ("CONNECT", Color.WHITE, True)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[CSessionManager::ConnectCmd\] Connect started!"
    )

    def format(self, _: re.Match) -> str:
        return "Connecting..."
