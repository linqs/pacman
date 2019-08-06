"""
Interfaces for capture agents and agent factories
"""

import random

from pacai.agents.agent import Agent

class RandomAgent(Agent):
    """
    A random agent that abides by the rules.
    """

    def __init__(self, index):
        super().__init__(index)

    def getAction(self, state):
        return random.choice(state.getLegalActions(self.index))
