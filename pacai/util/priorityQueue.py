"""
Priority queue containers.
"""

import heapq

class PriorityQueue(object):
    """
    Implements a priority queue data structure.
    Each inserted item has a priority associated with it,
    and the user is usually interested in quick retrieval of the lowest-priority item in the queue.
    This data structure allows O(1) access to the lowest-priority item.

    Note that this PriorityQueue does not allow you to change the priority of an item.
    However, you may insert the same item multiple times with different priorities.
    """

    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        pair = (priority, item)
        heapq.heappush(self.heap, pair)

    def pop(self):
        (priority, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def __len__(self):
        return len(self.heap)

class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the Queue and the Stack classes.
    This is designed for drop-in replacement for those two classes.
    The caller has to provide a priority function, which extracts each item's priority.
    """

    def __init__(self, priorityFunction):
        """
        priorityFunction (item) -> priority
        """

        super().__init__()
        self.priorityFunction = priorityFunction

    def push(self, item):
        """
        Adds an item to the queue with priority from the priority function
        """

        super().push(item, self.priorityFunction(item))

    def __len__(self):
        return len(self.heap)
