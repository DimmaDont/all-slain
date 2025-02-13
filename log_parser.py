from handlers import (
    Branch,
    Cet,
    Connected,
    Connecting,
    Incap,
    Jump,
    KillP,
    KillV,
    Loaded,
    Loading,
    Quantum,
    Quit,
    QuitLobby,
    Respawn,
    Spawn,
)
from handlers.handler import Handler
from state import State


class LogParser:
    def __init__(self) -> None:
        self.state = State({})
        self.handlers: dict[str, Handler] = {
            "BRANCH": Branch(self.state),
            "CET": Cet(self.state),
            "KILLP": KillP(self.state),
            "KILLV": KillV(self.state),
            "RESPAWN": Respawn(self.state),
            "INCAP": Incap(self.state),
            "QUITLOBBY": QuitLobby(self.state),
            "SPAWN": Spawn(self.state),
            "JUMP": Jump(self.state),
            "CONNECTED": Connected(self.state),
            "CONNECTING": Connecting(self.state),
            "LOADED": Loaded(self.state),
            "LOADING": Loading(self.state),
            "QUIT": Quit(self.state),
            "QUANTUM": Quantum(self.state),
        }
        self.state.handlers = self.handlers

    def find_match(self, line: str):
        for event_type, handler in self.state.handlers.items():
            if match := handler.pattern.match(line):
                return (event_type, match)
        return (False, None)

    def process(self, line: str):
        event_type, match = self.find_match(line)
        if not event_type:
            return

        self.state.handlers[event_type](match)

        self.state.is_prev_line_cet = event_type == "CET"
