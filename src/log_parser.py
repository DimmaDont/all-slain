import datetime
import importlib
import re
import time
from io import TextIOWrapper
from typing import TYPE_CHECKING, cast

from .args import Args
from .handlers.branch import Branch
from .handlers.build import Build
from .state import State


if TYPE_CHECKING:
    # For PyInstaller dependency discovery. Also see `hook-log_parser.py`

    from .data_providers.dummy import Provider as Dummy
    from .data_providers.rsi import Provider as Rsi
    from .data_providers.starcitizen_api import Provider as ScApi
    from .data_providers.wks_navcom import Provider as WksNavCom


# TODO drop python3.10 and match Z
RE_TIME = re.compile(r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3})Z> (.*)")


class LogParser:
    LOG_ENCODING = "latin-1"
    LOG_NEWLINE = "\r\n"

    def __init__(self, args: Args) -> None:
        self.state = State(args)
        # Initialize with just the Branch and Build handlers
        # Handlers are added by the Build handler once game log version and build are determined
        self.state.handlers = {
            Branch.name(): Branch(self.state),
            Build.name(): Build(self.state),
        }
        if self.state.args.debug:
            self.state.count = {
                Branch.name(): 0,
                Build.name(): 0,
            }

        if args.player_lookup and (dp := args.data_provider.provider):
            self.state.data_provider = importlib.import_module(
                f"allslain.data_providers.{dp}"
            ).Provider(self.state)

        self.prev: datetime.datetime | None = None

    def follow(self, f: TextIOWrapper):
        if self.state.args.quit_on_eof:
            while line := f.readline():
                yield line.rstrip(self.LOG_NEWLINE)
        else:
            while True:
                if line := f.readline():
                    yield line.rstrip(self.LOG_NEWLINE)
                else:
                    time.sleep(1)

    def find_match(self, line: str):
        for event_type, handler in self.state.handlers.items():
            if match := handler.pattern.match(line):
                return (event_type, match)
        return (False, None)

    def process(self, line: str):
        logtime = RE_TIME.match(line)
        if not logtime:
            return

        event_type, match = self.find_match(logtime[2])
        if not event_type:
            return

        if self.state.args.replay:
            now = datetime.datetime.fromisoformat(logtime[1])
            delay = (now - (self.prev if self.prev else now)).total_seconds()
            self.prev = now
            time.sleep(
                delay
                if self.state.args.replay is True
                else min(self.state.args.replay, delay)
            )

        self.state.curr_event_timestr = logtime[1].replace("T", " ")[:-4]

        self.state.handlers[event_type](match)

        self.state.prev_event = (logtime[1], event_type, match)

        if self.state.args.debug:
            self.state.count[event_type] += 1

    def run(self):
        with open(
            cast(str, self.state.args.file),
            "r",
            encoding=self.LOG_ENCODING,
            newline=self.LOG_NEWLINE,
        ) as f:
            for line in self.follow(f):
                self.process(line)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self.state.args.debug:
            for i in self.state.count.items():
                print(f"{i[1]:>5} {i[0]}")
        return False
