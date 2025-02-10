from datetime import timedelta
import re

from colorize import Color

from .handler import Handler


LOADED_ITEM = {
    "pu": "PU",
    "pyro": "Pyro",
    "Frontend_Main": "Main Menu",
}


class Loaded(Handler):
    header = ("LOAD", Color.WHITE, True)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> Loading screen for (\w+) : SC_Frontend closed after (\d+.\d+) seconds"
    )

    def format(self, log: re.Match) -> str:
        what = Color.GREEN(LOADED_ITEM.get(log[2], log[2]))
        running_time_text = Color.GREEN(
            str(timedelta(seconds=float(log[3]))).rstrip("0")
        )
        return f"Loaded! {what} took {running_time_text} to load."
