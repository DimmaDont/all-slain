import json
import os
import traceback

from crypt_sindresorhus_conf import CryptSindresorhusConf

from colorize import Color


KEY = b"OjPs60LNS7LbbroAuPXDkwLRipgfH6hIFA6wvuBxkg4="


def read_launcher_store():
    try:
        with open(
            f"{os.getenv('APPDATA')}\\rsilauncher\\launcher store.json", "rb"
        ) as f:
            encrypted_data = f.read()

        crypt = CryptSindresorhusConf(KEY, encrypted_data[:16])
        decrypted = crypt.decrypt(encrypted_data)
        return json.loads(decrypted)
    except (OSError, json.JSONDecodeError):
        print(Color.RED("Failed to find game installation directory:"))
        print(traceback.format_exc())
        return None


def get_log() -> str | None:
    """
    Returns: Path of the latest game log.
    """
    try:
        data = read_launcher_store()
        if not data:
            return None

        library_available = data["library"]["available"]
        if not library_available:
            return None

        available_sc = [game for game in library_available if game["id"] == "SC"][0]
        available = [channel["id"] for channel in available_sc.get("channels", [])]

        install_dirs = {
            game["channelId"]: game.get("installDir")
            for game in data["library"]["settings"]
            if game["gameId"] == "SC" and game["channelId"] in available
        }

        library = data["library"]["installed"]
        if not library:
            # You don't have any games on your phone!
            return None

        # `installed` channel dicts are not guaranteed to have an "installDir" key, hence `install_dirs`
        installed_sc = [game for game in library if game["id"] == "SC"][0]
        installed = {
            channel["id"]: channel
            for channel in installed_sc.get("channels", [])
            if channel["id"] in available
        }

        # Option is saved immediately after selection in launcher, but check modification times anyway.
        # channel_id = [i["channelId"] for i in data["library"]["defaults"] if i["gameId"] == "SC"][0]

        files = {}
        for channel_id in available:
            # Just because it's available doesn't mean it's installed
            installed_channel = installed.get(channel_id)
            if not installed_channel:
                continue

            library_folder = installed_channel.get("libraryFolder")
            if not library_folder:
                continue
            install_folder = installed_channel.get("installDir") or install_dirs.get(channel_id)  # fmt: skip
            if not install_folder:
                continue
            file = f"{library_folder}{install_folder}\\{channel_id}\\Game.log"
            try:
                files[file] = os.path.getmtime(file)
            except OSError:
                pass
        return max(files, key=files.__getitem__) if files else None
    except (LookupError, ValueError):
        print(Color.RED("Failed to find log files:"))
        print(traceback.format_exc())
    return None
