import re

from colorize import Color

from .handler import Handler


class Session(Handler):
    header = ("SESSION", Color.CYAN, False)
    pattern = re.compile(r"\[Trace\] @session:\s+'([\w-]+)'")

    def format(self, data) -> str:
        session_id = Color.CYAN(data[1])
        return session_id
