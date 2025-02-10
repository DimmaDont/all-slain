import re

from colorize import Color

from .handler import Handler


class QuitLobby(Handler):
    header = ("QUIT", Color.CYAN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <\[EALobby\] EALobbyQuit> \[EALobby\]\[CEALobby::RequestQuitLobby\] ([\w-]+) Requesting QuitLobby.*"
    )

    def format(self, log: re.Match) -> str:
        whom = Color.GREEN(log[2])
        return f"{whom} has quit the game session."
