from pacai.agents.capture.capture import CaptureAgent
from pacai.core.directions import Directions
import random
from pacai.util import util


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

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
        """

        actions = gameState.getLegalActions(self.index)
        values = [self.evaluate(gameState, a) for a in actions]

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """

        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()

        if (pos != util.nearestPoint(pos)):
            # Only half a grid position was covered.
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights.
        """

        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        stateEval = sum(features[feature] * weights[feature] for feature in features)
        return stateEval


class DefensiveAgent(ReflexAgent):

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}

        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1
        foodList = self.getFood(successor).asList()
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
        return features

    def getWeights(self, gameState, action):
        return {
            'distanceToFood': -1,
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -100,
            'stop': -100,
            'reverse': -2,
            'distanceToCapsule': -1
        }


class OffensiveAgent(ReflexAgent):

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)

        features['successorScore'] = self.getScore(successor)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        distToClosestDefender = -1
        # Computes whether we're on defense (1) or offense (0).

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        defenders = [a for a in enemies if not a.isPacman() and a.getPosition() is not None]

        distToClosestDefender = \
            min([self.getMazeDistance(myPos, a.getPosition()) for a in defenders])

        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            if (min(dists) < 3) and myState.isPacman() == 0:
                features['besideEnemy'] = 100 / min(dists)

        features['numInvaders'] = len(invaders)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        # Compute distance to the nearest capsule
        capsuleList = self.getCapsules(successor)

        if len(capsuleList) > 0:
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, capsule) for capsule in capsuleList])
            if minDistance < 3 and minDistance < distToClosestDefender / 2:
                features['distanceToCapsule'] = 100  # To change
            else:
                features['distanceToCapsule'] = minDistance

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'besideEnemy': 1,
            'successorScore': 100,
            'distanceToFood': -1,
            'stop': -100,
            'reverse': -2,
            'distanceToCapsule': -0.5
        }

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
