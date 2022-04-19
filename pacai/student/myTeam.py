from pacai.util import reflection
from pacai.agents.capture.capture import CaptureAgent
from pacai.core.distance import maze, manhattan
import random

def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.agents.capture.dummy.DummyAgent',
        second = 'pacai.agents.capture.dummy.DummyAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """
    #pacai.agents.capture.dummy.DummyAgent
    firstAgent = UpperAgent
    secondAgent = LowerAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

class UpperAgent(CaptureAgent):
    def __init__(self, index, timeForComputing = 0.1, **kwargs):
        super().__init__(index, **kwargs)
        self.index = index
        self.past = []

    def chooseAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        scores = []
        for action in legalMoves:
            if self.past.count(gameState.generateSuccessor(self.index, action).getAgentState(self.index).getPosition()) > 3:
                scores.append(float('-inf'))
            else:
                scores.append(self.evaluationFunction(gameState, action))
        # scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        self.past.append(gameState.generateSuccessor(self.index, legalMoves[chosenIndex]).getAgentState(self.index).getPosition())
        if len(self.past) > 20:
            self.past.pop(0)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currgameState, action):
        nextstate = currgameState.generateSuccessor(self.index, action)
        mypos = (int(nextstate.getAgentState(self.index).getPosition()[0]), 
            int(nextstate.getAgentState(self.index).getPosition()[1]))
        kuandu = currgameState.getInitialLayout().getWidth()
        oppoa = self.getOpponents(currgameState)
        ghosts = [currgameState.getAgentState(i).getPosition() for i in oppoa]

        # only chase when is not scared ghost
        if (((nextstate.isOnRedTeam(self.index) and nextstate.isOnRedSide(mypos)) or
            (nextstate.isOnBlueTeam(self.index) and nextstate.isOnBlueSide(mypos))) and
            not nextstate.getAgentState(self.index).isScared()):
            minghost = float('inf')
            for j in range(len(ghosts)):
                i = (int(ghosts[j][0]), int(ghosts[j][1]))
                if (i == mypos):
                    return float('inf')
                mz = maze(i, mypos, nextstate)
                minghost = min(mz, minghost)

            minfood = float('inf')
            if (nextstate.isOnRedTeam(self.index)):
                foodpos = currgameState.getBlueFood().asList()
            else:
                foodpos = currgameState.getRedFood().asList()

            # seperate foods, so two agents would chase different food
            maxf = 0
            minf = currgameState.getInitialLayout().getHeight()
            for f in foodpos:
                maxf = max(maxf, f[1])
                minf = min(minf, f[1])
            avg = (minf + maxf) / 2 - 2
            for i in range(len(foodpos) - 1, -1, -1):
                if foodpos[i][1] < avg:
                    foodpos.pop(i)

            for i in foodpos:
                if i == mypos:
                    return float('inf')
                else:
                    temp = minfood
                    minfood = min(maze(i, mypos, nextstate), minfood)
            return 5 / minfood + 1 / minghost
        else:
            minghost = float('inf')
            for j in range(len(ghosts)):
                i = (int(ghosts[j][0]), int(ghosts[j][1]))
                mz = maze(i, mypos, nextstate)
                if (not currgameState.getAgentState(oppoa[j]).isScared()) and (mz < 2 or i == mypos):
                    return float('-inf')
                elif not currgameState.getAgentState(oppoa[j]).isScared():
                    minghost = min(mz, minghost)
            
            minfood = float('inf')
            if (nextstate.isOnRedTeam(self.index)):
                foodpos = currgameState.getBlueFood().asList()
            else:
                foodpos = currgameState.getRedFood().asList()

            maxf = 0
            minf = currgameState.getInitialLayout().getHeight()
            for f in foodpos:
                maxf = max(maxf, f[1])
                minf = min(minf, f[1])
            avg = (minf + maxf) / 2 -2
            for i in range(len(foodpos) - 1, -1, -1):
                if foodpos[i][1] < avg:
                    foodpos.pop(i)
            for i in foodpos:
                if i == mypos:
                    return float('inf')
                else:
                    temp = minfood
                    minfood = min(maze(i, mypos, nextstate), minfood)
            return ((currgameState.getInitialLayout().getWidth() + currgameState.getInitialLayout().getHeight()) / minfood - 1 / minghost) * 2 # prefer attack than defend

