"""
Interfaces for capture agents and agent factories
"""

import random
import time

from pacai.agents.base import BaseAgent

class TimeoutAgent(BaseAgent):
    """
    A random agent that takes too much time. Taking
    too much time results in penalties and random moves.
    """

    def __init__(self, index):
        super().__init__(index)

    def getAction(self, state):
        time.sleep(2.0)
        return random.choice(state.getLegalActions(self.index))
