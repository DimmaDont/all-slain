from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from handlers.handler import Handler


@dataclass
class State:
    cet_steps: int = 0
    count: dict[str, int] = field(default_factory=dict)
    handlers: dict[str, "Handler"] = field(default_factory=dict)
    header_width = 9
    is_prev_line_cet: bool = False
