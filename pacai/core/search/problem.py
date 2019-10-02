import abc

class SearchProblem(abc.ABC):
    """
    This class outlines the structure of a search problem.
    Any search problem will need to provide answers to the following questions:
    ```
    Where should the search start?
    Is this state a goal?
    What moves are possible from this state?
    How much did it cost to perform these action?
    ```

    The answers to these questions are provided by implementing
    the abstract methods in this class.

    Note that all the states passed into a `SearchProblem` are also generated
    by the same `SearchProblem`.
    `SearchProblem.startingState` and `SearchProblem.successorStates` produce
    states,
    while `SearchProblem.isGoal` and `SearchProblem.actionsCost` evaluate
    those same states and actions.
    """

    def __init__(self):
        # The number of search nodes we expended.
        self._numExpanded = 0

        # Keep track of the states we have visited.
        # Children are not required to use these,
        # but doing so will allow the GUI to highlight the visited locations.
        self._visitedLocations = set()
        self._visitHistory = []

    @abc.abstractmethod
    def actionsCost(self, actions):
        """
        Answers the question:
        How much did it cost to perform these action?

        Returns the total cost of a particular sequence of legal actions.
        """

        pass

    def getExpandedCount(self):
        return self._numExpanded

    def getVisitHistory(self):
        return self._visitHistory

    @abc.abstractmethod
    def isGoal(self, state):
        """
        Answers the question:
        Is this state a goal?

        Returns True if and only if the state is a valid goal state.
        """

        pass

    @abc.abstractmethod
    def startingState(self):
        """
        Answers the question:
        Where should the search start?

        Returns the starting state for the search problem.
        """

        pass

    @abc.abstractmethod
    def successorStates(self, state):
        """
        Answers the question:
        What moves are possible from this state?

        Returns a list of tuples with three values:
        (successor state, action, cost of taking the action).
        """

        pass
