import re
from typing import TYPE_CHECKING

from semver import Version

from ..colorize import Color
from ..data.elevators import ELEVATORS
from ..functions import get_location, strip_id
from ..functions_color import color_location
from .compatibility import SinceV410, SinceV420
from .handler import Handler


if TYPE_CHECKING:
    from ..state import State


# Available since Hotfix | 1.31.2025 | sc-alpha-4.0.1-9505265-LIVE


class Elevator401(Handler):
    header = ("ELEVATOR", Color.CYAN, False)
    pattern = re.compile(
        r"\[Notice\] <TransitCarriage(?:Start|Finish)Transit> \[TRANSITDEBUG\] \[TRANSIT CARRIAGE\] \[ECarriageGeneral\] : Carriage (\d+) \(Id: \d+\) for manager (\w+) (starting|finished) transit in zone (\w+) \[Team_ArenaCommanderFeature\]\[TransitSystem\]"
    )

    @classmethod
    def is_compatible(cls, version, build):
        # 4.0.1 9505265 to < 4.1.0
        return build >= 9505265 and Version(4, 0, 1) <= version < Version(4, 1, 0)

    def __init__(self, state: "State") -> None:
        super().__init__(state)
        self.prev: tuple[str | None, str, str, str] | None = None

    def format(self, data: re.Match[str]) -> tuple[int, str]:
        elevator_id = data[1]
        zone = data[4]
        action = data[3]
        manager = strip_id(data[2])
        this = (elevator_id, manager, action, zone)
        lc = 0
        if (
            not self.state.args.verbose
            and self.prev
            and self.prev[0] == elevator_id
            and self.prev[1] == manager
            and self.prev[2] == "starting"
            and action == "finished"
            and self.state.prev_event
            and self.state.prev_event[1] == self.name()
        ):
            lc = -1
        self.prev = this

        elevator_name = ELEVATORS.get(manager, manager)
        elevator_str = Color.CYAN(elevator_name)

        _, location_name, location_type = get_location(zone)
        location_str = color_location(location_name, location_type)
        location_p = "to" if action == "finished" else "from"

        return (
            lc,
            f"Elevator {elevator_str} {elevator_id} {action} moving {location_p} {location_str}",
        )


class Elevator410(SinceV410, Elevator401):
    pattern = re.compile(
        r"\[Notice\] <TransitCarriage(?:Start|Finish)Transit> \[TRANSITDEBUG\] \[TRANSIT CARRIAGE\] \[ECarriageGeneral\] : Carriage (\d+) \(Id: \d+\) for manager (\w+) (starting|finished) transit in zone (\w+) at position x: -?\d+\.\d+, y: -?\d+\.\d+, z: -?\d+\.\d+ \[Team_ArenaCommanderFeature\]\[TransitSystem\]"
    )
    # Now with coordinates


class Elevator420(SinceV420, Elevator401):
    pattern = re.compile(
        r"\[Notice\] <TransitCarriage(?:Start|Finish)Transit> \[TRANSITDEBUG\] \[TRANSIT CARRIAGE\] \[ECarriageGeneral\] : Carriage (\d+) \(Id: \d+\) for manager (\w+) (starting|finished) transit in zone (\w+) at position x: -?\d+\.\d+, y: -?\d+\.\d+, z: -?\d+\.\d+ \[Team_CGP2\]\[TransitSystem\]"
    )
    # Team changed
