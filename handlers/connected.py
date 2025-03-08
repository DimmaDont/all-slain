import re

from colorize import Color

from .handler import Handler


class Connected(Handler):
    header = ("CONNECT", Color.WHITE, True)
    pattern = re.compile(r"\[CSessionManager::OnClientConnected\] Connected!")

    def format(self, _) -> str:
        return "Connected!"
