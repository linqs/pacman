from pacai.util import reflection
import logging
import random
import time
from pacai.core.directions import Directions
from pacai.agents.capture.capture import CaptureAgent
from pacai.util import util

def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.student.myTeam.PacmanSlashBurstOffensive',
        second = 'pacai.student.myTeam.PacmanSlashBurstDefensive'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = reflection.qualifiedImport(first)
    secondAgent = reflection.qualifiedImport(second)

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

class PacmanSlashBurst(CaptureAgent):

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
        """

        actions = gameState.getLegalActions(self.index)

        start = time.time()
        values = [self.evaluate(gameState, a) for a in actions]
        logging.debug('evaluate() time for agent %d: %.4f' % (self.index, time.time() - start))

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

class PacmanSlashBurstDefensive(PacmanSlashBurst):
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.inScary = 0

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        #
        if myState.getScaredTimer() > 0:
            self.inScary = 1
        else:
            self.inScary = -1
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
            if(self.inScary == 1 and min(dists) >= 3):
                features['invaderDistance'] = -min(dists)
            else:
                features['invaderDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': self.inScary * 10,
            'stop': -100,
            'reverse': -2
        }

class PacmanSlashBurstOffensive(PacmanSlashBurst):
    """
    A reflex agent that seeks food.
    This agent will give you an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)
        self.immune = -1

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)
        myState = successor.getAgentState(self.index)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = 1 / (minDistance + 0.01)

        # Ghost
        self.immune = -1
        features["isPacman"] = -1
        if myState.isPacman():
            features["isPacman"] = 1
            enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
            ghosts = [a for a in enemies if a.isGhost() and a.getPosition() is not None]
            if (len(ghosts) > 0):
                if(ghosts[0].getScaredTimer() > 0):
                    self.immune = 0
                dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
                if(min(dists) > 10):
                    features['ghostDistance'] = -1
                else:
                    features['ghostDistance'] = 1 / (min(dists) + 0.01)
            else:
                features['ghostDistance'] = 0
        else:
            features['ghostDistance'] = 0

        # Capsules
        if(len(self.getCapsules(successor)) > 0):
            cap_dists = [self.getMazeDistance(myPos, pos) for pos in self.getCapsules(successor)]
            features['capsuleDistance'] = 1 / (min(cap_dists) + 0.01)
        else:
            features['capsuleDistance'] = 5000

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            if(myState.isGhost()):
                features['reverse'] = 1
            else:
                features['reverse'] = 0.2
        else:
            features['reverse'] = 0

        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': 1,
            'ghostDistance': self.immune * 5,
            'capsuleDistance': 5,
            'stop': -100,
            'reverse': -30,
            "isPacman": 5
        }
