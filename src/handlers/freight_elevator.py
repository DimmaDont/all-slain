import re
from typing import TYPE_CHECKING

from ..colorize import Color
from .compatibility import SinceV324, SinceV411
from .handler import Handler


if TYPE_CHECKING:
    from ..state import State


class FreightElevator(SinceV324, Handler):
    header = ("FREIGHT", Color.CYAN, False)
    pattern = re.compile(
        r"\[Notice\] <CSCLoadingPlatformManager::OnLoadingPlatformStateChanged> \[Loading Platform\] Loading Platform Manager \[(\w+)\] Platform state changed to (\w+) \[Team_NAPU\]\[Cargo\]"
    )

    def __init__(self, state: "State") -> None:
        super().__init__(state)
        self.prev: str | None = None

    def format(self, data: re.Match[str]) -> str:
        freight_elevator = data[1]
        state = data[2]

        if (
            not self.state.args.verbose
            and self.state.prev_event
            and self.state.prev_event[1] == self.name()
            and self.prev not in ["ClosedIdle", "OpenIdle"]
        ):
            print("\x1b[1A\x1b[2K", end="")
        self.prev = state

        freight_elevator_str = Color.YELLOW(freight_elevator)
        state_str = Color.CYAN(state)
        return f"{freight_elevator_str} is now {state_str}"


class FreightElevator411(SinceV411, FreightElevator):
    pattern = re.compile(
        r"\[Notice\] <CSCLoadingPlatformManager::St(?:art|op)EffectForAllTags> \[Loading Platform\] Loading Platform Manager \[(\w+)\] st(?:opp|art)ing effects in current platform state: (\w+) \[Team_CGP7\]\[Cargo\]"
    )
