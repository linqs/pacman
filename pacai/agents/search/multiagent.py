from pacai.agents.base import BaseAgent
from pacai.util import reflection

class MultiAgentSearchAgent(BaseAgent):
    """
    This class provides some common elements to all of your multi-agent searchers.
    Any methods defined here will be available to the
    MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.
    Please do not remove anything, however.
    """

    def __init__(self, index, evalFn = 'pacai.core.eval.score', depth = '2'):
        super().__init__(index)

        self.evaluationFunction = reflection.qualifiedImport(evalFn)
        self.treeDepth = int(depth)
