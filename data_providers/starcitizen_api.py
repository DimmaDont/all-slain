from enum import Enum

import requests

from .provider import BaseProvider, Org, Player


class Mode(Enum):
    LIVE = "live"
    CACHE = "cache"
    AUTO = "auto"
    EAGER = "eager"


class Provider(BaseProvider):
    def __init__(self, state) -> None:
        super().__init__(state)

        self.api_key = self.state.args.data_provider.starcitizen_api.api_key
        if not self.api_key:
            raise ValueError("API key missing")

        self.mode = self.state.args.data_provider.starcitizen_api.mode

    def _lookup_player(self, handle: str) -> Player:
        try:
            response = requests.get(
                f"https://api.starcitizen-api.com/{self.api_key}/v1/{self.mode.value}/user/{handle}",
                headers={"Accept": "application/json"},
                timeout=15,
            ).json()
        except requests.RequestException:
            response = {"success": 0}

        if response["success"] != 1:
            return Player(handle)

        return Player(
            handle=handle,
            main_org=response["data"]["organization"]["sid"],
            # ucr=response["data"]["profile"]["id"].lstrip("#"),
        )

    def _lookup_org(self, spectrum_id: str) -> Org:
        # API does not provide page theme
        return Org(spectrum_id)
