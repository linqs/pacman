"""
This file contains some of the agents that can be selected to control Pacman.
You will create more agents in pacai/student/searchAgents.py.

To select an agent, use the '-p' option when running pacman.py.
Arguments can be passed to your agent using '-a'.
For example, to load a SearchAgent that uses depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a searchFunction=depthFirstSearch

Commands to invoke other search strategies can be found in the project description.
"""

import time

import pacai.agents.searchAgents
import pacai.core.game
import pacai.core.search
import pacai.student.search
import pacai.util.util

from pacai.agents.base import BaseAgent

class GoWestAgent(BaseAgent):
  """
  An agent that goes West until it can't.
  """

  def __init__(self, index):
    super().__init__(index)

  def getAction(self, state):
    """
    The agent receives a GameState (defined in pacman.py).
    """

    if pacai.core.game.Directions.WEST in state.getLegalPacmanActions():
      return pacai.core.game.Directions.WEST
    else:
      return pacai.core.game.Directions.STOP

class SearchAgent(BaseAgent):
  """
  This very general search agent finds a path using a supplied search algorithm for a
  supplied search problem, then returns actions to follow that path.

  As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)

  Options for fn include:
    depthFirstSearch or dfs
    breadthFirstSearch or bfs


  Note: You should NOT change any code in SearchAgent
  """

  def __init__(self, index, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
    super().__init__(index)

    # Warning: some advanced Python magic is employed below to find the right functions and problems
    # TODO(eriq): Get rid of that "magic".

    # Break circular dependency (other import is for import scoping).
    # TODO(eriq): Remove once this is file is broken up.
    import pacai.student.searchAgents
    import pacai.agents.searchAgents

    # Get the search function from the name and heuristic.
    self.searchFunction = self._fetchSearchFunction(fn, heuristic)

    # Get the search problem type from the name.
    self.searchType = pacai.util.util.fetchModuleAttribute(prob, [pacai.agents.searchAgents, pacai.student.searchAgents])
    print('[SearchAgent] using problem type %s.' % (prob))

  def _fetchSearchFunction(self, functionName, heuristicName):
    """
    Search specific modules for a function matching the given name.
    If that function also takes a heurisitc (i.e. has a parameter called "heuristic"),
    then return a lambda that binds the heuristic.
    """

    # Break circular dependency (other imports are for import scoping).
    # TODO(eriq): Remove once this is file is broken up.
    import pacai.student.searchAgents
    import pacai.agents.searchAgents
    import pacai.core.search
    import pacai.student.search

    # Locate the function.
    function = pacai.util.util.fetchModuleAttribute(functionName, [pacai.core.search, pacai.student.search])

    # Check if the function has a heuristic.
    if 'heuristic' not in function.__code__.co_varnames:
      print('[SearchAgent] using function %s.' % (functionName))
      return function

    # Fetch the heuristic.
    heuristic = pacai.util.util.fetchModuleAttribute(heuristicName, [pacai.core.search, pacai.student.search, pacai.agents.searchAgents, pacai.student.searchAgents])
    print('[SearchAgent] using function %s and heuristic %s.' % (functionName, heuristicName))

    # Bind the heuristic.
    return lambda x: function(x, heuristic=heuristic)

  def registerInitialState(self, state):
    """
    This is the first time that the agent sees the layout of the game board. Here, we
    choose a path to the goal.  In this phase, the agent should compute the path to the
    goal and store it in a local variable.  All of the work is done in this method!

    state: a GameState object (pacman.py)
    """

    if self.searchFunction == None:
      raise Exception("No search function provided for SearchAgent")

    starttime = time.time()
    problem = self.searchType(state) # Makes a new search problem
    self.actions  = self.searchFunction(problem) # Find a path
    totalCost = problem.actionsCost(self.actions)

    print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
    if '_expanded' in dir(problem):
      print('Search nodes expanded: %d' % problem._expanded)

  def getAction(self, state):
    """
    Returns the next action in the path chosen earlier (in registerInitialState).  Return
    pacai.core.game.Directions.STOP if there is no further action to take.

    state: a GameState object (pacman.py)
    """

    if 'actionIndex' not in dir(self):
      self.actionIndex = 0

    i = self.actionIndex
    self.actionIndex += 1
    if i < len(self.actions):
      return self.actions[i]
    else:
      return pacai.core.game.Directions.STOP

class PositionSearchProblem(pacai.core.search.SearchProblem):
  """
  A search problem defines the state space, start state, goal test,
  successor function and cost function.  This search problem can be
  used to find paths to a particular point on the pacman board.

  The state space consists of (x,y) positions in a pacman game.

  Note: this search problem is fully specified; you should NOT change it.
  """

  def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True):
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

    if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
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
    for action in [pacai.core.game.Directions.NORTH, pacai.core.game.Directions.SOUTH, pacai.core.game.Directions.EAST, pacai.core.game.Directions.WEST]:
      x,y = state
      dx, dy = pacai.core.game.Actions.directionToVector(action)
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
    Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999
    """

    if actions == None:
      return 999999

    x,y= self.startingState()
    cost = 0
    for action in actions:
      # Check figure out the next state and see whether its' legal
      dx, dy = pacai.core.game.Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]:
        return 999999
      cost += self.costFn((x,y))
    return cost

class StayEastSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes being in
  positions on the West side of the board.

  The cost function for stepping into a position (x,y) is 1/2^x.
  """

  def __init__(self, index):
      super().__init__(index)

      self.searchFunction = pacai.core.search.ucs
      costFn = lambda pos: 0.5 ** pos[0]
      self.searchType = lambda state: PositionSearchProblem(state, costFn)

class StayWestSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes being in
  positions on the East side of the board.

  The cost function for stepping into a position (x,y) is 2^x.
  """

  def __init__(self, index):
      super().__init__(index)

      self.searchFunction = pacai.core.search.ucs
      costFn = lambda pos: 2 ** pos[0]
      self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
  """
  The Manhattan distance heuristic for a PositionSearchProblem
  """

  xy1 = position
  xy2 = problem.goal
  return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
  """
  The Euclidean distance heuristic for a PositionSearchProblem
  """

  xy1 = position
  xy2 = problem.goal
  return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5

class AStarCornersAgent(SearchAgent):
  """
  A SearchAgent for CornersProblem using A* and your cornersHeuristic
  """

  def __init__(self, index):
    super().__init__(index)

    # Break circular dependency.
    # TODO(eriq): Remove once this is file is broken up.
    import pacai.student.searchAgents

    self.searchFunction = lambda prob: pacai.core.search.astar(prob, pacai.student.searchAgents.cornersHeuristic)
    self.searchType = pacai.student.searchAgents.CornersProblem

class FoodSearchProblem(pacai.core.search.SearchProblem):
  """
  A search problem associated with finding the a path that collects all of the
  food (dots) in a Pacman game.

  A search state in this problem is a tuple (pacmanPosition, foodGrid) where
    pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
    foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
  """

  def __init__(self, startingGameState):
    self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
    self.walls = startingGameState.getWalls()
    self.startingGameState = startingGameState
    self._expanded = 0
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
    self._expanded += 1
    for direction in [pacai.core.game.Directions.NORTH, pacai.core.game.Directions.SOUTH, pacai.core.game.Directions.EAST, pacai.core.game.Directions.WEST]:
      x,y = state[0]
      dx, dy = pacai.core.game.Actions.directionToVector(direction)
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
      dx, dy = pacai.core.game.Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]:
        return 999999
      cost += 1
    return cost

class AStarFoodSearchAgent(SearchAgent):
  """
  A SearchAgent for FoodSearchProblem using A* and your foodHeuristic
  """

  def __init__(self, index):
    super().__init__(index)

    # Break circular dependency.
    # TODO(eriq): Remove once this is file is broken up.
    import pacai.student.searchAgents

    self.searchFunction = lambda prob: pacai.core.search.astar(prob, pacai.student.searchAgents.foodHeuristic)
    self.searchType = FoodSearchProblem

def numFoodHeuristic(state, problem):
  return state[1].count()

def mazeDistance(point1, point2, gameState):
  """
  Returns the maze distance between any two points, using the search functions
  you have already built.  The gameState can be any game state -- Pacman's position
  in that state is ignored.

  Example usage: mazeDistance( (2,4), (5,6), gameState)

  This might be a useful helper function for your ApproximateSearchAgent.
  """

  x1, y1 = point1
  x2, y2 = point2
  walls = gameState.getWalls()
  assert not walls[x1][y1], 'point1 is a wall: ' + point1
  assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
  prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False)

  return len(pacai.core.search.bfs(prob))
