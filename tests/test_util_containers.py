import unittest

from pacai.util import containers

"""
This is a test class to assess the functionality of the data structures
defined in util.py. The data structures to be tested are the Queue, Stack,
and the Priority Queue.
"""
class UtilTest(unittest.TestCase):
    def test_queue(self):
        queue = containers.Queue()
        self.assertTrue(queue.isEmpty())

        val_list = [x for x in range(1, 10)]
        for val in val_list:
            queue.push(val)
        self.assertFalse(queue.isEmpty())
        self.assertEquals(len(val_list), len(queue))

        # Test Queue for FIFO functionality.
        for val in val_list:
            self.assertEqual(val, queue.pop())

    def test_stack(self):
        stack = containers.Stack()
        self.assertTrue(stack.isEmpty())

        val_list = [x for x in range(1, 10)]
        for val in val_list:
            stack.push(val)
        self.assertFalse(stack.isEmpty())
        self.assertEquals(len(val_list), len(stack))

        # Test Stack for LIFO functionality.
        for val in reversed(val_list):
            self.assertEqual(val, stack.pop())

    def test_priority_queue(self):
        priority_queue = containers.PriorityQueue()
        self.assertTrue(priority_queue.isEmpty())

        # List of values with a priority number that correspondes to the position in the list.
        val_list = [(x, -x) for x in range(1, 10)]
        for val, pri in val_list:
            priority_queue.push(val, pri)
        self.assertFalse(priority_queue.isEmpty())
        self.assertEquals(len(val_list), len(priority_queue))

        # Test Min Queue for priority functionality.
        for val, pri in reversed(val_list):
            self.assertEqual(val, priority_queue.pop())

if __name__ == '__main__':
    unittest.main()
