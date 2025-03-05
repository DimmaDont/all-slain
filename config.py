import os
from argparse import Namespace

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

    def write(self, data: TOMLDocument) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            f.write(data.as_string())


def mergeattr(src: dict, dest: object):
    for key, value in src.items():
        if isinstance(value, dict):
            if not hasattr(dest, key):
                setattr(dest, key, Namespace())
            node = getattr(dest, key)
            mergeattr(value, node)
        else:
            setattr(dest, key, value)


def load_config(namespace: Namespace | None = None) -> Namespace:
    # Load defaults and config file
    config = create_default_config()
    if os.path.exists(CONFIG_NAME):
        _config = TOMLFile(CONFIG_NAME).read()
        # Do not use dict.update or |= here
        merge(_config, config)
    else:
        _config = document()

    # Write back if contents differ
    if config.as_string() != _config.as_string():
        TOMLFile(CONFIG_NAME).write(config)

    if not namespace:
        namespace = Namespace()
    mergeattr(config.pop("main"), namespace)
    mergeattr(config, namespace)
    return namespace
