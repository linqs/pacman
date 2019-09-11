from pacai.core.game import Actions
from pacai.core.game import Directions
from pacai.core.search.problem import SearchProblem

class _ClosestFoodSearchProblem(SearchProblem):

    """
    A private search problem associated with finding the closest food
    from an initial position on the map.

    Search State: a tuple (x,y) representing the current position in the
    search
    """

    # Search problem requires the initial position to search from, the food
    # and walls on the map
    def __init__(self, initPos, food, walls):
        self._start = initPos
        self._foodGrid = food
        self._walls = walls

    def startingState(self):
        return self._start

    # Goal state is where the current position is at the same location as food
    def isGoal(self, state):
        return self._foodGrid[state[0]][state[1]]

    def successorStates(self, state):
        successors = []
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx) + int(y + dy)
            if not self._walls[nextx][nexty]:
                successors.append((nextx, nexty))
        return successors

    def actionsCost(self, actions):
        x, y = self._start
        cost = 0
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx) + int(y + dy)
            if self._walls[x][y]:
                return 999999
            cost += 1
        return cost
