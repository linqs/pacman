from pacai.agents.base import BaseAgent
from pacai.util import reflection

class MultiAgentSearchAgent(BaseAgent):
    """
    A common class for all multi-agent searchers.
    """

    def __init__(self, index, evalFn = 'pacai.core.eval.score', depth = 2, **kwargs):
        super().__init__(index)

        self.evaluationFunction = reflection.qualifiedImport(evalFn)
        self.treeDepth = int(depth)
