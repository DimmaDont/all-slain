import re

from colorize import Color

from .handler import Handler


class Branch(Handler):
    header = ("BRANCH", Color.WHITE, False)
    pattern = re.compile(r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> Branch: (.+)")

    def format(self, log: re.Match[str]):
        # Delete after use -- appears only once per log file
        del self.state.handlers["BRANCH"]

        # Quantum is only available for 4.0.0
        if log[2] != "sc-alpha-4.0.0":
            del self.state.handlers["QUANTUM"]

        return Color.CYAN(log[2])
