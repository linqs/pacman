from pacai.agents.base import BaseAgent
from pacai.core.game import Directions
from pacai.util import util

class GhostAgent(BaseAgent):
    def __init__(self, index):
        super().__init__(index)

    def getAction(self, state):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    def getDistribution(self, state):
        """
        Returns a Counter encoding a distribution over actions from the provided state.
        """

        util.raiseNotDefined()
