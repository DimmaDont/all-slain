import re

from colorize import Color
from functions import clean_location

from .handler import Handler


class ClientQuantum(Handler):
    header = ("QUANTUM", Color.BLACK, True)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Quantum Navtarget> CSCItemQuantumDrive::RmMulticastOnQTToPoint : Local client user ([\w-]*)\[\d{12,}\] received QT data for Entity:\w+_\d{12,}\[\d{12,}\] to Target (\w+).*"
    )

    def format(self, data) -> str:
        name = Color.GREEN(data[2])
        dest = Color.YELLOW(clean_location(data[3])[1])
        return f"{name} started quantum travel to {dest}"


class Quantum(Handler):
    header = ("QUANTUM", Color.BLACK, True)
    pattern = re.compile(
        r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> -- Entity Trying To QT: (.*)"
    )

    def format(self, data) -> str:
        name = Color.GREEN(data[2])
        return f"{name} started quantum travel"
