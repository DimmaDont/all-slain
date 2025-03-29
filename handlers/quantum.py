import re

from colorize import Color
from functions import clean_location
from handlers.compatibility import OnlyV400, V401AndBelow

from .handler import Handler


class ClientQuantum(OnlyV400, Handler):
    header = ("QUANTUM", Color.BLACK, True)
    pattern = re.compile(
        r"\[Notice\] <Quantum Navtarget> CSCItemQuantumDrive::RmMulticastOnQTToPoint : Local client user ([\w-]*)\[\d{12,}\] received QT data for Entity:\w+_\d{12,}\[\d{12,}\] to Target (\w+)"
    )

    def format(self, data) -> str:
        name = Color.GREEN(data[1])
        dest = Color.YELLOW(clean_location(data[2])[1])
        return f"{name} started quantum travel to {dest}"


class Quantum(V401AndBelow, Handler):
    header = ("QUANTUM", Color.BLACK, True)
    pattern = re.compile(r"-- Entity Trying To QT: (.*)")

    def format(self, data) -> str:
        name = Color.GREEN(data[1])
        return f"{name} started quantum travel"
