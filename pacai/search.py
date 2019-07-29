"""
The base for seach implementations.
"""

import game
import search_student
import util

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

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.
    For any other maze, the sequence of moves will be incorrect, so only use this for tinyMaze.
    """

    s = game.Directions.SOUTH
    w = game.Directions.WEST

    return  [s, s, w, s, w, w, s, w]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

# Abbreviations

breadthFirstSearch = search_student.breadthFirstSearch
bfs = search_student.breadthFirstSearch

depthFirstSearch = search_student.depthFirstSearch
dfs = search_student.depthFirstSearch

aStarSearch = search_student.aStarSearch
astar = search_student.aStarSearch

uniformCostSearch = search_student.uniformCostSearch
ucs = search_student.uniformCostSearch
