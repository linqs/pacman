from pacai.agents.search.base import SearchAgent
from pacai.core.search import search
from pacai.core.search.position import PositionSearchProblem

class StayEastSearchAgent(SearchAgent):
    """
    An agent for `pacai.core.search.position.PositionSearchProblem`
    with a cost function that penalizes being on the West side of the board.

    The cost function for stepping into a position (x, y) is `(1/2)^x`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

        self.searchFunction = search.ucs
        costFn = lambda pos: 0.5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for `pacai.core.search.position.PositionSearchProblem`
    with a cost function that penalizes being on the East side of the board.

    The cost function for stepping into a position (x, y) is `2^x`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

        self.searchFunction = search.ucs
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)
