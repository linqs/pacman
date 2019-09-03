import unittest

from pacai.util import priority_queue
from pacai.util import queue
from pacai.util import stack

"""
This is a test class to assess the functionality of the data structures
defined in util.py. The data structures to be tested are the Queue, Stack,
and the Priority Queue.
"""
class UtilTest(unittest.TestCase):
    def test_queue(self):
        q = queue.Queue()
        self.assertTrue(q.isEmpty())

        val_list = [x for x in range(1, 10)]
        for val in val_list:
            q.push(val)
        self.assertFalse(q.isEmpty())
        self.assertEquals(len(val_list), len(q))

        # Test Queue for FIFO functionality.
        for val in val_list:
            self.assertEqual(val, q.pop())

    def test_stack(self):
        intStack = stack.Stack()
        self.assertTrue(intStack.isEmpty())

        val_list = [x for x in range(1, 10)]
        for val in val_list:
            intStack.push(val)
        self.assertFalse(intStack.isEmpty())
        self.assertEquals(len(val_list), len(intStack))

        # Test Stack for LIFO functionality.
        for val in reversed(val_list):
            self.assertEqual(val, intStack.pop())

    def test_priority_queue(self):
        priQ = priority_queue.PriorityQueue()
        self.assertTrue(priQ.isEmpty())

        # List of values with a priority number that correspondes to the position in the list.
        val_list = [(x, -x) for x in range(1, 10)]
        for val, pri in val_list:
            priQ.push(val, pri)
        self.assertFalse(priQ.isEmpty())
        self.assertEquals(len(val_list), len(priQ))

        # Test Min Queue for priority functionality.
        for val, pri in reversed(val_list):
            self.assertEqual(val, priQ.pop())

if __name__ == '__main__':
    unittest.main()
