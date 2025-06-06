import re

from ..colorize import Color
from ..functions_color import color_info
from .compatibility import CompatibleAll
from .handler import Handler


class Character(CompatibleAll, Handler):
    header = ("LOGIN", Color.WHITE, False)
    pattern = re.compile(
        r"\[Notice\] <AccountLoginCharacterStatus_Character> Character: createdAt \d+ - updatedAt \d+ - geid \d+ - accountId \d+ - name ([\w-]+) - state STATE_(CURRENT|UNSPECIFIED) "
    )

    def format(self, data):
        return color_info(data[1])

    def after(self, data):
        self.state.player_name = data[1]

        # Remove from handlers after use -- appears only once per log file
        del self.state.handlers[self.name()]
