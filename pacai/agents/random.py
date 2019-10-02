import random

from pacai.agents.base import BaseAgent

class RandomAgent(BaseAgent):
    """
    An agent that moves randomly while still obeying the rules.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getAction(self, state):
        return random.choice(state.getLegalActions(self.index))
