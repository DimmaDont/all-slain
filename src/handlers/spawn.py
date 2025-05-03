import re

from ..colorize import Color
from .compatibility import CompatibleAll
from .handler import Handler


class Spawn(CompatibleAll, Handler):
    header = ("LOAD", Color.WHITE, True)
    pattern = re.compile(r"\[CSessionManager::OnClientSpawned\] Spawned!")

    def format(self, _) -> str:
        return "Character spawned!"
