import re

from colorize import Color

from .handler import Handler


class Quit(Handler):
    header = ("QUIT", Color.CYAN, False)
    pattern = re.compile(r"\[Notice\] <SystemQuit> CSystem::Quit invoked ")

    def format(self, _) -> str:
        return "Game quit."
