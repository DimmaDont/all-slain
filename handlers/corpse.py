import re

from colorize import Color
from functions import clean_location

from .handler import PlayerLookupHandler


class CorpseHospitalLocation(PlayerLookupHandler):
    header = ("RESPAWN", Color.CYAN, False)
    pattern = re.compile(
        r"\[Notice\] <Corpse> Player '([\w-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data) -> str:
        # datetime, player, location
        player_text = self.format_player(data[1], False)
        _, where, _ = clean_location(data[2])
        return f"{player_text} from {Color.YELLOW(where)}"


class Corpse402HospitalLocation(CorpseHospitalLocation):
    pattern = re.compile(
        r"\[Notice\] <\[ActorState\] Corpse> \[ACTOR STATE\]\[SSCActorStateCVars::LogCorpse\] Player '([\w-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital\. \[Team_ActorTech\]\[Actor\]"
    )


class Corpse402Corpsify(PlayerLookupHandler):
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
