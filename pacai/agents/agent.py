class Agent(object):
    """
    An agent is something in the pacman world that does something (takes some action).
    Could be a ghost, the player controller Pac-Man, an AI controlling Pac-Man, etc.

    An agent must define the getAction method,
    but may also override any of the other methods.
    """

    def __init__(self, index = 0):
        self.index = index

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """

        pacai.util.raiseNotDefined()

    def registerInitialState(self, state):
        """
        Inspect the starting state.
        """

        pass

    def observationFunction(self, state):
        """
        Make an observation on the state of the game.
        """

        return state.deepCopy()

    def final(self, state):
        """
        Inform the agent about the result of a game.
        """

        pass
