from pacai.agents.ghost.base import GhostAgent
from pacai.core.actions import Actions
from pacai.core import distance
from pacai.util import counter

class DirectionalGhost(GhostAgent):
    """
    A ghost that prefers to rush Pacman, or flee when scared.
    """

    def __init__(self, index, prob_attack = 0.8, prob_scaredFlee = 0.8, **kwargs):
        super().__init__(index)

        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution(self, state):
        # Read variables from state.
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        pos = state.getGhostPosition(self.index)
        isScared = ghostState.isScared()

        speed = 1
        if (isScared):
            speed = 0.5

        actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
        newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state.
        distancesToPacman = [distance.manhattan(pos, pacmanPosition) for pos in newPositions]
        if (isScared):
            bestScore = max(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack

        zipActions = zip(legalActions, distancesToPacman)
        bestActions = [action for action, distance in zipActions if distance == bestScore]

        # Construct distribution.
        dist = counter.Counter()

        for a in bestActions:
            dist[a] = float(bestProb) / len(bestActions)

        for a in legalActions:
            dist[a] += float(1 - bestProb) / len(legalActions)

        dist.normalize()
        return dist
