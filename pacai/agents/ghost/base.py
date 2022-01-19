import abc

from pacai.agents.base import BaseAgent
from pacai.core.directions import Directions
from pacai.util import probability

class GhostAgent(BaseAgent):
    """
    The base class for ghost agents.
    Ghosts provide a distribution of possible actions,
    which is then sampled from to get the next action.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        dist = self.getDistribution(state)

        if (len(dist) == 0):
            return Directions.STOP
        else:
            return probability.sample(dist)

    @abc.abstractmethod
    def getDistribution(self, state):
        """
        Returns a dictionary encoding a distribution over possible actions.
        """

        pass
