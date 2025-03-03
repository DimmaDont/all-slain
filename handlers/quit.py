import re

from colorize import Color

from .handler import Handler


class Quit(Handler):
    header = ("QUIT", Color.CYAN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <SystemQuit> CSystem::Quit invoked .+"
    )

    def format(self, _) -> str:
        return "Game quit."
