from dataclasses import dataclass, field
from re import Match
from typing import TYPE_CHECKING

from args import Args


if TYPE_CHECKING:
    from data_providers.provider import BaseProvider
    from handlers.handler import Handler


@dataclass
class State:
    args: Args = field(default_factory=Args)
    cet_steps: int = 0
    count: dict[str, int] = field(default_factory=dict)
    data_provider: "BaseProvider | None" = None
    handlers: dict[str, "Handler"] = field(default_factory=dict)
    header_width = 9
    player_name: str = ""

    prev_event: tuple[str, str, Match[str]] | None = None
    """log time str, event type, match"""

    curr_event_timestr: str = ""
