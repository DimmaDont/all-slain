import os
from argparse import Namespace
from typing import Any, cast

from tomlkit import (
    TOMLDocument,
    comment,
    document,
    loads,
    nl,
    register_encoder,
    string,
    table,
)
from tomlkit.exceptions import ConvertError
from tomlkit.items import Item

from data_providers.starcitizen_api import Mode


CONFIG_NAME = "allslain.conf.toml"


# TODO drop python3.10 and use StrEnum
def mode_encoder(e: Any) -> Item:
    if isinstance(e, Mode):
        return string(e.value)
    raise ConvertError()


register_encoder(mode_encoder)


class StarCitizenApi(Namespace):
    api_key: str = ""
    mode: Mode = Mode.AUTO


class DataProvider(Namespace):
    provider: str = ""
    use_org_theme: bool = True

    starcitizen_api: StarCitizenApi = StarCitizenApi()


class Config(Namespace):
    player_lookup: bool = False
    planespotting: bool = False

    data_provider: DataProvider = DataProvider()


# fmt: off
def create_default_config() -> TOMLDocument:
    doc = document()

    main = table()

    main.add(comment("Whether to perform player org lookups. If set to true, select a data provider below."))
    main.add(comment("Default: false"))
    main.add("player_lookup", Config.player_lookup)
    main.add(nl())

    main.add(comment("Whether to display vehicles spawning/entering and despawning/leaving hangars."))
    main.add(comment("Not 100% accurate -- ship spawning is buggy."))
    main.add(comment("Unavailable after Alpha 4.0.2, starting with Alpha 4.1.0"))
    main.add(comment("Default: false"))
    main.add("planespotting", Config.planespotting)
    main.add(nl())

    doc.add("main", main)

    data_provider = table()
    data_provider.add(comment("Available data providers:"))
    data_provider.add(comment('"rsi":'))
    data_provider.add(comment("    https://robertsspaceindustries.com/"))
    data_provider.add(comment('"starcitizen_api":'))
    data_provider.add(comment("    Unofficial Star Citizen API. Requires an API key!"))
    data_provider.add(comment("    https://starcitizen-api.com/"))
    data_provider.add(comment('"wks_navcom":'))
    data_provider.add(comment("    Wild Knight Squadron's NAVCOM API."))
    data_provider.add(comment("    https://sentry.wildknightsquadron.com"))
    data_provider.add(comment('Default: ""'))
    data_provider.add("provider", Config.data_provider.provider)
    data_provider.add(nl())
    data_provider.add(comment("Whether to pull and display the org's Spectrum theme color when displaying an org."))
    data_provider.add(comment('Currently only available with the "rsi" data provider.'))
    data_provider.add(comment("Default: true"))
    data_provider.add("use_org_theme", Config.data_provider.use_org_theme)

    starcitizen_api = table()
    starcitizen_api.add(comment('Default: ""'))
    starcitizen_api.add("api_key", Config.data_provider.starcitizen_api.api_key)
    starcitizen_api.add(nl())
    starcitizen_api.add(comment("One of: live, cache, auto, eager"))
    starcitizen_api.add(comment('Default: "auto"'))
    starcitizen_api.add("mode", Config.data_provider.starcitizen_api.mode)

    data_provider.add("starcitizen_api", starcitizen_api)

    doc.add("data_provider", data_provider)

    return doc
# fmt: on


def merge(src: dict[str, Any], dest: dict[Any, Any]) -> None:
    for key, value in src.items():
        if isinstance(value, dict):
            node = dest.setdefault(key, {})
            merge(value, node)
        else:
            dest[key] = value


# See https://github.com/python-poetry/tomlkit/pull/402
class TOMLFile:
    def __init__(self, path: str | os.PathLike[str]) -> None:
        self._path = path

    def read(self) -> TOMLDocument:
        with open(self._path, encoding="utf-8") as f:
            return loads(f.read())

    def write_if_modified(self, data: TOMLDocument, compare: TOMLDocument) -> None:
        if (config := data.as_string()) != compare.as_string():
            with open(self._path, "w", encoding="utf-8") as f:
                f.write(config)


def mergeattr(src: dict[str, Any], dest: object) -> None:
    for key, value in src.items():
        if isinstance(value, dict):
            if not hasattr(dest, key):
                setattr(dest, key, Namespace())
            node = getattr(dest, key)
            mergeattr(value, node)
        else:
            setattr(dest, key, value)


def load_config(namespace: Namespace | None = None) -> Config:
    # Load defaults and config file
    config = create_default_config()
    if os.path.exists(CONFIG_NAME):
        _config = TOMLFile(CONFIG_NAME).read()
        # Do not use dict.update or |= here
        merge(_config, config)
    else:
        _config = document()

    TOMLFile(CONFIG_NAME).write_if_modified(config, _config)

    if not namespace:
        namespace = Config()
    mergeattr(config.pop("main"), namespace)
    mergeattr(config, namespace)

    return cast(Config, namespace)
