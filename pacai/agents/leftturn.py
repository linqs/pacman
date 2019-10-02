from pacai.agents.base import BaseAgent
from pacai.core.directions import Directions

class LeftTurnAgent(BaseAgent):
    """
    An agent that turns left at every opportunity.
    Three lefts make a right, and two rights (six lefts) don't make a wrong.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().getDirection()
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
