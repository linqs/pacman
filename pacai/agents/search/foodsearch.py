from pacai.agents.search.base import SearchAgent
from pacai.core.search import search
from pacai.core.search.food import FoodSearchProblem
from pacai.student import searchAgents

class AStarFoodSearchAgent(SearchAgent):
    """
    A search agent for `pacai.core.search.food.FoodSearchProblem using A*
    and `pacai.student.searchAgents.foodHeuristic`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

        self.searchFunction = lambda prob: search.astar(prob, searchAgents.foodHeuristic)
        self.searchType = FoodSearchProblem
