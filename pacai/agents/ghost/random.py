from pacai.agents.ghost.base import GhostAgent
from pacai.util import probability

class RandomGhost(GhostAgent):
    """
    A ghost that chooses a legal action uniformly at random.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getDistribution(self, state):
        dist = {}
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0

        return probability.normalize(dist)
