"""
A heuristic function estimates the cost from the current state to the nearest
goal in the provided `pacai.core.search.problem.SearchProblem`.
"""

from pacai.core import distance

def null(state, problem = None):
    """
    This heuristic is trivial.
    """

    return 0

def manhattan(position, problem):
    """
    This heuristic is the manhattan distance to the goal.
    """

    position1 = position
    position2 = problem.goal

    return distance.manhattan(position1, position2)

def euclidean(position, problem):
    """
    This heuristic is the euclidean distance to the goal.
    """

    position1 = position
    position2 = problem.goal

    return distance.euclidean(position1, position2)

def numFood(state, problem):
    """
    This heuristic is the amount of food left to on the board.
    """

    return state[1].count()
