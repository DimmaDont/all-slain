import logging
import time
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from io import TextIOWrapper

from args import Args
from colorize import Color
from config import load_config
from launcher_store import LauncherStoreException, get_log
from log_parser import LogParser
from version import UpdateCheckAction, __version__, get_version_text


logging.basicConfig(format=logging.BASIC_FORMAT)
logger = logging.getLogger("allslain")


class AllSlain:
    LOG_ENCODING = "latin-1"
    LOG_NEWLINE = "\r\n"

    def follow(self, f: TextIOWrapper):
        if self.args.quit_on_eof:
            while line := f.readline():
                yield line.rstrip(self.LOG_NEWLINE)
        else:
            while True:
                if line := f.readline():
                    yield line.rstrip(self.LOG_NEWLINE)
                else:
                    time.sleep(1)

    def __init__(self):
        parser = ArgumentParser(
            formatter_class=RawDescriptionHelpFormatter,
            description=(
                "all-slain: Star Citizen Game Log Reader\n"
                + Color.BLUE("https://github.com/DimmaDont/all-slain", bold=True)
            ),
        )
        parser.add_argument("file", nargs="?")
        parser.add_argument("-d", "--debug", action="store_true")
        parser.add_argument(
            "-q",
            "--quit-on-eof",
            action="store_true",
            help="quit when end of log is reached",
        )
        parser.add_argument(
            "-r",
            "--replay",
            const=True,
            default=False,
            type=int,
            nargs="?",
            help="replays the log as if running live. optionally, specify the maximum number of seconds to wait between each line",
        )
        parser.register("action", "update_check", UpdateCheckAction)
        parser.add_argument("-u", "--update", action="update_check")
        parser.add_argument("-v", "--verbose", action="count", default=0)
        parser.add_argument("--version", action="version", version=get_version_text())
        self.args: Args = parser.parse_args(namespace=load_config())

        if self.args.debug:
            logger.setLevel(logging.DEBUG)
            self.args.verbose = self.args.verbose or 1

    def run(self) -> None:
        # Set window title and cursor shape
        print("\x1b]0;all-slain\x07\x1b[2\x20q", end="", flush=True)

        if self.args.file:
            if self.args.verbose:
                print(f'Reading "{Color.CYAN(self.args.file)}"\n')
        else:
            try:
                self.args.file = get_log()
            except LauncherStoreException as e:
                print(Color.RED(str(e)))

            if not self.args.file:
                print(Color.RED("No log files found."))
                print(
                    "Run this again after starting the game, or specify a game log to read."
                )
                return

        log_parser = LogParser(self.args)
        try:
            with open(
                self.args.file,
                "r",
                encoding=self.LOG_ENCODING,
                newline=self.LOG_NEWLINE,
            ) as f:
                for line in self.follow(f):
                    log_parser.process(line)
        except KeyboardInterrupt:
            pass
        except FileNotFoundError:
            print(Color.RED(f'Log file "{self.args.file}" not found.'))
        except OSError as e:
            print(Color.RED(f'Failed to read "{self.args.file}": {str(e)}'))
        log_parser.quit()


def main():
    AllSlain().run()


if __name__ == "__main__":
    main()


# vim: set expandtab ts=4 sw=4
