import os
from argparse import Namespace
from typing import cast

from tomlkit import TOMLDocument, comment, document, loads, nl, table

from data_providers.starcitizen_api import Mode


CONFIG_NAME = "allslain.conf.toml"


class StarCitizenApi(Namespace):
    api_key: str
    mode: Mode


class DataProvider(Namespace):
    provider: str
    use_org_theme: bool

    starcitizen_api: StarCitizenApi


class Config(Namespace):
    player_lookup: bool
    data_provider: DataProvider


# fmt: off
def create_default_config():
    doc = document()

    main = table()
    main.add(nl())
    main.add(comment("Whether to perform player org lookups. If set to true, select a data provider below."))
    main.add(comment('Default: false'))
    main.add("player_lookup", False)
    doc.add("main", main)

    data_provider = table()
    data_provider.add(comment("Available data providers:"))
    data_provider.add(comment("rsi:"))
    data_provider.add(comment("    https://robertsspaceindustries.com/"))
    data_provider.add(comment("starcitizen_api:"))
    data_provider.add(comment("    Unofficial Star Citizen API. Requires an API key!"))
    data_provider.add(comment("    https://starcitizen-api.com/"))
    data_provider.add(comment("wks_navcom:"))
    data_provider.add(comment("    Wild Knight Squadron's NAVCOM API."))
    data_provider.add(comment("    https://sentry.wildknightsquadron.com"))
    data_provider.add(comment('Default: ""'))
    data_provider.add("provider", "")
    data_provider.add(nl())
    data_provider.add(comment("Whether to pull and display the org's Spectrum theme color when displaying an org."))
    data_provider.add(comment('Currently only available with the "rsi" data provider.'))
    data_provider.add(comment('Default: true'))
    data_provider.add("use_org_theme", True)
    data_provider.add(nl())

    starcitizen_api = table()
    starcitizen_api.add(comment('Default: ""'))
    starcitizen_api.add("api_key", "")
    starcitizen_api.add(nl())
    starcitizen_api.add(comment("One of: live, cache, auto, eager"))
    starcitizen_api.add(comment('Default: "auto"'))
    starcitizen_api.add("mode", "auto")

    data_provider.add("starcitizen_api", starcitizen_api)

    doc.add("data_provider", data_provider)

    return doc
# fmt: on


def merge(src: dict, dest: dict):
    for key, value in src.items():
        if isinstance(value, dict):
            node = dest.setdefault(key, {})
            merge(value, node)
        else:
            dest[key] = value


# See https://github.com/python-poetry/tomlkit/pull/402
class TOMLFile:
    def __init__(self, path: str | os.PathLike) -> None:
        self._path = path

    def read(self) -> TOMLDocument:
        with open(self._path, encoding="utf-8") as f:
            return loads(f.read())

    def write_if_modified(self, data: TOMLDocument, compare: TOMLDocument) -> None:
        if (config := data.as_string()) != compare.as_string():
            with open(self._path, "w", encoding="utf-8") as f:
                f.write(config)


def mergeattr(src: dict, dest: object):
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
