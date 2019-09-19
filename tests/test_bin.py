import unittest

from pacai.bin import capture
from pacai.bin import gridworld
from pacai.bin import pacman

"""
This is a test class to assess the executables of this project
"""
class BinTest(unittest.TestCase):

    def test_pacman(self):
        # Run game of pacman with valid agent.
        pacman.main(['-p', 'GreedyAgent', '-q'])

        # Raise exception for passing in invalid agent for game of pacman.
        try:
            pacman.main(['-p', 'WhatAgent', '-q'])
            self.fail("Test did not raise expected exception.")
        except LookupError:
            # Expected exception.
            pass

    def test_capture(self):
        # Run game of capture with default agents.
        capture.main(['-q'])

    def test_gridworld(self):
        # Run game of capture with default agents.
        gridworld.main(['-t', '-q'])

if __name__ == '__main__':
    unittest.main()
