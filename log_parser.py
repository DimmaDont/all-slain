#!/usr/bin/env python3
import re


class SCLogParser:
    def __init__(self):
        self.log_patterns = {
            "INCAP": re.compile(
                r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> Logged an incap\.! nickname: ([A-Za-z0-9_-]+), causes: \[(.+)\]"
            ),
            "JUMP": re.compile(
                r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Changing Solar System>.* Client entity ([A-Za-z0-9_-]*) .* changing system from ([A-Za-z0-9_-]*) to ([A-Za-z0-9]*) .*"
            ),
            "KILLP": re.compile(
                r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Actor Death> CActor::Kill: '([A-Za-z0-9_-]+)' \[\d+\] in zone '([A-Za-z0-9_-]+)' killed by '([A-Za-z0-9_-]+)' \[\d+\] using '[A-Za-z0-9_-]+' \[Class ([A-Za-z0-9_-]+)\] with damage type '([A-Za-z]+)' from direction (.*) \[Team_ActorTech\]\[Actor\]"
            ),
            "KILLV": re.compile(
                r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([A-Za-z0-9_-]+)' \[\d+\] in zone '([A-Za-z0-9_-]+)' \[pos.*\] driven by '([A-Za-z0-9_-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([A-Za-z0-9_-]+)' \[[0-9_]+\] with '([A-Za-z]+)' \[Team_VehicleFeatures\]\[Vehicle\]"
            ),
            "QUIT": re.compile(
                r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <\[EALobby\] EALobbyQuit> \[EALobby\]\[CEALobby::RequestQuitLobby\] ([A-Za-z0-9_-]+) Requesting QuitLobby.*"
            ),
            "RESPAWN": re.compile(
                r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Corpse> Player '([A-Za-z0-9_-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital. \[Team_ActorTech\]\[Actor\]"
            ),
            "SPAWN": re.compile(
                r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[CSessionManager::OnClientSpawned\] Spawned!"
            ),
        }

        return None

    def parseLog(self, line: str) -> dict:
        match_sets = {_: None for _ in self.log_patterns.keys()}
        for event_type in self.log_patterns.keys():
            if matches := self.log_patterns[event_type].match(line):
                match_sets[event_type] = matches
        return match_sets
