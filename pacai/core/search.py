"""
The base for seach implementations.
"""

import pacai.student.search
import pacai.util.util

from pacai.core.game import Actions
from pacai.core.game import Directions

# TODO(eriq): Break this file up into its own package.

class SearchProblem(object):
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def startingState(self):
     """
     Returns the start state for the search problem
     """

     pacai.util.util.raiseNotDefined()

  def isGoal(self, state):
     """
     state: Search state

     Returns True if and only if the state is a valid goal state
     """

     pacai.util.util.raiseNotDefined()

  def successorStates(self, state):
     """
     state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """

     pacai.util.util.raiseNotDefined()

  def actionsCost(self, actions):
     """
     actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.
     The sequence must be composed of legal moves.
     """

     pacai.util.util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.
    For any other maze, the sequence of moves will be incorrect, so only use this for tinyMaze.
    """

    s = Directions.SOUTH
    w = Directions.WEST

    return  [s, s, w, s, w, w, s, w]

class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test,
    successor function and cost function. This search problem can be
    used to find paths to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1, 1), start = None, warn = True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """

        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start is not None:
            self.startState = start
        self.goal = goal
        self.costFn = costFn

        if (warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal))):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def startingState(self):
        return self.startState

    def isGoal(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def successorStates(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

        As noted in search.py:
        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999
        """

        if actions == None:
            return 999999

        x, y = self.startingState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += self.costFn((x,y))

        return cost

class FoodSearchProblem(SearchProblem):
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple (pacmanPosition, foodGrid) where
        pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
        foodGrid: a Grid (see game.py) of either True or False, specifying remaining food
    """

    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def startingState(self):
        return self.start

    def isGoal(self, state):
        return state[1].count() == 0

    def successorStates(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """

        successors = []
        self._expanded += 1
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
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
        If those actions include an illegal move, return 999999
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

# Abbreviations
# TODO(eriq): Remove these.

breadthFirstSearch = pacai.student.search.breadthFirstSearch
bfs = pacai.student.search.breadthFirstSearch

depthFirstSearch = pacai.student.search.depthFirstSearch
dfs = pacai.student.search.depthFirstSearch

aStarSearch = pacai.student.search.aStarSearch
astar = pacai.student.search.aStarSearch

uniformCostSearch = pacai.student.search.uniformCostSearch
ucs = pacai.student.search.uniformCostSearch
