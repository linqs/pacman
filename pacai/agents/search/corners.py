from pacai.agents.search.base import SearchAgent
from pacai.core import search
from pacai.student import searchAgents

class AStarCornersAgent(SearchAgent):
    """
    A SearchAgent for CornersProblem using A* and your cornersHeuristic
    """

    def __init__(self, index):
        super().__init__(index)

        self.searchFunction = lambda prob: search.astar(prob, searchAgents.cornersHeuristic)
        self.searchType = searchAgents.CornersProblem
