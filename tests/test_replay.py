import os
import tempfile
import unittest

from pacai.bin import capture
from pacai.bin import pacman

PACMAN_FILENAME = 'pacai_unittest_pacman.replay'
CAPTURE_FILENAME = 'pacai_unittest_capture.replay'

"""
Test saving and playing replays.
"""
class ReplayTest(unittest.TestCase):

    def test_pacman(self):
        replayPath = os.path.join(tempfile.gettempdir(), PACMAN_FILENAME)

        pacman.main(['--null-graphics', '--fps=500', '-p', 'GreedyAgent', '--record', replayPath])

        self.assertTrue(os.path.isfile(replayPath))

        pacman.main(['--null-graphics', '--replay', replayPath])

        os.remove(replayPath)

    def test_capture(self):
        replayPath = os.path.join(tempfile.gettempdir(), CAPTURE_FILENAME)

        capture.main(['--null-graphics', '--fps=1000', '--record', replayPath])

        self.assertTrue(os.path.isfile(replayPath))

        capture.main(['--null-graphics', '--replay', replayPath])

        os.remove(replayPath)

if __name__ == '__main__':
    unittest.main()
