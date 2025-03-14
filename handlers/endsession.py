import re

from colorize import Color

from .cet import Cet
from .handler import Handler


class EndSession(Handler):
    header = ("QUIT", Color.CYAN, False)
    pattern = re.compile(
        r"\[Notice\] <CDisciplineServiceExternal::EndSession> Ending session "
    )

    def format(self, _) -> str:
        return "Ending game session"

    def after(self, _):
        # Add CET to beginning
        self.state.handlers = {Cet.name(): Cet(self.state)} | self.state.handlers
