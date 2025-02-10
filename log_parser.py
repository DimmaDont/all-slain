from handlers import (
    Cet,
    Connected,
    Connecting,
    Handler,
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
from state import State


class LogParser:
    def __init__(self) -> None:
        self.state = State()

        self.handlers: dict[str, Handler] = {
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

    def find_match(self, line: str):
        for event_type, handler in self.handlers.items():
            if match := handler.pattern.match(line):
                return (event_type, match)
        return (False, None)

    def process(self, line: str):
        event_type, match = self.find_match(line)
        if not event_type:
            return

        self.handlers[event_type](match)

        self.state.is_prev_line_cet = "CET" == event_type
