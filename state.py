from argparse import Namespace
from dataclasses import dataclass, field
from re import Match
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from handlers.handler import Handler


@dataclass
class State:
    args: Namespace = field(default_factory=Namespace)
    cet_steps: int = 0
    count: dict[str, int] = field(default_factory=dict)
    handlers: dict[str, "Handler"] = field(default_factory=dict)
    header_width = 9
    prev_event: tuple[str, Match[str]] | None = None
