import unittest

from pacai.util import priorityQueue
from pacai.util import queue
from pacai.util import stack

"""
This is a test class to assess the functionality of the data structures defined in util.py.
"""
class UtilContainersTest(unittest.TestCase):
    def test_queue(self):
        testQueue = queue.Queue()
        self.assertTrue(testQueue.isEmpty())

        val_list = [x for x in range(1, 10)]
        for val in val_list:
            testQueue.push(val)
        self.assertFalse(testQueue.isEmpty())
        self.assertEquals(len(val_list), len(testQueue))

        # Test Queue for FIFO functionality.
        for val in val_list:
            self.assertEqual(val, testQueue.pop())

    def test_stack(self):
        testStack = stack.Stack()
        self.assertTrue(testStack.isEmpty())

        val_list = [x for x in range(1, 10)]
        for val in val_list:
            testStack.push(val)
        self.assertFalse(testStack.isEmpty())
        self.assertEquals(len(val_list), len(testStack))

        # Test Stack for LIFO functionality.
        for val in reversed(val_list):
            self.assertEqual(val, testStack.pop())

    def test_priority_queue(self):
        testPriorityQueue = priorityQueue.PriorityQueue()
        self.assertTrue(testPriorityQueue.isEmpty())

        # List of values with a priority number that correspondes to
        # the position in the list.
        val_list = [(x, -x) for x in range(1, 10)]
        for val, pri in val_list:
            testPriorityQueue.push(val, pri)
        self.assertFalse(testPriorityQueue.isEmpty())
        self.assertEquals(len(val_list), len(testPriorityQueue))

        # Test Min Queue for priority functionality.
        for val, pri in reversed(val_list):
            self.assertEqual(val, testPriorityQueue.pop())

if __name__ == '__main__':
    unittest.main()
