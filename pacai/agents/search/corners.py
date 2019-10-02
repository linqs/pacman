from pacai.agents.search.base import SearchAgent
from pacai.core.search import search
from pacai.student import searchAgents

class AStarCornersAgent(SearchAgent):
    """
    A search agent for `pacai.student.searchAgents.CornersProblem` using A*
    and `pacai.student.searchAgents.cornersHeuristic`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

        self.searchFunction = lambda prob: search.astar(prob, searchAgents.cornersHeuristic)
        self.searchType = searchAgents.CornersProblem
