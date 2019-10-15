from pacai.core.actions import Actions
from pacai.core.directions import Directions
from pacai.core.search.problem import SearchProblem

class FoodSearchProblem(SearchProblem):
    """
    A search problem associated with finding the a path that collects all of the
    food in a pacman game.

    A search state in this problem is a tuple (pacmanPosition, foodGrid).
    Wwhere pacmanPosition is a tuple (x, y) of integers specifying Pacman's position,
    and foodGrid is a `pacai.core.grid.Grid` of either `True` or `False`,
    specifying remaining food.
    """

    def __init__(self, startingGameState):
        super().__init__()

        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self.heuristicInfo = {}  # A dictionary for the heuristic to store information

    def startingState(self):
        return self.start

    def isGoal(self, state):
        return state[1].count() == 0

    def successorStates(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """

        successors = []
        self._numExpanded += 1
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append((((nextx, nexty), nextFood), direction, 1))

        return successors

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        """

        x, y = self.startingState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1

        return cost
