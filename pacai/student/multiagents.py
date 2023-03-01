import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.directions import Directions
from pacai.core.actions import Actions
from pacai.util.queue import Queue
from pacai.core import distance

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        food_list = currentGameState.getFood().asList()
        new_pos = successorGameState.getPacmanPosition()
        new_ghost_states = successorGameState.getGhostStates()
        new_scared_times = [ghostState.getScaredTimer() for ghostState in new_ghost_states]

        for ghost in currentGameState.getGhostStates():
            if(new_pos == ghost.getPosition()):
                return -9999

        # closest food
        closest_food = 65536
        for pos in food_list:
            closest_food = min(closest_food, mht_dis(pos, new_pos))

        closest_ghost = 65536
        for ghost in new_ghost_states:
            closest_ghost = min(closest_ghost, mht_dis(ghost.getPosition(), new_pos))

        res_score = 0
        res_score += 1.0 / (closest_food + 0.1)
        res_score -= 2.0 / (closest_ghost + 0.01)

        res_score += 10.0 / (len(successorGameState.getFood().asList()) + 0.1)
        res_score += 10.0 * sum(1 for non_zero in new_scared_times if non_zero > 0)

        return res_score

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        NumAgents = state.getNumAgents()
        evaluationFunction = self.getEvaluationFunction()

        # recursive func def

        def _minimax(state, depth, cur_agent):
            # terminal
            if(cur_agent == 0):
                depth += 1
            if state.isWin() or state.isLose() or depth > self.getTreeDepth():
                return evaluationFunction(state)
            # max layer, which is the pacman
            if(cur_agent == 0):
                max_res = -float("inf")
                actions = state.getLegalActions(0)
                actions.remove(Directions.STOP)
                for action in actions:
                    max_res = max(max_res,
                    _minimax(state.generateSuccessor(0, action), depth, cur_agent + 1))
                return max_res
            else:
                min_res = float("inf")
                for action in state.getLegalActions(cur_agent):
                    min_res = min(min_res,
                    _minimax(state.generateSuccessor(cur_agent, action),
                             depth, (cur_agent + 1) % NumAgents))
                return min_res
        # wrapper function
        actions = state.getLegalActions(0)
        actions.remove(Directions.STOP)
        evals = [(action, _minimax(state.generateSuccessor(0, action), 0, 1))
                for action in actions]
        return max(evals, key=lambda x: x[1])[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        NumAgents = state.getNumAgents()
        evaluationFunction = self.getEvaluationFunction()

        # recursive func def

        def _minimax(state, depth, cur_agent, a = -float("inf"), b = float("inf")):
            # terminal
            if(cur_agent == 0):
                depth += 1
            if state.isWin() or state.isLose() or depth > self.getTreeDepth():
                return evaluationFunction(state)
            # max layer, which is the pacman
            if(cur_agent == 0):
                actions = state.getLegalActions(0)
                actions.remove(Directions.STOP)
                v = -float("inf")
                for action in actions:
                    v = max(v, _minimax(state.generateSuccessor(0, action),
                                        depth, cur_agent + 1, a, b))
                    if v >= b:
                        return v
                    a = max(a, v)
                return v
            else:
                v = float("inf")
                for action in state.getLegalActions(cur_agent):
                    v = min(v, _minimax(state.generateSuccessor(cur_agent, action),
                                        depth, (cur_agent + 1) % NumAgents, a, b))
                    if v <= a:
                        return v
                    b = min(b, v)
                return v
        # wrapper function
        actions = state.getLegalActions(0)
        actions.remove(Directions.STOP)
        evals = [(action, _minimax(state.generateSuccessor(0, action), 0, 1))
                for action in actions]
        return max(evals, key=lambda x: x[1])[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        NumAgents = state.getNumAgents()
        evaluationFunction = self.getEvaluationFunction()

        # recursive func def

        def _minimax(state, depth, cur_agent):
            if(cur_agent == 0):
                depth += 1
            # terminal
            if state.isWin() or state.isLose() or depth > self.getTreeDepth():
                return evaluationFunction(state)
            # max layer, which is the pacman
            if(cur_agent == 0):
                max_res = -float("inf")
                actions = state.getLegalActions(0)
                actions.remove(Directions.STOP)
                for action in actions:
                    max_res = max(max_res,
                    _minimax(state.generateSuccessor(0, action), depth, cur_agent + 1))
                return max_res
            else:
                numActions = len(state.getLegalActions(cur_agent))
                sum = 0
                for action in state.getLegalActions(cur_agent):
                    sum += _minimax(state.generateSuccessor(cur_agent, action),
                                    depth, (cur_agent + 1) % NumAgents)
                return sum / numActions

        # wrapper function
        actions = state.getLegalActions(0)
        actions.remove(Directions.STOP)
        evals = [(action, _minimax(state.generateSuccessor(0, action), 0, 1))
                for action in actions]
        return max(evals, key=lambda x: x[1])[0]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    # state info
    cur_pos = currentGameState.getPacmanPosition()
    foods_mht = [mht_dis(p, cur_pos) for p in currentGameState.getFood().asList()]
    ghosts = currentGameState.getGhostStates()

    if(len(foods_mht) == 0):
        return 99999

    # weights defind
    FOOD_WEIGHT = 5
    GHOST_WEIGHT = -10
    SCARED_WEIGHT = 30
    THRESHOLD_FOOD = 3
    THRESHOLD_GHOST = 2
    # ==
    score = currentGameState.getScore()
    if(min(foods_mht) >= THRESHOLD_FOOD):
        dis_closest_food = min(foods_mht)
    else:
        dis_closest_food = _bfs(currentGameState)

    for ghost in ghosts:
        if(mht_dis(ghost.getPosition(), cur_pos) >= THRESHOLD_GHOST):
            dst = mht_dis(ghost.getPosition(), cur_pos)
        else:
            dst = distance.maze(cur_pos, (int(ghost.getPosition()[0]),
                int(ghost.getPosition()[1])), currentGameState)

        if(dst > 0):
            if(ghost.getScaredTimer() > 0):
                score += SCARED_WEIGHT / dst
            else:
                score += GHOST_WEIGHT / dst
        else:
            return -9999999
    score += FOOD_WEIGHT / (dis_closest_food + 0.1)
    return score

def _bfs(state):
    visited = set()
    in_frontier = set()
    predecessor = dict()
    frontier_queue = Queue()

    walls = state.getWalls()
    foods = state.getFood()

    visited.add(state.getPacmanPosition())
    for action in Directions.CARDINAL:
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        hitsWall = walls[nextx][nexty]

        if(not hitsWall):
            frontier_queue.push((nextx, nexty))
            in_frontier.add((nextx, nexty))
            predecessor[(nextx, nexty)] = (x, y)

    goal = None
    while (not frontier_queue.isEmpty()):
        cur_pos = frontier_queue.pop()
        visited.add(cur_pos)

        if (foods[cur_pos[0]][cur_pos[1]]):
            goal = cur_pos
            break

        for action in Directions.CARDINAL:
            x, y = cur_pos
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = walls[nextx][nexty]

            if(not hitsWall and not((nextx, nexty) in visited)
               and not((nextx, nexty) in in_frontier)):
                frontier_queue.push((nextx, nexty))
                in_frontier.add((nextx, nexty))
                predecessor[(nextx, nexty)] = (x, y)

    res = []
    if(goal is None):
        return 0
    while (not (goal == state.getPacmanPosition())):
        res.append(goal)
        goal = predecessor[goal]
    return len(res)

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

def mht_dis(pos_0, pos_1):
    return abs(pos_0[0] - pos_1[0]) + abs(pos_0[1] - pos_1[1])
