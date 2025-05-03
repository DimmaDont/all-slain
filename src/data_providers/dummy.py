import random
import time

from .provider import BaseProvider, Org, Player, Theme


class Provider(BaseProvider):
    def _lookup_player(self, handle: str) -> Player:
        time.sleep(random.random() / 5)
        return Player(handle=handle, main_org=random.randbytes(4).hex())

    def _lookup_org(self, spectrum_id: str) -> Org:
        time.sleep(random.random() / 5)
        return Org(sid=spectrum_id, theme=random.choice(list(Theme)))
