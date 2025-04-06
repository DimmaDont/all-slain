import re

from colorize import Color
from functions_color import color_info
from handlers.compatibility import CompatibleAll

from .handler import Handler


class Session(CompatibleAll, Handler):
    header = ("SESSION", Color.CYAN, False)
    pattern = re.compile(r"\[Trace\] @session:\s+'([\w-]+)'")

    def format(self, data) -> str:
        session_id = color_info(data[1])
        return session_id
