import re

from semver import Version

from colorize import Color

from .cet import Cet
from .character import Character
from .connected import Connected
from .connecting import Connecting
from .corpse import (
    Corpse402Corpsify,
    Corpse402HospitalLocation,
    Corpse402IsCorpseEnabled,
    CorpseHospitalLocation,
)
from .endsession import EndSession
from .enter_leave import VehicleEnterLeave
from .handler import Handler
from .incap import Incap
from .jump import Jump
from .killp import KillP, KillP402
from .killv import KillV
from .loaded import Loaded
from .loading import Loading
from .quantum import ClientQuantum, Quantum
from .quit import Quit
from .spawn import Spawn


HANDLERS_402: list[type[Handler]] = [
    Cet,
    Character,
    VehicleEnterLeave,
    KillP402,
    KillV,
    Corpse402HospitalLocation,
    Corpse402Corpsify,
    Corpse402IsCorpseEnabled,
    Incap,
    EndSession,
    Spawn,
    Jump,
    Connected,
    Connecting,
    Loaded,
    Loading,
    Quit,
]

HANDLERS_400: list[type[Handler]] = [
    Cet,
    Character,
    VehicleEnterLeave,
    KillP,
    KillV,
    Quantum,
    ClientQuantum,
    CorpseHospitalLocation,
    Incap,
    EndSession,
    Spawn,
    Jump,
    Connected,
    Connecting,
    Loaded,
    Loading,
    Quit,
]


RE_SC_VERSION = re.compile(r"sc-alpha-(\d\.\d+(?:\.\d+)?)-?\w?")


class Branch(Handler):
    header = ("BRANCH", Color.WHITE, False)
    pattern = re.compile(r"Branch: (.+)")

    def format(self, data):
        return Color.CYAN(data[1])

    def after(self, data):
        version = Version.parse(RE_SC_VERSION.match(data[1])[1], True)
        if version >= Version(4, 0, 2):
            # 4.0.2 added a ReadyToReplicate step
            self.state.cet_steps = 16

            for handler in HANDLERS_402:
                self.state.handlers[handler.name()] = handler(self.state)
        else:
            # 4.0.1 and below
            self.state.cet_steps = 15

            for handler in HANDLERS_400:
                self.state.handlers[handler.name()] = handler(self.state)

            # ClientQuantum is only available for 4.0.0
            if version != Version(4, 0, 0):
                del self.state.handlers[ClientQuantum.name()]

        if not self.state.args.player_lookup and not self.state.args.planespotting:
            del self.state.handlers[Character.name()]

        if not self.state.args.planespotting:
            del self.state.handlers[VehicleEnterLeave.name()]

        if self.state.args.debug:
            self.state.count = {p[0]: 0 for p in self.state.handlers.items()}

        # Remove from handlers after use -- appears only once per log file
        del self.state.handlers[self.name()]
