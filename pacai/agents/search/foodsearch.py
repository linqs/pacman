from pacai.agents.search.base import SearchAgent
from pacai.core.search import search
from pacai.core.search.food import FoodSearchProblem
from pacai.student import searchAgents

class AStarFoodSearchAgent(SearchAgent):
    """
    A SearchAgent for FoodSearchProblem using A* and your foodHeuristic
    """

    def __init__(self, index):
        super().__init__(index)

        self.searchFunction = lambda prob: search.astar(prob, searchAgents.foodHeuristic)
        self.searchType = FoodSearchProblem
