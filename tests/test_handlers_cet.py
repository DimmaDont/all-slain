import unittest

from handlers.cet import Cet
from state import State


class TestCet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        state = State()
        state.cet_steps = 0
        cls.cet = Cet(state)

    def test_finished(self):
        match = self.cet.pattern.match(
            '[Notice] <ContextEstablisherTaskFinished> establisher="Network" message="CET completed" taskname="InitializeSpawnData" state=eCVS_ReadyToStream(11) status="Finished" runningTime=0.000001 numRuns=1 map="megamap" gamerules="SC_Frontend" sessionId="11111111111111111111111111111111" [Team_Network][Network][Replication][Loading][Persistence]'
        )
        self.assertIsNotNone(match)
        self.assertEqual(match[1], "Finished")
        self.assertEqual(match[2], "InitializeSpawnData")
        self.assertEqual(match[3], "ReadyToStream")
        self.assertEqual(match[4], "11")
        self.assertEqual(match[5], "0.000001")
        self.assertEqual(match[6], "SC_Frontend")

    def test_longwait(self):
        match = self.cet.pattern.match(
            '[Notice] <CContextEstablisherTaskLongWait> establisher="CReplicationModel" message="CET running for a long time" taskname="ModelWaitForViews" state=eCVS_UnstowPlayer(12) status="Busy" runningTime=60.000000 numRuns=900 map="megamap" gamerules="SC_Frontend" sessionId="11111111-1111-1111-1111-111111111111" [Team_Network][Network][Replication][Loading][Persistence]'
        )
        self.assertIsNotNone(match)
        self.assertEqual(match[1], "LongWait")
        self.assertEqual(match[2], "ModelWaitForViews")
        self.assertEqual(match[3], "UnstowPlayer")
        self.assertEqual(match[4], "12")
        self.assertEqual(match[5], "60.000000")
        self.assertEqual(match[6], "SC_Frontend")

    def test_failed_network(self):
        match = self.cet.pattern.match(
            '[Error] <ContextEstablisherTaskFailed> establisher="Network" message="CET failed" taskname="WaitForQueryPlayerData" state=eCVS_ReadyToStream(11) status="Player Query failed" runningTime=12.345678 numRuns=123 map="megamap" gamerules="SC_Frontend" sessionId="11111111111111111111111111111111" [Team_Network][Network][Replication][Loading][Persistence]'
        )
        self.assertIsNotNone(match)
        self.assertEqual(match[1], "Failed")
        self.assertEqual(match[2], "WaitForQueryPlayerData")
        self.assertEqual(match[3], "ReadyToStream")
        self.assertEqual(match[4], "11")
        self.assertEqual(match[5], "12.345678")
        self.assertEqual(match[6], "SC_Frontend")

    def test_failed_c_replication_model(self):
        match = self.cet.pattern.match(
            '[Error] <ContextEstablisherTaskFailed> establisher="CReplicationModel" message="CET failed" taskname="ModelWaitForViews" state=eCVS_ResetEntitySystem(1) status="ModelWaitForViews timed out after 1234.56 seconds waiting for the necessary views to be in sync with the model" runningTime=1234.567890 numRuns=12345 map="megamap" gamerules="SC_Frontend" sessionId="aaaaaaaa-1234-1234-1234-123456789012" [Team_Network][Network][Replication][Loading][Persistence]'
        )
        self.assertIsNotNone(match)
        self.assertEqual(match[1], "Failed")
        self.assertEqual(match[2], "ModelWaitForViews")
        self.assertEqual(match[3], "ResetEntitySystem")
        self.assertEqual(match[4], "1")
        self.assertEqual(match[5], "1234.567890")
        self.assertEqual(match[6], "SC_Frontend")
