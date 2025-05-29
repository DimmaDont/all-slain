import os
import sys
from difflib import unified_diff

from crypt_sindresorhus_conf import CryptSindresorhusConf


KEY = b"OjPs60LNS7LbbroAuPXDkwLRipgfH6hIFA6wvuBxkg4="


def decrypt(path: str):
    with open(path, "rb") as f:
        encrypted_data = f.read()
    return (
        CryptSindresorhusConf(KEY, encrypted_data[:16])
        .decrypt(encrypted_data)
        .decode()
        .splitlines(True)
    )


def main():
    sys.stdout.writelines(
        unified_diff(
            decrypt(Rf"{os.getenv('APPDATA')}\rsilauncher\launcher store old.json"),
            decrypt(Rf"{os.getenv('APPDATA')}\rsilauncher\launcher store.json"),
            "launcher store old.json",
            "launcher store.json",
        )
    )


if __name__ == "__main__":
    main()
