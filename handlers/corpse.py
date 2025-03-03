import re

from colorize import Color
from functions import clean_location

from .handler import Handler


class CorpseHospitalLocation(Handler):
    header = ("RESPAWN", Color.CYAN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Corpse> Player '([\w-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data) -> str:
        # datetime, player, location
        whom = Color.GREEN(data[2])
        _, where, _ = clean_location(data[3])
        return f"{whom} from {Color.YELLOW(where)}"


class Corpse402HospitalLocation(CorpseHospitalLocation):
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <\[ActorState\] Corpse> \[ACTOR STATE\]\[SSCActorStateCVars::LogCorpse\] Player '([\w-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital\. \[Team_ActorTech\]\[Actor\]"
    )


class Corpse402Corpsify(Handler):
    header = ("CORPSE", Color.CYAN, True)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <\[ActorState\] Corpse> \[ACTOR STATE\]\[SSCActorStateCVars::LogCorpse\] Player '([\w-]+)' <remote client>: Running corpsify for corpse\. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data) -> str:
        return f"Corpsify: {Color.GREEN(data[2])}"


class Corpse402IsCorpseEnabled(Corpse402Corpsify):
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <\[ActorState\] Corpse> \[ACTOR STATE\]\[SSCActorStateCVars::LogCorpse\] Player '([\w-]+)' <remote client>: IsCorpseEnabled: (Yes, there is no local inventory|No)\. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data) -> str:
        return f"Corpse? {Color.GREEN(data[2])}"


class Corpse402Dead(Corpse402Corpsify):
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <\[ActorState\] Corpse> \[ACTOR STATE\]\[SSCActorStateCVars::LogCorpse\] Player '([\w-]+)' <local client>: Entering control state dead\. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data) -> str:
        return f"Dead: {Color.GREEN(data[2])}"


class Corpse402EntityId(Corpse402Corpsify):
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <\[ActorState\] Corpse> \[ACTOR STATE\]\[SSCActorStateCVars::LogCorpse\] Player '([\w-]+)' <local client>: Setting corpse entity id from validation\. \[Team_ActorTech\]\[Actor\]"
    )

    def format(self, data) -> str:
        return f"Corpse: {Color.GREEN(data[2])}"
