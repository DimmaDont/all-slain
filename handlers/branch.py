import re

from colorize import Color

from .handler import Handler


class Branch(Handler):
    header = ("BRANCH", Color.WHITE, False)
    pattern = re.compile(r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> Branch: (.+)")

    def format(self, data):
        return Color.CYAN(data[2])

    def after(self, data):
        # Remove from handlers after use -- appears only once per log file
        del self.state.handlers["BRANCH"]

        version = data[2].rsplit("-", maxsplit=1)[-1]

        # ClientQuantum is only available for 4.0.0
        if version != "4.0.0":
            del self.state.handlers["CLIENTQUANTUM"]

        if version == "4.0.2":
            # 4.0.2 added a ReadyToReplicate step
            self.state.cet_steps = 16
        else:
            self.state.cet_steps = 15
