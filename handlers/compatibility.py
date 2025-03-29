from semver import Version


class CompatibleAll:
    @classmethod
    def is_compatible(cls, version: Version, build: int) -> bool:
        return True


class SinceV410:
    @classmethod
    def is_compatible(cls, version: Version, build: int) -> bool:
        return version >= Version(4, 1, 0)


class SinceV402:
    @classmethod
    def is_compatible(cls, version: Version, build: int) -> bool:
        return version >= Version(4, 0, 2)


class V402AndBelow:
    @classmethod
    def is_compatible(cls, version: Version, build: int) -> bool:
        return version <= Version(4, 0, 2)


class V401AndBelow:
    @classmethod
    def is_compatible(cls, version: Version, build: int) -> bool:
        return version <= Version(4, 0, 1)


class OnlyV400:
    @classmethod
    def is_compatible(cls, version: Version, build: int) -> bool:
        return version == Version(4, 0, 0)


class SinceV324:
    @classmethod
    def is_compatible(cls, version: Version, build: int) -> bool:
        return version >= Version(3, 24, 0)
