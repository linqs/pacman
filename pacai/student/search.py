"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """
    # *** Your Code Here ***
    stk = list()
    visited = set()
    res = list()
    goal_found = False
    in_frontier = set()
    for successor in problem.successorStates(problem.startingState()):
        stk.append(successor)
        in_frontier.add(successor[0])
    visited.add(problem.startingState())
    while(len(stk)):
        cur = stk[-1]
        if(problem.isGoal(cur[0])):
            goal_found = True
            visited.add(cur[0])
            res.append(cur)
            stk.pop()
            continue
        if(not goal_found):
            if(not (cur[0] in visited)):
                visited.add(cur[0])
                for successor in problem.successorStates(cur[0]):
                    if not (successor[0] in visited) and not(successor[0] in in_frontier):
                        in_frontier.add(successor[0])
                        stk.append(successor)
            else:
                stk.pop()
        else:
            if(not (cur[0] in visited)):
                stk.pop()
            else:
                res.append(cur)
                stk.pop()
    res.reverse()
    output = [item[1] for item in res]
    return output

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    Start: (5, 5)
    Is the start a goal?: False
    Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    successor == ((5, 4), 'South', 1)
    """
    visited = set()
    in_frontier = set()
    predecessor = dict()
    frontier_queue = Queue()
    visited.add(problem.startingState())
    for successor in problem.successorStates(problem.startingState()):
        frontier_queue.push(successor)
        in_frontier.add(successor[0])
        predecessor[successor] = problem.startingState()
    goal = None
    while (not frontier_queue.isEmpty()):
        cur = frontier_queue.pop()
        visited.add(cur[0])
        if problem.isGoal(cur[0]):
            goal = cur
            break
        for successor in problem.successorStates(cur[0]):
            if not(successor[0] in visited) and not(successor[0] in in_frontier):
                frontier_queue.push(successor)
                in_frontier.add(successor[0])
                predecessor[successor] = cur
    res = []
    if(goal is None):
        return []
    while (not (goal == problem.startingState())):
        res.append(goal[1])
        goal = predecessor[goal]
    res.reverse()
    return res

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    # *** Your Code Here ***
    visited = set()                     # *** pos ***
    opened = dict()                     # *** pos --> sum_cost ***
    predecessor = dict()                # *** (pos, pre_action) --> (pos, pre_action) ***
    frontier_queue = PriorityQueue()    # *** (pos, pre_action, sum_cost) ***
    visited.add(problem.startingState())
    for successor in problem.successorStates(problem.startingState()):
        frontier_queue.push(successor, successor[2])
        opened[successor[0]] = successor[2]
        predecessor[(successor[0], successor[1])] = (problem.startingState(), "None(Origin)")
    goal = None
    while (not frontier_queue.isEmpty()):
        cur = frontier_queue.pop()
        visited.add(cur[0])
        if problem.isGoal(cur[0]):
            goal = (cur[0], cur[1])
            break
        for successor in problem.successorStates(cur[0]):
            if not(successor in visited):
                if not((successor[0] in opened)
                        and (opened[successor[0]] <= successor[2] + cur[2])):
                    frontier_queue.push((successor[0], successor[1], successor[2] + cur[2]),
                    successor[2] + cur[2])
                    opened[successor[0]] = successor[2] + cur[2]
                    predecessor[(successor[0], successor[1])] = (cur[0], cur[1])
    res = []
    while (not (goal[0] == problem.startingState())):
        res.append(goal[1])
        goal = predecessor[goal]
    res.reverse()
    return res

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # *** Your Code Here ***
    '''
    visited = set()                     # *** pos ***
    opened = dict()                     # *** pos --> f(pos) ***
    predecessor = dict()                # *** (pos, pre_action) --> (pos, pre_action) ***
    frontier_queue = PriorityQueue()    # *** (pos, pre_action, sum_cost), priority <==> f(cur) ***
    visited.add(problem.startingState())
    for successor in problem.successorStates(problem.startingState()):
        # *** f(n+1) = sum(n) + cost(n->n+1) + h(n+1) ***
        eval = 0 + successor[2] + heuristic(successor[0], problem)
        frontier_queue.push(successor, eval)
        opened[successor[0]] = eval
        predecessor[(successor[0], successor[1])] = (problem.startingState(), "None(Origin)")
    goal = None
    while (not frontier_queue.isEmpty()):
        cur = frontier_queue.pop()
        visited.add(cur[0])
        if problem.isGoal(cur[0]):
            goal = (cur[0], cur[1])
            break
        for successor in problem.successorStates(cur[0]):
            if not(successor in visited):
                eval = cur[2] + successor[2] + heuristic(successor[0], problem)
                if not((successor[0] in opened) and (opened[successor[0]] <= eval)):
                    frontier_queue.push((successor[0], successor[1], successor[2] + cur[2]), eval)
                    opened[successor[0]] = eval
                    predecessor[(successor[0], successor[1])] = (cur[0], cur[1])
    res = []
    while (not (goal[0] == problem.startingState())):
        res.append(goal[1])
        goal = predecessor[goal]
    res.reverse()
    return res
    '''
    visited = set()                     # *** pos ***
    opened = dict()                     # *** pos --> f(pos) ***
    predecessor = dict()                # *** (pos, pre_action) --> (pos, pre_action) ***
    frontier_queue = PriorityQueue()    # *** (pos, pre_action, sum_cost), priority <==> f(cur) ***
    visited.add(problem.startingState())
    for successor in problem.successorStates(problem.startingState()):
        # *** f(n+1) = sum(n) + cost(n->n+1) + h(n+1) ***
        eval = 0 + successor[2] + heuristic(successor[0], problem)
        frontier_queue.push(successor, eval)
        opened[successor[0]] = eval
        predecessor[(successor[0], successor[1])] = (problem.startingState(), "None(Origin)")
    goal = None
    while (not frontier_queue.isEmpty()):
        cur = frontier_queue.pop()
        if(cur[0] in visited):
            continue
        visited.add(cur[0])
        if problem.isGoal(cur[0]):
            goal = (cur[0], cur[1])
            break
        for successor in problem.successorStates(cur[0]):
            if not(successor in visited):
                eval = cur[2] + successor[2] + heuristic(successor[0], problem)
                if not((successor[0] in opened) and (opened[successor[0]] <= eval)):
                    frontier_queue.push((successor[0], successor[1], successor[2] + cur[2]), eval)
                    opened[successor[0]] = eval
                    predecessor[(successor[0], successor[1])] = (cur[0], cur[1])
    res = []
    while (not (goal[0] == problem.startingState())):
        res.append(goal[1])
        goal = predecessor[goal]
    res.reverse()
    return res
