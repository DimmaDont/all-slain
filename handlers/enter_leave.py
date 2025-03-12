import datetime
import re

from colorize import Color
from functions import get_vehicle

from .handler import Handler


class Enter(Handler):
    header = ("ENTER", Color.GREEN, False)
    pattern = re.compile(
        r"(?:\[SPAM \d+\])?\[Notice\] <CEntityComponentInstancedInterior::OnEntityEnterZone> \[InstancedInterior\] OnEntityEnterZone - InstancedInterior \[(.*)\] \[\d{12,}\] -> Entity \[(\w+)\] \[\d{12,}\] -- m_openDoors\[\d\], m_managerGEID\[\d{12,}\], m_ownerGEID\[([\w-]+)\]\[\d{12,}\], m_isPersistent\[\d\] .*"
    )

    def format(self, data) -> str:
        where = Color.CYAN("a hangar" if "_hangar_" in data[1] else data[1])
        what = (
            Color.BLACK("Elevator", True)
            if "_elev_" in data[2]
            else Color.GREEN(get_vehicle(data[2])[0])
        )
        whom = Color.GREEN(data[3])
        return f"{what} has entered {where} owned by {whom}"


class Leave(Handler):
    header = ("LEAVE", Color.GREEN, False)
    pattern = re.compile(
        r"(?:\[SPAM \d+\])?\[Notice\] <CEntityComponentInstancedInterior::OnEntityLeaveZone> \[InstancedInterior\] OnEntityLeaveZone - InstancedInterior \[(.*)\] \[\d{12,}\] -> Entity \[(\w+)\] \[\d{12,}\] -- m_openDoors\[\d\], m_managerGEID\[\d{12,}\], m_ownerGEID\[([\w-]+)\]\[\d{12,}\], m_isPersistent\[\d\] .*"
    )

    def format(self, data) -> str:
        where = Color.CYAN("a hangar" if "_hangar_" in data[1] else data[1])
        what = (
            Color.BLACK("Elevator", True)
            if "_elev_" in data[2]
            else Color.GREEN(get_vehicle(data[2])[0])
        )
        whom = Color.GREEN(data[3])
        return f"{what} has exited {where} owned by {whom}"


HANGAR_LOCATIONS = {
    "a18": "Area 18",
    "dc": "Distro Center",
    "gh": "Grim HEX",
    "lorville": "Lorville",
    "newbab": "New Babbage",
    "orison": "Orison",
    "rest_rund": "Pyro Rest Stop",
    "rest_occu": "Rest Stop",
}


class VehicleEnterLeave(Handler):
    header = ("ENTER", Color.CYAN, False)
    pattern = re.compile(
        r"(?:\[SPAM \d+\])?\[Notice\] <CEntityComponentInstancedInterior::OnEntity(Enter|Leave)Zone> \[InstancedInterior\] OnEntity(?:Enter|Leave)Zone - InstancedInterior \[StreamingSOC_hangar_\w+_\d+_(.*?)\] \[\d{12,}\] -> Entity \[((?:SCItem_Debris_\d+_)?(?:AEGS|ANVL|ARGO|BANU|CNOU|CRUS|DRAK|ESPR|GAMA|GRIN|KRIG|MISC|MRAI|ORIG|RSI|TMBL|VNCL|XIAN|XNAA)_\w+)\] \[\d{12,}\] -- m_openDoors\[\d\], m_managerGEID\[\d{12,}\], m_ownerGEID\[([\w-]+)\]"
    )
    # isPersistent hangar persistence?

    def __init__(self, state) -> None:
        super().__init__(state)
        self.prev: tuple[str | None, str | None, datetime.datetime] | None = None

    def format(self, data):
        is_enter = data[1] == "Enter"

        where = HANGAR_LOCATIONS.get(data[2], data[2].title())
        where_a = "a " if data[2].startswith("r") else ""

        # Ships and ship debris
        vehicle, vehicle_type, found = get_vehicle(data[3])

        if found:
            what = (
                Color.GREEN(vehicle_type, True) if vehicle_type else ""
            ) + Color.GREEN(vehicle)
        else:
            what = Color.GREEN(data[3])

        whom = data[4] if data[4] != "unknown" else None
        if whom == self.state.player_name:
            # Enter/exits for the client player don't bounce.
            action = ("entered/spawned in" if is_enter else "despawned in/left", True)
            self.set_header_text("ENTER" if is_enter else "LEAVE", Color.CYAN, True)
            return f"{what} {Color.CYAN(*action)} {Color.GREEN(whom) + '\'s' if whom else 'a'} hangar at {where_a}{Color.YELLOW(where)}"
        else:
            # Assume spawn and despawn
            action = ("spawned" if is_enter else "despawned", True)
            self.set_header_text("ENTER" if is_enter else "LEAVE", Color.CYAN, True)

        # Ships entering or leaving a hangar will log entering and leaving multiple times. Ships spawning/despawning don't?
        # If the same player+ship enter/leaves within 2s of the previous vehicle enter leave event, don't print it.
        now = datetime.datetime.fromisoformat(self.state.curr_event_timestr)
        this = (whom, what, now, is_enter, False)
        if (
            self.prev
            and self.prev[0] == whom
            and self.prev[1] == what
            and now - self.prev[2] < datetime.timedelta(seconds=2)
        ):
            # Skip event if already printed
            if self.prev[4]:
                return
            # Use the first event's action
            self.prev = (this[0], this[1], this[2], self.prev[3], True)
            action = ("entered" if self.prev[3] else "left", False)
            self.set_header_text("ENTER" if self.prev[3] else "LEAVE", Color.CYAN, False)
            # Overwrite the previous spawn/despawn line with the fixed enter/leave line
            print("\x1b[1A\x1b[2K", end="")
            return f"{what} {Color.CYAN(*action)} {Color.GREEN(whom) + '\'s' if whom else 'a'} hangar at {where_a}{Color.YELLOW(where)}"
        self.prev = this

        return f"{what} {Color.CYAN(*action)} in {Color.GREEN(whom) + '\'s' if whom else 'a'} hangar at {where_a}{Color.YELLOW(where)}"
