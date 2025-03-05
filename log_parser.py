import datetime
import time
from argparse import Namespace

from handlers.branch import Branch
from state import State


class LogParser:
    def __init__(self, args: Namespace) -> None:
        self.state = State(args)
        # Initialize with just the Branch handler
        # Handlers are added when the game log version is determined
        self.state.handlers = {Branch.name(): Branch(self.state)}

        self.prev: datetime.datetime | None = None

    def find_match(self, line: str):
        for event_type, handler in self.state.handlers.items():
            if match := handler.pattern.match(line):
                return (event_type, match)
        return (False, None)

    def process(self, line: str):
        event_type, match = self.find_match(line)
        if not event_type:
            return

        if self.state.args.replay:
            now = datetime.datetime.fromisoformat(match[1])
            delay = (now - (self.prev if self.prev else now)).total_seconds()
            self.prev = now
            time.sleep(
                delay
                if self.state.args.replay is True
                else min(self.state.args.replay, delay)
            )

        self.state.handlers[event_type](match)

        self.state.prev_event = (event_type, match)

        if self.state.args.debug:
            self.state.count[event_type] += 1

    def quit(self):
        if self.state.args.debug:
            for i in sorted(self.state.count.items(), key=lambda item: item[1]):
                print(f"{i[1]:>3} {i[0]}")
