import json
import logging
import os
import time
from argparse import ArgumentParser
from collections.abc import Generator
from io import TextIOWrapper
from typing import Any

from crypt_sindresorhus_conf import CryptSindresorhusConf

from colorize import Color
from log_parser import LogParser
from version import UpdateCheck, __version__


class AllSlain:
    LOG_ENCODING = "latin-1"
    LOG_NEWLINE = "\r\n"

    @classmethod
    def get_log(cls) -> str | None:
        """
        Returns: Path of the latest game log.
        """
        try:
            with open(
                f"{os.getenv('APPDATA')}\\rsilauncher\\launcher store.json", "rb"
            ) as f:
                encrypted_data = f.read()

            crypt = CryptSindresorhusConf(
                b"OjPs60LNS7LbbroAuPXDkwLRipgfH6hIFA6wvuBxkg4=", encrypted_data[:16]
            )
            decrypted = crypt.decrypt(encrypted_data)
            data = json.loads(decrypted)

            install_dirs = {
                game["channelId"]: game["installDir"]
                for game in data["library"]["settings"]
                if game["gameId"] == "SC"
            }
            sc = [game for game in data["library"]["installed"] if game["id"] == "SC"][0]  # fmt: skip

            # Option is saved immediately after selection in launcher, but check modification times anyway.
            # channel_id = [i["channelId"] for i in data["library"]["defaults"] if i["gameId"] == "SC"][0]

            files = {}
            for channel in sc["channels"]:
                file = f"{channel['libraryFolder']}{install_dirs.get(channel['id'])}\\{channel['id']}\\Game.log"
                try:
                    files[file] = os.path.getmtime(file)
                except OSError:
                    pass
            return max(files, key=files.__getitem__)
        except (OSError, LookupError, ValueError, json.JSONDecodeError) as e:
            print(
                f"Failed to find game installation directory or log files: {Color.RED(str(e))}"
            )
        return None

    def follow(self, f: TextIOWrapper) -> Generator[str, Any, None]:
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
        parser = ArgumentParser()
        parser.add_argument("file", nargs="?")
        parser.add_argument("-d", "--debug", action="store_true")
        parser.add_argument(
            "-r",
            "--replay",
            action="store_true",
            help="replays the log as if running live",
        )
        parser.add_argument(
            "-q",
            "--quit-on-eof",
            action="store_true",
            help="quit when end of log is reached",
        )
        parser.add_argument(
            "-u",
            "--check-for-updates",
            action=UpdateCheck,
            help="check for updates and exit",
        )
        parser.add_argument("-v", "--verbose", action="count")
        parser.add_argument("--version", action="version", version=__version__)
        self.args = parser.parse_args()

        if self.args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
            self.args.verbose = 1

    def run(self) -> None:
        # Set window title and cursor shape
        print("\x1b]0;all-slain\x07\x1b[2\x20q", end="")
        print(f"{Color.WHITE('all-slain', bold=True)}: Star Citizen Game Log Reader")
        print(f"{Color.BLUE('https://github.com/DimmaDont/all-slain', bold=True)}\n")

        if filename := self.args.file if self.args.file else self.get_log():
            print(f'Reading "{Color.CYAN(filename)}"\n')
        else:
            print(Color.RED("No log files found."))
            print(
                "Run this again after starting the game, or specify a game log to read."
            )
            return

        log_parser = LogParser(self.args)
        try:
            with open(
                filename, "r", encoding=self.LOG_ENCODING, newline=self.LOG_NEWLINE
            ) as f:
                for line in self.follow(f):
                    log_parser.process(line)
        except KeyboardInterrupt:
            pass
        except FileNotFoundError:
            print(Color.RED(f'Log file "{filename}" not found.'))
        except OSError as e:
            print(Color.RED(f'Failed to read "{filename}": {str(e)}'))


def main():
    AllSlain().run()


if __name__ == "__main__":
    main()


# vim: set expandtab ts=4 sw=4
