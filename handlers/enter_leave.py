import re

from colorize import Color
from functions import get_vehicle

from .handler import Handler


class Enter(Handler):
    header = ("LEAVE", Color.GREEN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <CEntityComponentInstancedInterior::OnEntityEnterZone> \[InstancedInterior\] OnEntityEnterZone - InstancedInterior \[(.*)\] \[\d{12,}\] -> Entity \[(\w+)\] \[\d{12,}\] -- m_openDoors\[\d\], m_managerGEID\[\d{12,}\], m_ownerGEID\[([\w-]+)\]\[\d{12,}\], m_isPersistent\[\d\] .*"
    )

    def format(self, data) -> str:
        where = Color.CYAN("a hangar" if "_hangar_" in data[2] else data[2])
        what = (
            Color.BLACK("Elevator", True)
            if "_elev_" in data[3]
            else Color.GREEN(get_vehicle(data[3])[0])
        )
        whom = Color.GREEN(data[4])
        return f"{what} has entered {where} owned by {whom}"


class Leave(Handler):
    header = ("LEAVE", Color.GREEN, False)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <CEntityComponentInstancedInterior::OnEntityLeaveZone> \[InstancedInterior\] OnEntityLeaveZone - InstancedInterior \[(.*)\] \[\d{12,}\] -> Entity \[(\w+)\] \[\d{12,}\] -- m_openDoors\[\d\], m_managerGEID\[\d{12,}\], m_ownerGEID\[([\w-]+)\]\[\d{12,}\], m_isPersistent\[\d\] .*"
    )

    def format(self, data) -> str:
        where = Color.CYAN("a hangar" if "_hangar_" in data[2] else data[2])
        what = (
            Color.BLACK("Elevator", True)
            if "_elev_" in data[3]
            else Color.GREEN(get_vehicle(data[3])[0])
        )
        whom = Color.GREEN(data[4])
        return f"{what} has exited {where} owned by {whom}"
