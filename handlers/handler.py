import re
from abc import ABC, abstractmethod

from colorize import Color
from state import State


class Handler(ABC):
    header: tuple[str, Color, bool]
    pattern: re.Pattern

    def __init__(self, state: State):
        self.state = state
        self.header_text = self.header[1](
            self.header[0].rjust(self.state.header_width), bold=self.header[2]
        )

    def __call__(self, log: re.Match[str]) -> None:
        when = log[1].replace("T", " ")
        print(f"{when}{self.header_text}: {self.format(log)}")

    @abstractmethod
    def format(self, log: re.Match) -> str: ...
