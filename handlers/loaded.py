import re
from datetime import timedelta

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
        r"Loading screen for (\w+) : \w+ closed after (\d+.\d+) seconds"
    )

    def format(self, data) -> str:
        what = Color.GREEN(LOADED_ITEM.get(data[1], data[1]))
        running_time_text = Color.GREEN(
            str(timedelta(seconds=float(data[2]))).rstrip("0")
        )
        return f"Loaded! {what} took {running_time_text} to load."
