#!/usr/bin/env python3
import re


class SCLogParser:
    PATTERNS = {
        "CET": re.compile(
            r'<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <(ContextEstablisherTaskFinished|CContextEstablisherTaskLongWait)> establisher="\w+" message="[\w\s]+" taskname="([\w\.]+)" state=eCVS_(\w+)\((\d+)\) status="\w+" runningTime=(\d+\.\d).*'
        ),
        "KILLP": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Actor Death> CActor::Kill: '([\w-]+)' \[\d+\] in zone '([\w-]+)' killed by '([\w-]+)' \[\d+\] using '[\w-]+' \[Class ([\w-]+)\] with damage type '([A-Za-z]+)' from direction (.*) \[Team_ActorTech\]\[Actor\]"
        ),
        "KILLV": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Vehicle Destruction> CVehicle::OnAdvanceDestroyLevel: Vehicle '([\w-]+)' \[\d+\] in zone '([\w-]+)' \[pos.*\] driven by '([\w-]+)' \[\d+\] advanced from destroy level \d to (\d) caused by '([\w-]+)' \[[0-9_]+\] with '([A-Za-z]+)' \[Team_VehicleFeatures\]\[Vehicle\]"
        ),
        "RESPAWN": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Corpse> Player '([\w-]+)' <(?:remote|local) client>: DoesLocationContainHospital: Searching landing zone location \"(.*)\" for the closest hospital. \[Team_ActorTech\]\[Actor\]"
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
        "QUITLOBBY": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <\[EALobby\] EALobbyQuit> \[EALobby\]\[CEALobby::RequestQuitLobby\] ([\w-]+) Requesting QuitLobby.*"
        ),
        "INCAP": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> Logged an incap\.! nickname: ([\w-]+), causes: \[(.+)\]"
        ),
        "JUMP": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Changing Solar System>.* Client entity ([\w-]*) .* changing system from ([\w-]*) to ([A-Za-z0-9]*) .*"
        ),
        "QUIT": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <SystemQuit> CSystem::Quit invoked .+"
        ),
        "QUANTUM": re.compile(
            r"<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <Quantum Navtarget> CSCItemQuantumDrive::RmMulticastOnQTToPoint : Local client user ([\w-]*)\[\d{12}\] received QT data for Entity:\w+_\d{12,}\[\d{12,}\] to Target (\w+).*"
        ),
    }

    @classmethod
    def find_match(cls, line: str) -> tuple[str, re.Match] | None:
        for event_type, regex in cls.PATTERNS.items():
            if match := regex.match(line):
                return (event_type, match)
        return None
