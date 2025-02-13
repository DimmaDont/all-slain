import re

from colorize import Color

from .handler import Handler


class Loading(Handler):
    header = ("LOAD", Color.WHITE, True)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[CGlobalGameUI::OpenLoadingScreen\] Request context transition to LoadingScreenView"
    )

    def format(self, _) -> str:
        return "Loading..."
