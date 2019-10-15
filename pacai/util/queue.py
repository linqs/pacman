"""
A queue container data structure.
"""

class Queue(object):
    """
    A container with a first-in-first-out (FIFO) queuing policy.
    """

    def __init__(self):
        self.list = []

    def push(self, item):
        """
        Enqueue the item into the queue.
        """

        self.list.insert(0, item)

    def pop(self):
        """
        Dequeue the earliest enqueued item still in the queue.
        This operation removes the item from the queue.
        """

        return self.list.pop()

    def isEmpty(self):
        """
        Returns True if the queue is empty.
        """

        return len(self.list) == 0

    def __len__(self):
        return len(self.list)
