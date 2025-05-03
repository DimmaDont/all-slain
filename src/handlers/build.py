import re

from ..colorize import Color
from .cet import Cet
from .character import Character
from .compatibility import CompatibleAll
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
from .killp import KillP
from .killv import KillV
from .loaded import Loaded
from .loading import Loading
from .med_bed_heal import MedBedHeal
from .quantum import ClientQuantum, Quantum
from .quit import Quit
from .spawn import Spawn


HANDLERS: list[type[Handler]] = [
    Cet,
    Character,
    VehicleEnterLeave,
    KillP,
    KillV,
    Quantum,
    ClientQuantum,
    CorpseHospitalLocation,
    Corpse402HospitalLocation,
    Corpse402Corpsify,
    Corpse402IsCorpseEnabled,
    Incap,
    Spawn,
    EndSession,
    Jump,
    Connected,
    Connecting,
    Loaded,
    Loading,
    MedBedHeal,
    Quit,
]


class Build(CompatibleAll, Handler):
    header = ("VERSION", Color.WHITE, False)
    pattern = re.compile(r"Changelist: (\d+)")
    branch: str

    def format(self, data):
        return f"{Color.CYAN(self.branch)} build {Color.CYAN(data[1])}"

    def after(self, data):
        build = int(data[1])
        assert self.state.version

        handlers = [h for h in HANDLERS if h.is_compatible(self.state.version, build)]

        self.state.header_width = max(len(h.header[0]) for h in handlers) + 1

        for handler in handlers:
            self.state.handlers[handler.name()] = handler(self.state)

        if not self.state.args.player_lookup and not self.state.args.planespotting:
            del self.state.handlers[Character.name()]

        if not self.state.args.planespotting:
            try:
                del self.state.handlers[VehicleEnterLeave.name()]
            except KeyError:
                # Might not have been added
                pass

        if self.state.args.debug:
            self.state.count = {p[0]: 0 for p in self.state.handlers.items()}

        # Remove from handlers after use -- appears only once per log file
        del self.state.handlers[self.name()]
