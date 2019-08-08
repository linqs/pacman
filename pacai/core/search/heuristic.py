from pacai.core import distance

def null(state, problem = None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.
    This heuristic is trivial.
    """

    return 0

def manhattan(position, problem):
    position1 = position
    position2 = problem.goal

    return distance.manhattan(position1, position2)

def euclidean(position, problem):
    position1 = position
    position2 = problem.goal

    return distance.euclidean(position1, position2)

def numFood(state, problem):
    return state[1].count()
