from __future__ import annotations

from abc import ABC, abstractmethod
from re import Match, Pattern
from typing import TYPE_CHECKING

from semver import Version

from ..colorize import Color
from ..functions_color import (
    color_player_default,
    color_player_npc,
    color_player_with_org,
)


if TYPE_CHECKING:
    from ..state import State


class Handler(ABC):
    header: tuple[str, Color, bool]
    pattern: Pattern[str]

    def __init__(self, state: State):
        self.state = state
        self.set_header_text(self.header[0], self.header[1], self.header[2])

    def set_header_text(self, text: str, color: Color, bold: bool) -> None:
        self.header_text = color(text.rjust(self.state.header_width), bold=bold)

    def __call__(self, data: Match[str]) -> None:
        if text := self.format(data):
            print(f"{self.state.curr_event_timestr}{self.header_text}: {text}")
        self.after(data)

    @classmethod
    def name(cls) -> str:
        return cls.__name__.upper()

    @abstractmethod
    def format(self, data: Match[str]) -> str | None: ...

    @classmethod
    @abstractmethod
    def is_compatible(cls, version: Version, build: int) -> bool: ...

    # pylint: disable=unused-argument
    def after(self, data: Match[str]) -> None: ...


class PlayerLookupHandler(Handler):
    def format_player(self, handle: str, is_actor_npc: bool) -> str:
        if is_actor_npc:
            return color_player_npc(handle)
        if self.state.args.player_lookup and self.state.data_provider:
            player = self.state.data_provider.lookup_player(handle)
            if not player.main_org:
                return color_player_default(player)
            main_org = (
                self.state.data_provider.lookup_org(player.main_org)
                if self.state.args.data_provider.use_org_theme
                else player.main_org
            )
            return color_player_with_org(player, main_org)
        return color_player_default(handle)
