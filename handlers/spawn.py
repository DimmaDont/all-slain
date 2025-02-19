import re

from colorize import Color

from .handler import Handler


class Spawn(Handler):
    header = ("LOAD", Color.WHITE, True)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[CSessionManager::OnClientSpawned\] Spawned!"
    )

    def format(self, _) -> str:
        return "Character spawned!"
