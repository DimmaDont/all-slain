import json
import logging
import os


logger = logging.getLogger("allslain").getChild("launcher_store")


KEY = b"OjPs60LNS7LbbroAuPXDkwLRipgfH6hIFA6wvuBxkg4="


class LauncherStoreException(Exception):
    pass


def read_launcher_store():
    from crypt_sindresorhus_conf import CryptSindresorhusConf

    try:
        with open(
            Rf"{os.getenv('APPDATA')}\rsilauncher\launcher store.json", "rb"
        ) as f:
            encrypted_data = f.read()

        crypt = CryptSindresorhusConf(KEY, encrypted_data[:16])
        decrypted = crypt.decrypt(encrypted_data)
        return json.loads(decrypted)
    except OSError:
        raise LauncherStoreException("Failed to find launcher store") from None
    except json.JSONDecodeError:
        raise LauncherStoreException("Failed to read launcher store") from None


def get_log() -> str | None:
    """
    Returns: Path of the latest game log.

    Raises: :exc:`LauncherStoreException`
    """
    try:
        data = read_launcher_store()
        if not data:
            return None

        library_available = data["library"]["available"]
        if not library_available:
            logger.debug("Nothing available")
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
            logger.debug("Nothing installed")
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

        files: dict[str, float] = {}
        for channel_id in available:
            logger.debug("Available: %s", channel_id)
            # Just because it's available doesn't mean it's installed
            installed_channel = installed.get(channel_id)
            if not installed_channel:
                continue
            logger.debug("Installed: %s", channel_id)

            library_folder = installed_channel.get("libraryFolder")
            if not library_folder:
                logger.debug("No library folder: %s", channel_id)
                continue
            install_folder = installed_channel.get("installDir") or install_dirs.get(channel_id)  # fmt: skip
            if not install_folder:
                logger.debug("No install folder: %s", channel_id)
                continue
            file = f"{library_folder}{install_folder}\\{channel_id}\\Game.log"
            try:
                files[file] = os.path.getmtime(file)
            except OSError as e:
                logger.debug("%s %s %s", channel_id, file, str(e))

        return max(files, key=files.__getitem__) if files else None
    except (LookupError, ValueError) as e:
        raise LauncherStoreException(
            "Failed to find game installation directories"
        ) from e
