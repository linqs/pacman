"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    node_stack = Stack()  # a stack is used so we explore down a whole branch first since it is LIFO
    explored = set()  # keeps track of all the explored nodes

    node_stack.push((problem.startingState(), [], 0))
    # push the node we are on, the path (which is empty because we just started),
    # and the cost (which is 0 bc we just started) onto the node_stack
    while not node_stack.isEmpty():  # while there are still states to explore
        curr_node, path, cost = node_stack.pop()  # take the next node to explore from the stack
        if problem.isGoal(curr_node):  # if we have achieved the goal, return path that achieved it
            return path
        else:
            if curr_node not in explored:  # if we havent already explored the node
                explored.add(curr_node)  # mark the node as explored
                successor_states = problem.successorStates(curr_node)
                # get the successor states from the node
                for successor_state in successor_states:
                    # push each successor state onto the stack so we can explore them
                    node_stack.push((successor_state[0],
                        path + [successor_state[1]], successor_state[2] + cost))
    return None

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    node_queue = Queue()
    # a queue is used so we explore nodes left to right
    # rather than up and down with a stack because a queue is FIFO
    explored = []  # keeps track of all the explored nodes

    node_queue.push((problem.startingState(), [], 0))
    # push the node we are on, the path (which is empty because we just started),
    # and the cost (which is 0 bc we just started) onto the node_stack
    while not node_queue.isEmpty():  # while there are still states to explore
        curr_node, path, cost = node_queue.pop()  # take the next node to explore from the queue
        if problem.isGoal(curr_node):  # if we have achieved the goal, return path that achieved it
            return path
        else:
            if curr_node not in explored:  # if we havent already explored the node
                explored.append(curr_node)  # mark the node as explored
                successor_states = problem.successorStates(curr_node)
                # get the successor states from the node
                for successor_state in successor_states:
                    # push each successor state onto the queue so we can explore them
                    node_queue.push((successor_state[0],
                        path + [successor_state[1]], successor_state[2] + cost))
    return None

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    node_pqueue = PriorityQueue()
    # a priority queue is used so we explore nodes with the least total cost first
    explored = []  # keeps track of all the explored nodes

    node_pqueue.push((problem.startingState(), [], 0), 0)
    # push the node we are on, the path (which is empty because we just started),
    # and the cost (which is 0 bc we just started) onto the node_pqueue and the priority 0
    while not node_pqueue.isEmpty():  # while there are still states to explore
        curr_node, path, cost = node_pqueue.pop()
        # take the next node to explore from the priority queue
        if problem.isGoal(curr_node):  # if we have achieved the goal, return path that achieved it
            return path
        else:
            if curr_node not in explored:  # if we havent already explored the node
                explored.append(curr_node)  # mark the node as explored
                successor_states = problem.successorStates(curr_node)
                # get the successor states from the node
                for successor_state in successor_states:
                    # push each successor state onto the queue so we can explore them
                    node_pqueue.push((successor_state[0], path + [successor_state[1]],
                        successor_state[2] + cost), cost)
                    # we record the cost of visiting node as well as the total cost of the path

    return None

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    node_pqueue = PriorityQueue()
    # a priority queue is used so we explore nodes with the least total cost first
    explored = []  # keeps track of all the explored nodes

    node_pqueue.push((problem.startingState(), [], 0),
        heuristic(problem.startingState(), problem))
    # push the node we are on, the path (which is empty because we just started),
    # and the cost (which is 0 bc we just started) onto the node_pqueue and the priority 0
    while True:  # while there are still states to explore
        curr_node, path, cost = node_pqueue.pop()
        # take the next node to explore from the priority queue
        if problem.isGoal(curr_node):  # if we have achieved the goal, return path that achieved it
            return path
        else:
            if curr_node not in explored:  # if we havent already explored the node
                explored.append(curr_node)  # mark the node as explored
                successor_states = problem.successorStates(curr_node)
                # get the successor states from the node
                for successor_state in successor_states:
                    # push each successor state onto the queue so we can explore them
                    node_pqueue.push((successor_state[0], path + [successor_state[1]],
                        successor_state[2] + cost),
                        heuristic(successor_state[0], problem) + cost + successor_state[2])
                    # we record the cost of visiting node as well as the total cost of the path
                    # h(n) + f(n) is the cost for astar

    return None
