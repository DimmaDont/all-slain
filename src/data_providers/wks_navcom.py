import requests

from .provider import BaseProvider, Org, Player


class Provider(BaseProvider):
    def _lookup_player(self, handle: str) -> Player:
        player = Player(handle)
        try:
            memberships = requests.get(
                f"https://sentry.wildknightsquadron.com/api/v1/citizens/{handle}/memberships",
                headers={"Accept": "application/json"},
                timeout=15,
            ).json()
        except requests.RequestException:
            return player

        main_org = next((m for m in memberships if m["is_main"]), None)

        return Player(
            # ucr=response["profile"]["citizen_record"].lstrip("#"),
            handle=handle,
            main_org=main_org["organization_sid"] if main_org else None,
        )

    def _lookup_org(self, spectrum_id: str) -> Org:
        # API does not provide page theme
        return Org(spectrum_id)
