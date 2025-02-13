from abc import ABC, abstractmethod
from re import Match, Pattern

from colorize import Color
from state import State


class Handler(ABC):
    header: tuple[str, Color, bool]
    pattern: Pattern

    def __init__(self, state: State):
        self.state = state
        self.header_text = self.header[1](
            self.header[0].rjust(self.state.header_width), bold=self.header[2]
        )

    def __call__(self, data: Match[str]) -> None:
        when = data[1].replace("T", " ")
        print(f"{when}{self.header_text}: {self.format(data)}")

    @abstractmethod
    def format(self, data: Match[str]) -> str: ...
