import unittest

from pacai.util import util

"""
Test misc utilities.
"""
class UtilTest(unittest.TestCase):
    def test_hash(self):
        self.assertEquals(util.buildHash(1), 630)
        self.assertEquals(util.buildHash(2), 631)

        self.assertEquals(util.buildHash(1, 1), 23311)
        self.assertEquals(util.buildHash(1, 2), 23312)

if __name__ == '__main__':
    unittest.main()
