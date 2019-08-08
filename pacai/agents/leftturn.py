from pacai.agents.base import BaseAgent
from pacai.core.game import Directions

class LeftTurnAgent(BaseAgent):
    """
    An agent that turns left at every opportunity
    """

    def __init__(self, index):
        super().__init__(index)

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP:
            current = Directions.NORTH

        left = Directions.LEFT[current]
        if left in legal:
            return left

        if current in legal:
            return current

        if Directions.RIGHT[current] in legal:
            return Directions.RIGHT[current]

        if Directions.LEFT[left] in legal:
            return Directions.LEFT[left]

        return Directions.STOP
