import re
from typing import cast

from semver import Version

from ..colorize import Color
from .build import Build
from .compatibility import CompatibleAll
from .handler import Handler


RE_SC_VERSION = re.compile(r"sc-alpha-(\d\.\d+(?:\.\d+)?(?:-\w+)?)(\w+)?")


class UnsupportedVersionException(Exception):
    pass


class Branch(CompatibleAll, Handler):
    header = ("BRANCH", Color.WHITE, False)
    pattern = re.compile(r"Branch: (.+)")

    def format(self, data) -> None:
        pass

    def after(self, data) -> None:
        match = RE_SC_VERSION.match(data[1])
        if match is None:
            raise UnsupportedVersionException(data[1])

        self.state.version = Version.parse(match[1], True)
        if match[2] is not None:
            # "a" to "a.1"
            self.state.version.bump_prerelease(match[2])

        # For printing by Build
        build = cast(Build, self.state.handlers[Build.name()])
        build.branch = data[1]

        if self.state.version >= Version(4, 0, 2):
            # 4.0.2 added a ReadyToReplicate step
            self.state.cet_steps = 16
        else:
            # 4.0.1 and below
            self.state.cet_steps = 15

        # Remove from handlers after use -- appears only once per log file
        del self.state.handlers[self.name()]
