import re

from ..colorize import Color
from .compatibility import CompatibleAll
from .handler import Handler


class Loading(CompatibleAll, Handler):
    header = ("LOAD", Color.WHITE, True)
    pattern = re.compile(
        r"\[CGlobalGameUI::OpenLoadingScreen\] Request context transition to LoadingScreenView"
    )

    def format(self, _) -> str:
        return "Loading..."
