import argparse
from importlib.metadata import version
from platform import python_implementation, python_version
from typing import NamedTuple

from packaging.version import Version

from .colorize import Color


class GameVersion(NamedTuple):
    phase: str
    version: Version


GAME_VERSION = GameVersion("Alpha", Version("4.3.1"))


local_version = Version(version("allslain"))


class VersionCheckResult(NamedTuple):
    error: str | None
    version: Version | None = None
    url: str | None = None


class VersionCheckOk(VersionCheckResult):
    error: None
    version: Version
    url: str


class VersionCheckErr(VersionCheckResult):
    error: str
    version: None
    url: None


def get_latest_version(repo: str) -> VersionCheckResult:
    # https://github.com/psf/requests/issues/6790
    import requests

    try:
        response = requests.get(
            f"https://api.github.com/repos/Dimmadont/{repo}/releases/latest",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=15,
        )
        if response.status_code == 200:
            latest_release = response.json()
            return VersionCheckOk(
                None, Version(latest_release["tag_name"]), latest_release["html_url"]
            )
        else:
            return VersionCheckErr("No releases available")
    except (requests.RequestException, ValueError, KeyError) as e:
        return VersionCheckErr(str(e))


def check_for_updates(repo="all-slain") -> str:
    result = get_latest_version(repo)
    if isinstance(result, VersionCheckOk):
        remote_version_text = f"Latest version: {Color.CYAN(str(result.version))}"

        if result.version > local_version:
            return f"{remote_version_text}\n{Color.GREEN(f'Update available: {local_version} -> {result.version}')}\n{Color.BLUE(result.url, bold=True)}"
        return (
            f"{remote_version_text}\n{repo} is up to date ({Color.CYAN(local_version)})"
        )
    else:
        return Color.RED(f"Update check failed: {result.error}")


def get_version_text() -> str:
    return (
        f"{Color.CYAN(local_version)} on {python_implementation()} {python_version()}"
        f"\nUpdated for Star Citizen {GAME_VERSION.phase} {Color.CYAN(GAME_VERSION.version)}"
    )


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
