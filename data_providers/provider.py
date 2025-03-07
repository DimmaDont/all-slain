from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, final

from colorize import Color


if TYPE_CHECKING:
    from state import State


class Theme(Enum):
    """
    Theme names and colors are from RSI org css
    """

    PROFIT = (0xFF, 0xF0, 0)
    DEFAULT = (0x6D, 0xB9, 0xD8)
    LIGHT = (0xD7, 0xD7, 0xD7)
    RAGE = (0xFF, 0, 0)
    FORCE = (0x50, 0xD3, 0x78)


@dataclass
class Org:
    sid: str
    # name: str
    theme: Theme = Theme.DEFAULT

    def __str__(self) -> str:
        return Color.rgb(self.theme.value, text=self.sid)


@dataclass
class Player:
    # UEE Citizen Record
    # ucr: str | None

    # Community Moniker
    # cm: str

    handle: str

    # Spectrum ID
    main_org: str | None = None

    # enlisted: datetime
    # location: str
    # fluency: list[str]
    # orgs: list[Org] | None

    def __str__(self) -> str:
        return self.handle


class BaseProvider(ABC):
    def __init__(self, state: "State"):
        self.state = state

        self.org_info: dict[str, "Org"] = {}
        self.player_info: dict[str, "Player"] = {}

        # Set by Character handler
        self.player_name: str = ""

    @abstractmethod
    def _lookup_player(self, handle: str) -> Player: ...

    @final
    def lookup_player(self, handle: str) -> Player:
        if self.player_name == handle:
            return Player(handle)
        player = self.player_info.get(handle)
        if not player:
            player = self._lookup_player(handle)
            self.player_info[handle] = player
        return player

    @abstractmethod
    def _lookup_org(self, spectrum_id: str) -> Org: ...

    @final
    def lookup_org(self, spectrum_id: str) -> Org:
        org = self.org_info.get(spectrum_id)
        if not org:
            org = self._lookup_org(spectrum_id)
            self.org_info[spectrum_id] = org
        return org
