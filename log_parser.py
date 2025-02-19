import datetime
import logging
import time
from argparse import Namespace

from handlers import DEFAULT as HANDLERS
from handlers.handler import Handler
from state import State


class LogParser:
    def __init__(self, args: Namespace | None = None) -> None:
        self.state = State(args) if args else State()
        self.handlers: dict[str, Handler] = {
            handler.name(): handler(self.state) for handler in HANDLERS
        }
        self.state.handlers = self.handlers
        self.state.count = {p[0]: 0 for p in self.handlers.items()}

        self.delay: float = 0
        self.now: datetime.datetime | None = None
        self.prev: datetime.datetime | None = None

    def find_match(self, line: str):
        for event_type, handler in self.state.handlers.items():
            if match := handler.pattern.match(line):
                self.state.count[event_type] += 1
                return (event_type, match)
        return (False, None)

    def process(self, line: str):
        event_type, match = self.find_match(line)
        if not event_type:
            return

        if self.state.args.replay:
            self.now = datetime.datetime.fromisoformat(match[1])
            self.delay = (
                self.now - (self.prev if self.prev else self.now)
            ).total_seconds()
            logging.debug("%s %s pausing for %f", self.prev, self.now, self.delay)
            self.prev = self.now
            time.sleep(
                self.delay
                if self.state.args.replay is True
                else min(self.state.args.replay, self.delay)
            )

        self.state.handlers[event_type](match)

        self.state.prev_event = (event_type, match)
