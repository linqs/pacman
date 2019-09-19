import logging
import time

from pacai.agents.base import BaseAgent
from pacai.core.directions import Directions
from pacai.util import reflection

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

    # TODO(eriq): We should pass actual objects instead of strings.
    def __init__(self, index, fn = 'pacai.core.search.search.dfs',
            prob = 'pacai.core.search.position.PositionSearchProblem',
            heuristic = 'pacai.core.search.heuristic.null'):
        super().__init__(index)
        # Get the search problem type from the name.
        self.searchType = reflection.qualifiedImport(prob)
        logging.info('[SearchAgent] using problem type %s.' % (prob))

        # Get the search function from the name and heuristic.
        self.searchFunction = self._fetchSearchFunction(fn, heuristic)

    def _fetchSearchFunction(self, functionName, heuristicName):
        """
        Search specific modules for a function matching the given name.
        If that function also takes a heurisitc (i.e. has a parameter called "heuristic"),
        then return a lambda that binds the heuristic.
        """

        # Locate the function.
        function = reflection.qualifiedImport(functionName)

        # Check if the function has a heuristic.
        if 'heuristic' not in function.__code__.co_varnames:
            logging.info('[SearchAgent] using function %s.' % (functionName))
            return function

        # Fetch the heuristic.
        heuristic = reflection.qualifiedImport(heuristicName)
        logging.info('[SearchAgent] using function %s and heuristic %s.' %
                (functionName, heuristicName))

        # Bind the heuristic.
        return lambda x: function(x, heuristic = heuristic)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game board. Here, we
        choose a path to the goal. In this phase, the agent should compute the path to the
        goal and store it in a local variable. All of the work is done in this method!

        state: a GameState object (pacman.py)
        """

        if (self.searchFunction is None):
            raise Exception('No search function provided for SearchAgent')

        starttime = time.time()
        problem = self.searchType(state)  # Makes a new search problem
        self.actions = self.searchFunction(problem)  # Find a path
        totalCost = problem.actionsCost(self.actions)

        logging.info('Path found with total cost of %d in %.1f seconds' %
                (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem):
            logging.info('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in registerInitialState).
        Return Directions.STOP if there is no further action to take.

        state: a GameState object (pacman.py)
        """

        if 'actionIndex' not in dir(self):
            self.actionIndex = 0

        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]

        return Directions.STOP
