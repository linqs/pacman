from pacai.agents.capture.capture import CaptureAgent

def createTeam(firstIndex, secondIndex, isRed):

    firstAgent = DefensiveAgent
    secondAgent = OffensiveAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

class ReflexAgent(CaptureAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    # def chooseAction(self, gameState):

    # def getSuccessor(self, gameState, action):

    # def evaluate(self, gameState, action):

    # def getFeatures(self, gameState, action):

    # def getWeights(self, gameState, action):


class DefensiveAgent(ReflexAgent):

    def __init__(self, index, **kwargs):
        super().__init__(index)

    # def getFeatures(self, gameState, action):

    # def getWeights(self, gameState, action):

class OffensiveAgent(ReflexAgent):

    def __init__(self, index, **kwargs):
        super().__init__(index)

    # def getFeatures(self, gameState, action):

    # def getWeights(self, gameState, action):

# ASTAR ALGORITHM
# def aStarSearch(problem, heuristic):
#     """
#     Search the node that has the lowest combined cost and heuristic first.
#     """
#     from pacai.util.priorityQueue import PriorityQueue
#
#     # Initialize structs
#     fringe = PriorityQueue()
#     visited = set()
#     pathToNode = []
#
#     fringe.push((problem.startingState(), pathToNode), 0)
#
#     while not fringe.isEmpty():
#         state, path = fringe.pop()
#         if problem.isGoal(state):
#             return path
#
#         if state not in visited:
#             visited.add(state)
#             for succState, action, cost in problem.successorStates(state):
#                 if succState not in visited:
#                     totalCost = problem.actionsCost(path + [action])
#                     fringe.push((succState, path + [action]),
#                                 totalCost + heuristic(succState, problem))