import logging
import time

from pacai.agents.base import BaseAgent
from pacai.core.directions import Directions
from pacai.util import reflection

class SearchAgent(BaseAgent):
    """
    A general search agent that finds a path using a supplied search algorithm for a
    supplied search problem,
    then returns actions to follow that path.

    As a default, this agent runs `pacai.student.search.depthFirstSearch` on a
    `pacai.core.search.position.PositionSearchProblem` to find location (1, 1).
    """

    def __init__(self, index,
            fn = 'pacai.student.search.depthFirstSearch',
            prob = 'pacai.core.search.position.PositionSearchProblem',
            heuristic = 'pacai.core.search.heuristic.null',
            **kwargs):
        super().__init__(index)

        # Get the search problem type from the name.
        self.searchType = reflection.qualifiedImport(prob)
        logging.info('[SearchAgent] using problem type %s.' % (prob))

        # Get the search function from the name and heuristic.
        self.searchFunction = self._fetchSearchFunction(fn, heuristic)

        # The actions the search produced.
        self._actions = []

        # The currentl action (from self._actions) that the agent is performing.
        self._actionIndex = 0

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game board.
        Here, we choose a path to the goal.
        In this phase, the agent should compute the path to the goal
        and store it in a local variable.
        All of the work is done in this method!
        """

        if (self.searchFunction is None):
            raise Exception('No search function provided for SearchAgent.')

        starttime = time.time()
        problem = self.searchType(state)  # Makes a new search problem.

        self._actions = self.searchFunction(problem)  # Find a path.
        self._actionIndex = 0

        totalCost = problem.actionsCost(self._actions)

        state.setHighlightLocations(problem.getVisitHistory())

        logging.info('Path found with total cost of %d in %.1f seconds' %
                (totalCost, time.time() - starttime))

        logging.info('Search nodes expanded: %d' % problem.getExpandedCount())

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

    def _fetchSearchFunction(self, functionName, heuristicName):
        """
        Get the specified search function by name.
        If that function also takes a heurisitc (i.e. has a parameter called "heuristic"),
        then return a lambda that binds the heuristic to the function.
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
