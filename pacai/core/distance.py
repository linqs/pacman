from pacai.core.search.position import PositionSearchProblem
from pacai.student import search

def manhattan(position1, position2):
    """
    Manhattan distance between two position tuples (x, y).
    """

    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

def euclidean(position1, position2):
    """
    Euclidean distance between two position tuples (x, y).
    """

    return ((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2) ** 0.5

def maze(position1, position2, gameState):
    """
    Returns the maze distance between any two positions,
    using the search functions you have already built.

    WARNING: `pacai.student.search.breadthFirstSearch` must already be implemted.

    Example usage: `distance.maze((2, 4), (5, 6), gameState)`.
    """

    x1, y1 = position1
    x2, y2 = position2

    walls = gameState.getWalls()

    if (walls[x1][y1]):
        raise ValueError('Position1 is a wall: ' + str(position1))

    if (walls[x2][y2]):
        raise ValueError('Position2 is a wall: ' + str(position2))

    prob = PositionSearchProblem(gameState, start = position1, goal = position2)

    return len(search.breadthFirstSearch(prob))
