import argparse

from requests import get
from semver import Version

from colorize import Color


__version__ = "VERSION_HERE"


def check_for_updates() -> str:
    try:
        local_version = Version.parse(__version__)
    except ValueError:
        return "Not supported in dev releases, sorry."

    try:
        latest_release = get(
            "https://api.github.com/repos/Dimmadont/all-slain/releases/latest",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=15,
        ).json()
        if not latest_release:
            return Color.RED("No releases found.")

        remote_version = Version.parse(latest_release["tag_name"])

        if remote_version > local_version:
            return f"{Color.GREEN(f'Update available: {__version__} -> {remote_version}')}\n{Color.BLUE(latest_release['html_url'], bold=True)}"

        return Color.CYAN(
            f"Latest version: {remote_version}\nall-slain is up to date ({__version__})"
        )
    except ValueError:
        return Color.RED("Update check failed.")


class UpdateCheck(argparse.Action):
    def __init__(
        self, option_strings, dest, help=None
    ):  # pylint: disable=redefined-builtin
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            help=help,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, True)
        parser._print_message(check_for_updates())
        parser.exit()
