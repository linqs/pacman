import abc

class SearchProblem(abc.ABC):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    @abc.abstractmethod
    def startingState(self):
        """
        Returns the start state for the search problem
        """

        pass

    @abc.abstractmethod
    def isGoal(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """

        pass

    @abc.abstractmethod
    def successorStates(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """

        pass

    @abc.abstractmethod
    def actionsCost(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """

        pass
