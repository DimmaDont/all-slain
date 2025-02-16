import json
import os

from crypt_sindresorhus_conf import CryptSindresorhusConf

from colorize import Color


KEY = b"OjPs60LNS7LbbroAuPXDkwLRipgfH6hIFA6wvuBxkg4="


def get_log() -> str | None:
    """
    Returns: Path of the latest game log.
    """
    try:
        with open(
            f"{os.getenv('APPDATA')}\\rsilauncher\\launcher store.json", "rb"
        ) as f:
            encrypted_data = f.read()

        crypt = CryptSindresorhusConf(KEY, encrypted_data[:16])
        decrypted = crypt.decrypt(encrypted_data)
        data = json.loads(decrypted)

        available = [
            channel["id"]
            for channel in [
                game for game in data["library"]["available"] if game["id"] == "SC"
            ][0]["channels"]
        ]
        install_dirs = {
            game["channelId"]: game["installDir"]
            for game in data["library"]["settings"]
            if game["gameId"] == "SC" and game["channelId"] in available
        }

        # `installed` channels are not guaranteed to have a "installDir" key, hence `install_dirs`
        installed = {
            channel["id"]: channel
            for channel in [
                game for game in data["library"]["installed"] if game["id"] == "SC"
            ][0]["channels"]
            if channel["id"] in available
        }

        # Option is saved immediately after selection in launcher, but check modification times anyway.
        # channel_id = [i["channelId"] for i in data["library"]["defaults"] if i["gameId"] == "SC"][0]

        files = {}
        for channel in available:
            file = f"{installed[channel]['libraryFolder']}{install_dirs.get(channel)}\\{channel}\\Game.log"
            try:
                files[file] = os.path.getmtime(file)
            except OSError:
                pass
        return max(files, key=files.__getitem__)
    except (OSError, LookupError, ValueError, json.JSONDecodeError) as e:
        print(
            f"Failed to find game installation directory or log files: {Color.RED(str(e))}"
        )
    return None
