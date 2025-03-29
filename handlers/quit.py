import re

from colorize import Color
from handlers.compatibility import CompatibleAll

from .handler import Handler


class Quit(CompatibleAll, Handler):
    header = ("QUIT", Color.CYAN, False)
    pattern = re.compile(r"\[Notice\] <SystemQuit> CSystem::Quit invoked ")

    def format(self, _) -> str:
        return "Game quit."
