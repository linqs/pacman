import time

from pacai.agents.random import RandomAgent

DEFAULT_TIMEOUT_SEC = 2

class TimeoutAgent(RandomAgent):
    """
    A random agent that takes too much time.
    Taking too much time results in penalties and random moves.
    """

    def __init__(self, index, timeout = DEFAULT_TIMEOUT_SEC, **kwargs):
        super().__init__(index)

        self._timeout = timeout

    def getAction(self, state):
        time.sleep(self._timeout)

        return super().getAction(state)
