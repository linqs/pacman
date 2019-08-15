"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

import pacai.util.util

# Called by search.depthFirstSearch.
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    """

    # *** Your Code Here ***
    pacai.util.util.raiseNotDefined()

# Called by search.breadthFirstSearch.
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    fringe = pacai.util.util.Queue()  # uses a queue, which acts like a LIFO
    x = problem.startingState()
    fringe.push((x, ()))
    explored = set()
    while not fringe.isEmpty():
        state = fringe.pop()
        explored.add(state[0])
        children = problem.successorStates(state[0])
        trackfringe = list(fringe.list)
        trackpositions = [i[0] for i in trackfringe]  # create a list to check if child is going to be expanded anyway
        for child in children:
            addpath = list(state[1])
            addpath.append(child[1])
            child = (child[0], addpath)  # add direction to go to chil's position into the child[1] indice
            checkchild = list(child)
            if child[0] not in explored and child[0] not in trackpositions:  # check if node needs to  been expanded
                if problem.isGoal(child[0]):
                    return child[1]
                else:
                    fringe.push(child)  # push child onto node to be expanded
    return []
    # *** Your Code Here ***
    pacai.util.util.raiseNotDefined()

# Called by search.uniformCostSearch.
def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    pacai.util.util.raiseNotDefined()

# Called by search.aStarSearch.
def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    pacai.util.util.raiseNotDefined()
