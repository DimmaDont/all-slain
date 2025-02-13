import re

from colorize import Color

from .handler import Handler


class Session(Handler):
    header = ("SESSION", Color.CYAN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Trace\] @session:\s+'([\w-]+)'"
    )

    def format(self, data) -> str:
        session_id = Color.CYAN(data[2])
        return session_id
