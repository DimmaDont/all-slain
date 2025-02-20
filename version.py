import argparse
from importlib import import_module
from platform import python_version
from typing import TYPE_CHECKING

from semver import Version

from colorize import Color


__version__ = "VERSION_HERE"


def check_for_updates() -> str:
    try:
        local_version = Version.parse(__version__)
    except ValueError:
        return "Not available in development releases, sorry."

    # https://github.com/psf/requests/issues/6790
    if TYPE_CHECKING:
        import requests  # pylint: disable=C0415
    else:
        requests = import_module("requests")
    try:
        latest_release = requests.get(
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
        remote_version_text = f"Latest version: {Color.CYAN(str(remote_version))}"

        if remote_version > local_version:
            return f"{remote_version_text}\n{Color.GREEN(f'Update available: {local_version} -> {remote_version}')}\n{Color.BLUE(latest_release['html_url'], bold=True)}"
        return f"{remote_version_text}\nall-slain is up to date ({get_version_text()})"
    except (requests.RequestException, ValueError) as e:
        return Color.RED(f"Update check failed: {str(e)}")


def get_version_text() -> str:
    return f"{Color.CYAN(__version__)} on Python {python_version()}"


class UpdateCheckAction(argparse.Action):
    def __init__(
        self, option_strings, dest, help="check for updates and exit"
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
