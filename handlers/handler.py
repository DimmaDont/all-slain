from abc import ABC, abstractmethod
from re import Match, Pattern
from typing import TYPE_CHECKING

from colorize import Color


if TYPE_CHECKING:
    from state import State


class Handler(ABC):
    header: tuple[str, Color, bool]
    pattern: Pattern

    def __init__(self, state: "State"):
        self.state = state
        self.header_text = self.header[1](
            self.header[0].rjust(self.state.header_width), bold=self.header[2]
        )

    def __call__(self, data: Match[str]) -> None:
        when = data[1].replace("T", " ")
        print(f"{when}{self.header_text}: {self.format(data)}")
        self.after(data)

    @classmethod
    def name(cls):
        return cls.__name__.upper()

    @abstractmethod
    def format(self, data: Match[str]) -> str: ...

    # pylint: disable=unused-argument
    def after(self, data: Match[str]) -> None: ...


class PlayerLookupHandler(Handler):
    def format_player(self, handle: str, is_actor_npc: bool) -> str:
        if is_actor_npc:
            return Color.BLACK(handle, True)
        if self.state.args.player_lookup and self.state.data_provider:
            player = self.state.data_provider.lookup_player(handle)
            if not player.main_org:
                return Color.GREEN(handle)
            main_org = (
                self.state.data_provider.lookup_org(player.main_org)
                if self.state.args.data_provider.use_org_theme
                else player.main_org
            )
            return f"{Color.GREEN(handle)} {Color.BLACK('(', True)}{main_org}{Color.BLACK(')', True)}"
        return Color.GREEN(handle)
