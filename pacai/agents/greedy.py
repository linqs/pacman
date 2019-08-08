import random

from pacai.agents.base import BaseAgent
from pacai.core.game import Directions
from pacai.util import util

class GreedyAgent(BaseAgent):
    def __init__(self, index, evalFn = "pacai.core.eval.score"):
        super().__init__(index)

        self.evaluationFunction = util.qualifiedImport(evalFn)
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]

        return random.choice(bestActions)
