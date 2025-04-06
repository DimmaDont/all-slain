import re

from colorize import Color
from functions import get_location
from functions_color import color_location

from .compatibility import SinceV402, V401AndBelow
from .handler import PlayerLookupHandler


class CorpseHospitalLocation(V401AndBelow, PlayerLookupHandler):
    header = ("RESPAWN", Color.CYAN, False)
    pattern = re.compile(
        r"\[Notice\] <Corpse> Player '([\w-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data) -> str:
        # datetime, player, location
        player_str = self.format_player(data[1], False)
        _, where, location_type = get_location(data[2])
        location_str = color_location(where, location_type)
        return f"{player_str} from {location_str}"


class Corpse402HospitalLocation(SinceV402, CorpseHospitalLocation):
    pattern = re.compile(
        r"\[Notice\] <\[ActorState\] Corpse> \[ACTOR STATE\]\[SSCActorStateCVars::LogCorpse\] Player '([\w-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital\. \[Team_ActorTech\]\[Actor\]"
    )


class Corpse402Corpsify(SinceV402, PlayerLookupHandler):
    header = ("CORPSE", Color.RED, True)
    pattern = re.compile(
        r"\[Notice\] <\[ActorState\] Corpse> \[ACTOR STATE\]\[SSCActorStateCVars::LogCorpse\] Player '([\w-]+)' <(?:remote|local) client>: Running corpsify for corpse\. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data) -> str:
        return f"{self.format_player(data[1], False)} {Color.BLACK('(corpsify)', True)}"


class Corpse402IsCorpseEnabled(Corpse402Corpsify):
    pattern = re.compile(
        r"\[Notice\] <\[ActorState\] Corpse> \[ACTOR STATE\]\[SSCActorStateCVars::LogCorpse\] Player '([\w-]+)' <(?:remote|local) client>: IsCorpseEnabled"
    )

    def format(self, data) -> str:
        return self.format_player(data[1], False)
