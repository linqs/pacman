from pacai.agents.base import BaseAgent
from pacai.core.directions import Directions

class GoWestAgent(BaseAgent):
    """
    An agent that goes West until it can't.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getAction(self, state):
        """
        The agent receives a GameState (defined in pacman.py).
        """

        if (Directions.WEST in state.getLegalPacmanActions()):
            return Directions.WEST
        else:
            return Directions.STOP
