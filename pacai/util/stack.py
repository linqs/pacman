"""
A stack data structure.
"""

class Stack(object):
    """
    A container with a last-in-first-out (LIFO) queuing policy.
    """

    def __init__(self):
        self.list = []

    def push(self, item):
        """
        Push an item onto the stack.
        """

        self.list.append(item)

    def pop(self):
        """
        Pop the most recently pushed item from the stack.
        """

        return self.list.pop()

    def isEmpty(self):
        """
        Returns True if the stack is empty.
        """

        return len(self.list) == 0

    def __len__(self):
        return len(self.list)
