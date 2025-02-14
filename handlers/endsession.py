import re

from colorize import Color

from .handler import Handler


class EndSession(Handler):
    header = ("QUIT", Color.CYAN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <CDisciplineServiceExternal::EndSession> Ending session .*"
    )

    def format(self, data):
        return "Ending game session"

    def after(self, _):
        # Move CET to beginning
        self.state.handlers = {"CET": None} | self.state.handlers
