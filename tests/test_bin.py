import unittest

from pacai.bin import capture
from pacai.bin import gridworld
from pacai.bin import pacman

"""
This is a test class to assess the executables of this project.
"""
class BinTest(unittest.TestCase):

    def test_pacman(self):
        # Run game of pacman with valid agent.
        pacman.main(['-p', 'GreedyAgent', '--null-graphics'])

        # Raise exception for passing in invalid agent for game of pacman.
        try:
            pacman.main(['-p', 'WhatAgent', '--null-graphics'])
            self.fail("Test did not raise expected exception.")
        except LookupError:
            # Expected exception.
            pass

    def test_pacman_help(self):
        # Show all pacman arguments.
        try:
            pacman.main(['--help'])
        except SystemExit as status:
            if status.code != 0:
                self.fail("Error occured when running --help.")

    def test_capture(self):
        # Run game of capture with default agents.
        capture.main(['--null-graphics'])

    def test_capture_help(self):
        # Show all capture arguments.
        try:
            capture.main(['--help'])
        except SystemExit as status:
            if status.code != 0:
                self.fail("Error occured when running --help.")

    def test_gridworld(self):
        # Run game of gridworld with default agents.
        gridworld.main(['--null-graphics'])

    def test_gridworld_help(self):
        # Show all gridworld arguments.
        try:
            gridworld.main(['--help'])
        except SystemExit as status:
            if status.code != 0:
                self.fail("Error occured when running --help.")

    def test_seeded_runs(self):
        # Run game of capture with seed entry.
        capture.main(['--null-graphics', '--seed', '1234'])

        # Run game of pacman with seed value entry.
        pacman.main(['-p', 'GreedyAgent', '--null-graphics', '--seed', '1234'])

    def test_capture_seeded_maze_generations(self):
        # Run game of capture with random generated map without seed value.
        capture.main(['--null-graphics', '--layout', 'RANDOM']) 

        # Run game of capture with random generated map with seed value.
        capture.main(['--null-graphics', '--layout', 'RANDOM94'])

if __name__ == '__main__':
    unittest.main()
