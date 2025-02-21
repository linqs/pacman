import random
import time

from pacai.agents.capture.capture import CaptureAgent

DEFAULT_WAIT_DURATION_SECS = 0

class TimeoutAgent(CaptureAgent):
    """
    An agent that always waits a specified duration before making a random move.
    """

    # The duration to wait.
    # Testers may edit this directly (and reset() when done).
    waitMoveDurationSecs = DEFAULT_WAIT_DURATION_SECS
    waitInitDurationSecs = DEFAULT_WAIT_DURATION_SECS

    def reset():
        TimeoutAgent.waitMoveDurationSecs = DEFAULT_WAIT_DURATION_SECS
        TimeoutAgent.waitInitDurationSecs = DEFAULT_WAIT_DURATION_SECS

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, gameState):
        # Wait first.
        time.sleep(TimeoutAgent.waitInitDurationSecs)

        super().registerInitialState(gameState)

    def chooseAction(self, gameState):
        # Wait first.
        time.sleep(TimeoutAgent.waitMoveDurationSecs)

        # Take a random action.
        actions = gameState.getLegalActions(self.index)
        return random.choice(actions)
