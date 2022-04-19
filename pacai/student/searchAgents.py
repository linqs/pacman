"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""

import logging
import pacai.student.search as search
from pacai.core.actions import Actions
# from pacai.core.search import heuristic
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent
from pacai.core.directions import Directions

class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.
    See the `pacai.core.search.position.PositionSearchProblem` class for an example of
    a working SearchProblem.

    Additional methods to implement:

    `pacai.core.search.problem.SearchProblem.startingState`:
    Returns the start state (in your search space,
    NOT a `pacai.core.gamestate.AbstractGameState`).

    `pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.

    `pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    ```
        successors = []

        for action in Directions.CARDINAL:
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.

        return successors
    ```
    """

    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))
        self._numExpanded = 0
        # *** Your Code Here ***

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """

        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)

    def getExpandedCount(self):
        return self._numExpanded

    def getVisitHistory(self):
        return self._visitHistory

    def isGoal(self, state):
        """
        Answers the question:
        Is this state a goal?

        Returns True if and only if the state is a valid goal state.
        """
        return len(state[1]) == 4
        # if 4 corners in the state then we have reached all corners, only unique corners added

    def startingState(self):
        """
        Answers the question:
        Where should the search start?

        Returns the starting state for the search problem.
        """
        return ((self.startingPosition), ())  # state[1] is the empty tuple of the corners visited
        # search starts at the starting position, also need to know where corners are

    def successorStates(self, state):
        """
        Answers the question:
        What moves are possible from this state?

        Returns a list of tuples with three values:
        (successor state, action, cost of taking the action).
        """
        self._numExpanded += 1
        successors = []
        for action in Directions.CARDINAL:
            if type(state[0]) == tuple:
                x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            if (not hitsWall):
                if type(state[1]) == tuple:  # had to add this to get around a type error
                    visited = list(state[1])  # saving previous states corners visited
                    next_state = (nextx, nexty)  # changing to next state
                    for corner in self.corners:  # for each corner
                        if next_state == corner and next_state not in visited:
                            # if state is a corner and we havent visited this corner
                            visited.append(corner)  # store the visted corner
                    cost = self.actionsCost([action])
                    successors.append(((next_state, tuple(visited)), action, cost))
                    # create the successor and append to the array we are gonna return
        return successors

def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)
    """

    # Useful information.
    # corners = problem.corners  # These are the corner coordinates
    # walls = problem.walls  # These are the walls of the maze, as a Grid.

    # *** Your Code Here ***
    x, y = tuple(state[0])
    man_distances = []
    unvisited = []
    heuristic = 0
    for corner in problem.corners:  # get all unvisited corners
        if corner not in state[1]:
            unvisited.append(corner)
    while len(unvisited) > 0:  # while we haven't visited all the corners
        for corner in unvisited:  # find all the manhattan distances
            man_distances.append((abs(corner[0] - x) + abs(corner[1] - y)))  # manhattan distance
        i = man_distances.index(min(man_distances))  # index of the closest manhattan distance
        heuristic += man_distances[i]  # add to the total distance to visit every corner
        x, y = unvisited.pop(i)  # corner is now visited
        man_distances.clear()  # start over
    return heuristic

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.
    First, try to come up with an admissible heuristic;
    almost all admissible heuristics will be consistent as well.

    If using A* ever finds a solution that is worse than what uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!
    On the other hand, inadmissible or inconsistent heuristics may find optimal solutions,
    so be careful.

    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a
    `pacai.core.grid.Grid` of either True or False.
    You can call `foodGrid.asList()` to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, `problem.walls` gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use.
    For example, if you only want to count the walls once and store that value, try:
    ```
    problem.heuristicInfo['wallCount'] = problem.walls.count()
    ```
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount'].
    """
    position, foodGrid = state
    if type(position) == tuple:  # added to prevent error
        x, y = tuple(position)
        distances = []
        for pellet in foodGrid.asList():  # for each piece of food
            distances.append((abs(pellet[0] - x) + abs(pellet[1] - y)))  # manhattan distance
        if len(distances) != 0:
            return (min(distances) + max(distances)) / 2
            # this is the average distance you are between the closest and farthest piece
    return 0


class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """

        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        return search.aStarSearch(problem, foodHeuristic)  # using a star so we can use heuristic

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem,
    but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.

    The class definition above, `AnyFoodSearchProblem(PositionSearchProblem)`,
    inherits the methods of `pacai.core.search.position.PositionSearchProblem`.

    You can use this search problem to help you fill in
    the `ClosestDotSearchAgent.findPathToClosestDot` method.

    Additional methods to implement:

    `pacai.core.search.position.PositionSearchProblem.isGoal`:
    The state is Pacman's position.
    Fill this in with a goal test that will complete the problem definition.
    """

    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)

        # Store the food for later reference.
        self.food = gameState.getFood()

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """

        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)

    def getExpandedCount(self):
        return self._numExpanded

    def getVisitHistory(self):
        return self._visitHistory

    def isGoal(self, state):
        """
        Answers the question:
        Is this state a goal?

        Returns True if and only if the state is a valid goal state.
        """
        if state in self.food.asList():  # if our state is in the food list then it is food
            return True
        return False

    def startingState(self):
        return self.startState

    def successorStates(self, state):  # copied from position.py
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
            # Note: visit history requires coordinates not states. In this situation
            # they are equivalent.
            coordinates = state
            self._visitHistory.append(coordinates)

        return successors

class ApproximateSearchAgent(BaseAgent):
    """
    Implement your contest entry here.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Get a `pacai.bin.pacman.PacmanGameState`
    and return a `pacai.core.directions.Directions`.

    `pacai.agents.base.BaseAgent.registerInitialState`:
    This method is called before any moves are made.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