class LowerAgent(CaptureAgent):
    def __init__(self, index, timeForComputing = 0.1, **kwargs):
        super().__init__(index, **kwargs)
        self.index = index
        self.past = []

    def chooseAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        scores = []
        for action in legalMoves:
            if self.past.count(gameState.generateSuccessor(self.index, action).getAgentState(self.index).getPosition()) > 3:
                scores.append(float('-inf'))
            else:
                scores.append(self.evaluationFunction(gameState, action))
        # scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        self.past.append(gameState.generateSuccessor(self.index, legalMoves[chosenIndex]).getAgentState(self.index).getPosition())
        if len(self.past) > 20:
            self.past.pop(0)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currgameState, action):
        nextstate = currgameState.generateSuccessor(self.index, action)
        mypos = (int(nextstate.getAgentState(self.index).getPosition()[0]), 
            int(nextstate.getAgentState(self.index).getPosition()[1]))
        kuandu = currgameState.getInitialLayout().getWidth()
        oppoa = self.getOpponents(currgameState)
        ghosts = [currgameState.getAgentState(i).getPosition() for i in oppoa]

        # only chase when is not scared ghost
        if (((nextstate.isOnRedTeam(self.index) and nextstate.isOnRedSide(mypos)) or
            (nextstate.isOnBlueTeam(self.index) and nextstate.isOnBlueSide(mypos))) and
            not nextstate.getAgentState(self.index).isScared()):
            minghost = float('inf')
            for j in range(len(ghosts)):
                i = (int(ghosts[j][0]), int(ghosts[j][1]))
                if (i == mypos):
                    return float('inf')
                mz = maze(i, mypos, nextstate)
                minghost = min(mz, minghost)

            minfood = float('inf')
            if (nextstate.isOnRedTeam(self.index)):
                foodpos = currgameState.getBlueFood().asList()
            else:
                foodpos = currgameState.getRedFood().asList()

            # seperate foods, so two agents would chase different food
            maxf = 0
            minf = currgameState.getInitialLayout().getHeight()
            for f in foodpos:
                maxf = max(maxf, f[1])
                minf = min(minf, f[1])
            avg = (minf + maxf) / 2 + 2
            for i in range(len(foodpos) - 1, -1, -1):
                if foodpos[i][1] > avg:
                    foodpos.pop(i)

            for i in foodpos:
                if i == mypos:
                    return float('inf')
                else:
                    temp = minfood
                    minfood = min(maze(i, mypos, nextstate), minfood)
            return 5 / minfood + 1 / minghost
        else:
            minghost = float('inf')
            for j in range(len(ghosts)):
                i = (int(ghosts[j][0]), int(ghosts[j][1]))
                mz = maze(i, mypos, nextstate)
                if (not currgameState.getAgentState(oppoa[j]).isScared()) and (mz < 2 or i == mypos):
                    return float('-inf')
                elif not currgameState.getAgentState(oppoa[j]).isScared():
                    minghost = min(mz, minghost)
            
            minfood = float('inf')
            if (nextstate.isOnRedTeam(self.index)):
                foodpos = currgameState.getBlueFood().asList()
            else:
                foodpos = currgameState.getRedFood().asList()

            maxf = 0
            minf = currgameState.getInitialLayout().getHeight()
            for f in foodpos:
                maxf = max(maxf, f[1])
                minf = min(minf, f[1])
            avg = (minf + maxf) / 2 + 2
            for i in range(len(foodpos) - 1, -1, -1):
                if foodpos[i][1] > avg:
                    foodpos.pop(i)
            for i in foodpos:
                if i == mypos:
                    return float('inf')
                else:
                    temp = minfood
                    minfood = min(maze(i, mypos, nextstate), minfood)
            return ((currgameState.getInitialLayout().getWidth() + currgameState.getInitialLayout().getHeight()) / minfood - 1 / minghost) * 2 # prefer attack than defend
