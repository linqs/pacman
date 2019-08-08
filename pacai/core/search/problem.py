from pacai.util import util

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

     util.raiseNotDefined()

  def isGoal(self, state):
     """
     state: Search state

     Returns True if and only if the state is a valid goal state
     """

     util.raiseNotDefined()

  def successorStates(self, state):
     """
     state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """

     util.raiseNotDefined()

  def actionsCost(self, actions):
     """
     actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.
     The sequence must be composed of legal moves.
     """

     util.raiseNotDefined()
