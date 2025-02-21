import unittest

from pacai.bin import capture
from pacai.agents.capture.timeout import TimeoutAgent

class CaptureTest(unittest.TestCase):
    def test_base(self):
        games = capture.main([
            '--null-graphics',
            '--catch-exceptions',
            '--max-moves', '16',
        ])

        self.assertTrue(games[0].gameOver)
        self.assertFalse(games[0].agentCrashed)
        self.assertFalse(games[0].agentTimeout)

    def test_full_game_timeout(self):
        games = capture.main([
            '--null-graphics',
            '--catch-exceptions',
            '--max-total-agent-time', '0.01',
        ])

        self.assertTrue(games[0].gameOver)
        self.assertTrue(games[0].agentCrashed)
        self.assertTrue(games[0].agentTimeout)

    def test_no_timeout(self):
        games = capture.main([
            '--null-graphics',
            '--catch-exceptions',
            '--blue', 'pacai.core.timeoutTeam',
            '--max-moves', '16',
        ])

        self.assertTrue(games[0].gameOver)
        self.assertFalse(games[0].agentCrashed)
        self.assertFalse(games[0].agentTimeout)

    def test_init_timeout(self):
        try:
            TimeoutAgent.waitInitDurationSecs = 0.5

            games = capture.main([
                '--null-graphics',
                '--catch-exceptions',
                '--blue', 'pacai.core.timeoutTeam',
                '--max-startup-time', '0.1',
            ])
        finally:
            TimeoutAgent.reset()

        self.assertTrue(games[0].gameOver)
        self.assertTrue(games[0].agentCrashed)
        self.assertTrue(games[0].agentTimeout)

    def test_move_timeout(self):
        try:
            TimeoutAgent.waitMoveDurationSecs = 0.5

            games = capture.main([
                '--null-graphics',
                '--catch-exceptions',
                '--blue', 'pacai.core.timeoutTeam',
                '--move-timeout-time', '0.1',
            ])
        finally:
            TimeoutAgent.reset()

        self.assertTrue(games[0].gameOver)
        self.assertTrue(games[0].agentCrashed)
        self.assertTrue(games[0].agentTimeout)

    def test_move_warnings(self):
        try:
            TimeoutAgent.waitMoveDurationSecs = 0.1

            games = capture.main([
                '--null-graphics',
                '--catch-exceptions',
                '--blue', 'pacai.core.timeoutTeam',
                '--move-warning-time', '0.05',
            ])
        finally:
            TimeoutAgent.reset()

        self.assertTrue(games[0].gameOver)
        self.assertTrue(games[0].agentCrashed)
        self.assertTrue(games[0].agentTimeout)

        # Each blue agent should get a warning on every turn.
        # The game ends right away at the third warning an agent gets.
        self.assertEqual(5, sum(games[0].totalAgentTimeWarnings))
