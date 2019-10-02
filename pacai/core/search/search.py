from pacai.core.directions import Directions
from pacai.student import search

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves `tinyMaze`.
    For any other maze, the sequence of moves will be incorrect,
    so only use this for `tinyMaze`.
    """

    s = Directions.SOUTH
    w = Directions.WEST

    return [s, s, w, s, w, w, s, w]

# Abbreviations

breadthFirstSearch = search.breadthFirstSearch
bfs = search.breadthFirstSearch

depthFirstSearch = search.depthFirstSearch
dfs = search.depthFirstSearch

aStarSearch = search.aStarSearch
astar = search.aStarSearch

uniformCostSearch = search.uniformCostSearch
ucs = search.uniformCostSearch
