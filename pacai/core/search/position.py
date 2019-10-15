from pacai.core.actions import Actions
from pacai.core.directions import Directions
from pacai.core.search.problem import SearchProblem

DEFAULT_COST_FUNCTION = lambda x: 1
DEFAULT_GOAL_POSITION = (1, 1)

class PositionSearchProblem(SearchProblem):
    """
    A `pacai.core.search.problem.SearchProblem` for finding a specific location on the board.
    The state space consists of (x, y) positions.

    Note that this search problem is fully specified and should be used as an example.
    """
    def __init__(self, gameState, costFn = DEFAULT_COST_FUNCTION,
            goal = DEFAULT_GOAL_POSITION, start = None):
        """
        Args:
            gameState: A `pacai.core.gamestate.AbstractGameState`.
            costFn: A function from a search state (x, y) to a non-negative number.
            goal: The target position.
        """

        super().__init__()

        self.walls = gameState.getWalls()
        self.goal = goal
        self.costFn = costFn

        self.startState = start
        if (self.startState is None):
            self.startState = gameState.getAgentPosition(0)

        if (self.startState is None):
            raise ValueError("Could not find starting location.")

    def startingState(self):
        return self.startState

    def isGoal(self, state):
        if (state != self.goal):
            return False

        # Register the locations we have visited.
        # This allows the GUI to highlight them.
        self._visitedLocations.add(state)
        self._visitHistory.append(state)

        return True

    def successorStates(self, state):
        """
        Returns successor states, the actions they require, and a constant cost of 1.
        """

        successors = []

        for action in Directions.CARDINAL:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)

            if (not self.walls[nextx][nexty]):
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)

                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes (the highlight in the GUI).
        self._numExpanded += 1
        if (state not in self._visitedLocations):
            self._visitedLocations.add(state)
            self._visitHistory.append(state)

        return successors

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        """

        if (actions is None):
            return 999999

        x, y = self.startingState()
        cost = 0

        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if (self.walls[x][y]):
                return 999999

            cost += self.costFn((x, y))

        return cost
