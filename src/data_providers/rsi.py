import re

import requests
from bs4 import BeautifulSoup

from .provider import BaseProvider, Org, Player, Theme


ORG_THEME = re.compile(r'\s*<body id="organization-page" class="([a-z]{4,7})"')


class Provider(BaseProvider):
    def _lookup_player(self, handle: str) -> Player:
        player = Player(handle)
        try:
            response = requests.get(
                f"https://robertsspaceindustries.com/citizens/{handle}",
                timeout=15,
            )
            soup = BeautifulSoup(response.text, "html.parser")
            for entry in soup.find_all("p", class_="entry"):
                text = entry.get_text().strip().split("\n")
                match text[0]:
                    # case "UEE Citizen Record":
                    #     player["ucr"] = text[1].lstrip("#")
                    case "Spectrum Identification (SID)":
                        player.main_org = text[1]
                        break
                    # case "Bio":
                    #     player.bio = text[1:]
        except requests.RequestException:
            pass
        return player

    def _lookup_org(self, spectrum_id: str) -> Org:
        org = Org(sid=spectrum_id)
        try:
            response = requests.get(
                f"https://robertsspaceindustries.com/orgs/{spectrum_id}",
                timeout=15,
            ).text.splitlines()
            for line in response:
                if match := ORG_THEME.match(line):
                    org.theme = Theme[match[1].upper()]
                    break
        except (requests.RequestException, KeyError):
            pass
        return org
