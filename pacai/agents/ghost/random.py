from pacai.agents.ghost.base import GhostAgent
from pacai.util import containers

class RandomGhost(GhostAgent):
    """
    A ghost that chooses a legal action uniformly at random.
    """

    def __init__(self, index):
        super().__init__(index)

    def getDistribution(self, state):
        dist = containers.Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist
