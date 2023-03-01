"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""
import logging
from pacai.core.directions import Directions
from pacai.core.actions import Actions
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent
from pacai.student.search import breadthFirstSearch
from pacai.student.search import uniformCostSearch

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
    # (1, 1), (1, top), (right, 1), (right, top)
    # state: ( (x, y), (if_find, ..., ..., ...) )

    def startingState(self):
        return (self.startingPosition, (False, False, False, False))

    def isGoal(self, state):
        return state[1][0] and state[1][1] and state[1][2] and state[1][3]

    def successorStates(self, state):
        successors = []
        for action in Directions.CARDINAL:
            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            if(not hitsWall):
                idx = 0
                while(idx != 4):
                    if((nextx, nexty) == self.corners[idx]):
                        corners_found = list(state[1])
                        corners_found[idx] = True
                        successors.append((((nextx, nexty), tuple(corners_found)), action, 1))
                        break
                    else:
                        idx += 1
                # not corner:
                if(idx == 4):
                    successors.append((((nextx, nexty), state[1]), action, 1))

        # Bookkeeping for display purposes (the highlight in the GUI).
        self._numExpanded += 1
        if (state not in self._visitedLocations):
            self._visitedLocations.add(state)
            # Note: visit history requires coordinates not states. In this situation
            # they are equivalent.
            coordinates = state[0]
            self._visitHistory.append(coordinates)
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

    # state: ( (x, y), (if_find, ..., ..., ...) )
    cur_x, cur_y = state[0]
    max_mht = -1
    for idx in range(0, 4):
        if(state[1][idx] is False):
            dx, dy = problem.corners[idx]
            cur_mht = abs(dx - cur_x) + abs(dy - cur_y)
            max_mht = max(max_mht, cur_mht)

    return max_mht
    # return heuristic.null(state, problem)  # Default to trivial solution

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
    cur_x, cur_y = position
    x_pos, x_neg, y_pos, y_neg = (0, 0, 0, 0)
    for food_cord in foodGrid.asList():
        dx, dy = (food_cord[0] - cur_x, food_cord[1] - cur_y)
        x_pos = max(x_pos, dx)
        x_neg = min(x_neg, dx)
        y_pos = max(y_pos, dy)
        y_neg = min(y_neg, dy)
    return 2 * (x_pos - x_neg) - max(x_pos, -x_neg) + 2 * (y_pos - y_neg) - max(y_pos, -y_neg)

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
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***

        problem = AnyFoodSearchProblem(gameState)
        return breadthFirstSearch(problem)

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

    def isGoal(self, state):
        cur = state
        return self.food[cur[0]][cur[1]] is True

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
        self._actions = []
        self._actionIndex = 0
        self.searchFunction = uniformCostSearch

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game board.
        Here, we choose a path to the goal.
        In this phase, the agent should compute the path to the goal
        and store it in a local variable.
        All of the work is done in this method!
        """
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            cur_pos = currentState.getPacmanPosition()
            food_list = currentState.getFood().asList()

            closest_positions = [cur_pos, cur_pos, cur_pos, cur_pos]
            counts = [0, 0, 0, 0]

            for food in food_list:
                dx, dy = (food[0] - cur_pos[0], food[1] - cur_pos[1])
                if dx >= 0 and dy >= 0:
                    counts[0] += 1
                    closest_positions[0] = food
                elif dx < 0 and dy >= 0:
                    counts[1] += 1
                    closest_positions[1] = food
                elif dx < 0 and dy < 0:
                    counts[2] += 1
                    closest_positions[2] = food
                elif dx >= 0 and dy < 0:
                    counts[3] += 1
                    closest_positions[3] = food
                else:
                    pass

            if counts[0] == 1:
                nextPathSegment = self.findTo(currentState, closest_positions[0])
            elif counts[1] == 1:
                nextPathSegment = self.findTo(currentState, closest_positions[1])
            elif counts[2] == 1:
                nextPathSegment = self.findTo(currentState, closest_positions[2])
            elif counts[3] == 1:
                nextPathSegment = self.findTo(currentState, closest_positions[3])
            else:
                nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece

            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findTo(self, gameState, cor):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """
        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        problem = SpecificSearchProblem(gameState, cor)
        return uniformCostSearch(problem)

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """
        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        problem = AnyFoodSearchProblem(gameState)
        return uniformCostSearch(problem)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in registerInitialState).
        Return Directions.STOP if there is no further action to take.
        """

        if (self._actionIndex >= (len(self._actions))):
            return Directions.STOP

        action = self._actions[self._actionIndex]
        self._actionIndex += 1

        return action

class SpecificSearchProblem(PositionSearchProblem):
    def __init__(self, gameState, goal, start = None):
        super().__init__(gameState, goal = goal, start = start)

        self._goal = goal

    def isGoal(self, state):
        return state == self._goal

def mht_dis(pos_0, pos_1):
    return abs(pos_0[0] - pos_1[0]) + abs(pos_0[1] - pos_1[1])
