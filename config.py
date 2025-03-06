import os
from argparse import Namespace
from typing import cast

from tomlkit import TOMLDocument, document, loads, table


CONFIG_NAME = "allslain.conf.toml"


# fmt: off
def create_default_config():
    doc = document()

    main = table()
    doc.add("main", main)

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
