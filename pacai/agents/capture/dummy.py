import random

from pacai.agents.capture.capture import CaptureAgent

class DummyAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at pacai.core.baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 15 seconds.
        """

        """
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState.
        """

        CaptureAgent.registerInitialState(self, gameState)

        """
        Your initialization code goes here, if you need any.
        """

    def chooseAction(self, gameState):
        """
        Picks among actions randomly.
        """
        actions = gameState.getLegalActions(self.index)

        """
        You should change this in your own agent.
        """

        return random.choice(actions)
