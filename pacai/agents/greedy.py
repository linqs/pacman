import random

from pacai.agents.base import BaseAgent
from pacai.core.directions import Directions
from pacai.util import reflection

class GreedyAgent(BaseAgent):
    """
    An agent that greedily takes the available move with the best score at the time.
    """

    def __init__(self, index, evalFn = "pacai.core.eval.score", **kwargs):
        super().__init__(index)

        self.evaluationFunction = reflection.qualifiedImport(evalFn)
        assert(self.evaluationFunction is not None)

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if (Directions.STOP in legal):
            legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]

        return random.choice(bestActions)
