import re

from colorize import Color
from functions import get_location
from functions_color import color_location, color_player_default
from handlers.compatibility import OnlyV400, V401AndBelow

from .handler import Handler


class ClientQuantum(OnlyV400, Handler):
    header = ("QUANTUM", Color.BLACK, True)
    pattern = re.compile(
        r"\[Notice\] <Quantum Navtarget> CSCItemQuantumDrive::RmMulticastOnQTToPoint : Local client user ([\w-]*)\[\d{12,}\] received QT data for Entity:\w+_\d{12,}\[\d{12,}\] to Target (\w+)"
    )

    def format(self, data) -> str:
        name = color_player_default(data[1])
        dest = color_location(*get_location(data[2])[1:])
        return f"{name} started quantum travel to {dest}"


class Quantum(V401AndBelow, Handler):
    header = ("QUANTUM", Color.BLACK, True)
    pattern = re.compile(r"-- Entity Trying To QT: (.*)")

    def format(self, data) -> str:
        name = color_player_default(data[1])
        return f"{name} started quantum travel"
