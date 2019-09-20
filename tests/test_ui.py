import shutil
import subprocess
import unittest

"""
Test standard graphics under xvfb.
"""
class UITest(unittest.TestCase):
    def test_pacman(self):
        if (shutil.which('xvfb-run') is None):
            print("Skipping test, could not find xvfb.")
            return

        args = [
            'xvfb-run', '-a',
            '-w', '0.01',
            'python3',
            '-m', 'pacai.bin.pacman',
            '--frameTime=0.001',
            '-p', 'GreedyAgent',
        ]

        subprocess.run(args, shell = False, check = True)

    def test_capture(self):
        if (shutil.which('xvfb-run') is None):
            print("Skipping test, could not find xvfb.")
            return

        args = [
            'xvfb-run', '-a',
            '-w', '0.01',
            'python3',
            '-m', 'pacai.bin.capture',
        ]

        subprocess.run(args, shell = False, check = True)

    def test_gridworld(self):
        if (shutil.which('xvfb-run') is None):
            print("Skipping test, could not find xvfb.")
            return

        args = [
            'xvfb-run', '-a',
            '-w', '0.01',
            'python3',
            '-m', 'pacai.bin.gridworld',
            '-q',
        ]

        subprocess.run(args, shell = False, check = True)

if __name__ == '__main__':
    unittest.main()
