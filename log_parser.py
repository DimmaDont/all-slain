#!/usr/bin/env python3
import re


class SCLogParser:
    PATTERNS = {
        "CET": re.compile(
            r'<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <(ContextEstablisherTaskFinished|CContextEstablisherTaskLongWait)> establisher="\w+" message="[\w\s]+" taskname="([\w\.]+)" state=eCVS_(\w+)\((\d+)\) status="\w+" runningTime=(\d+\.\d).*'
        ),
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
        "CONNECTING": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[CSessionManager::ConnectCmd\] Connect started!"
        ),
        "CONNECTED": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[CSessionManager::OnClientConnected\] Connected!"
        ),
        "LOADING": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[CGlobalGameUI::OpenLoadingScreen\] Request context transition to LoadingScreenView"
        ),
        "LOADED": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> Loading screen for (\w+) : SC_Frontend closed after (\d+.\d+) seconds"
        ),
    }

    @classmethod
    def find_match(cls, line: str) -> tuple[str, re.Match] | None:
        for event_type, regex in cls.PATTERNS.items():
            if match := regex.match(line):
                return (event_type, match)
        return None
