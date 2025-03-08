import re

from colorize import Color

from .handler import Handler


class Spawn(Handler):
    header = ("LOAD", Color.WHITE, True)
    pattern = re.compile(r"\[CSessionManager::OnClientSpawned\] Spawned!")

    def format(self, _) -> str:
        return "Character spawned!"
