from pacai.core.search import search
from pacai.core.search.position import PositionSearchProblem

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
    The gameState can be any game state -- Pacman's position in that state is ignored.

    WARNING: bfs must already be implemted in the student package.

    Example usage: distance.maze((2, 4), (5, 6), gameState)
    """

    x1, y1 = position1
    x2, y2 = position2

    walls = gameState.getWalls()
    assert not walls[x1][y1], 'position1 is a wall: ' + position1
    assert not walls[x2][y2], 'position2 is a wall: ' + str(position2)

    prob = PositionSearchProblem(gameState, start = position1, goal = position2, warn = False)

    return len(search.bfs(prob))
