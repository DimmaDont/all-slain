import re

from colorize import Color

from .handler import Handler


class Character(Handler):
    header = ("LOGIN", Color.WHITE, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <AccountLoginCharacterStatus_Character> Character: createdAt \d+ - updatedAt \d+ - geid \d+ - accountId \d+ - name ([\w-]+) - state STATE_(CURRENT|UNSPECIFIED) .*"
    )

    def format(self, data):
        return Color.CYAN(data[2])

    def after(self, data):
        self.state.data_provider.player_name = data[2]

        # Remove from handlers after use -- appears only once per log file
        del self.state.handlers[self.name()]
