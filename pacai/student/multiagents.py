import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent

from pacai.core.distance import manhattan

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
        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        # newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]
        position = currentGameState.getPacmanPosition()

        # *** Your Code Here ***
        score = 0
        ghosts = []
        for ghost in newGhostStates:  # get the positions of ghosts
            ghost_coords = ghost.getPosition()
            ghosts.append((ghost_coords[0], ghost_coords[1]))
        for ghost in ghosts:
            if manhattan(ghost, newPosition) > manhattan(ghost, position):
                x = manhattan(ghost, newPosition)
                score += 25 - x   # if ghost is farther away, moving away from ghost = less valuable
        closest = oldFood.asList()[0]
        closest_distance = manhattan(closest, newPosition)
        for food in oldFood.asList():  # find closest food
            if manhattan(food, currentGameState.getPacmanPosition()) < closest_distance:
                closest_distance = manhattan(food, newPosition)
                closest = food
        if manhattan(closest, newPosition) < manhattan(closest, position):
            # if we get closer to the closest food thent he previous state, reward pacman
            score += 20
        return score

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

    def getAction(self, gameState):

        def helper(state, agent, depth):
            # -----------setup-----------
            if depth == self.getTreeDepth() or state.isWin() or state.isLose():
                # If the state is a terminal state: return the state’s utility
                return self.getEvaluationFunction()(state)
            minimum = float("inf")
            maximum = float("-inf")
            next_agent = agent + 1
            if next_agent == gameState.getNumAgents():
                # generalization needed to make alpha beta pseudocode from lecture work for pacman
                next_agent = 0
                depth += 1  # if last ghost we are going to go back to pacman and go to a new depth
            # -----------setup-----------

            # -----------MAX-VALUE-----------
            if agent == 0:  # its pacman, we have reached a max layer
                actions = state.getLegalActions(agent)
                if "Stop" in actions:
                    actions.remove("Stop")
                for action in actions:  # for each successor of state
                    successor = state.generateSuccessor(agent, action)  # compute value(successor)
                    maximum = max(maximum, helper(successor, next_agent, depth))
                    # update max accordingly
                    # update max with max of curr value and value of min of next agent at same depth
                    # v <- Max(v, MIN-VALUE(Result(s,a)))
                return maximum  # If the next agent is MAX: return max-value(state)
            # -----------MAX-VALUE-----------

            # -----------MIN-VALUE-----------
            else:  # if there are more ghosts to go, keep calling min layers
                actions = state.getLegalActions(agent)
                for action in actions:  # for each successor of state
                    successor = state.generateSuccessor(agent, action)  # compute value(successor)
                    minimum = min(minimum, helper(successor, next_agent, depth))
                    # update min accordingly
                    # update min with min of curr value and value of min/max of next agent at =depth
                    # v <- Min(v, MAX-VALUE(Result(s,a)))
                return minimum  # If the next agent is MIN: return min-value(state)
            # -----------MIN-VALUE-----------

        actions_outcomes = []
        best_moves = []
        actions = gameState.getLegalActions(0)  # all of pacmans actions from the start is root node
        actions.remove("Stop")
        for action in actions:
            actions_outcomes.append(helper(gameState.generateSuccessor(0, action), 1, 0))
            # for each valid state from pacmans start state start a branch
        i = 0
        for outcome in actions_outcomes:
            # need to randomize the action taken if there is a tie
            # for the best action so it doesnt get stuck and do the same thing over and over
            if outcome == max(actions_outcomes):
                best_moves.append(actions[i])
            i += 1
        return best_moves[random.randint(0, len(best_moves) - 1)]
        # return actions[actions_outcomes.index(max(actions_outcomes))]

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

    def getAction(self, gameState):

        def helper(state, agent, depth, alpha, beta):
            # -----------setup-----------
            if depth == self.getTreeDepth() or state.isWin() or state.isLose():
                # If the state is a terminal state: return the state’s utility
                return self.getEvaluationFunction()(state)
            minimum = float("inf")
            maximum = float("-inf")
            next_agent = agent + 1
            if next_agent == gameState.getNumAgents():
                # generalization needed to make alpha beta pseudocode from lecture work for pacman
                next_agent = 0
                depth += 1
                # if its the last ghost we are going to go back to pacman and go to a new depth
            # -----------setup-----------

            # -----------MAX-VALUE-----------
            if agent == 0:  # its pacman, we have reached a max layer
                actions = state.getLegalActions(agent)
                if "Stop" in actions:
                    actions.remove("Stop")
                for action in actions:  # for each successor of state
                    successor = state.generateSuccessor(agent, action)  # compute value(successor)
                    maximum = max(maximum, helper(successor, next_agent, depth, alpha, beta))
                    # update max accordingly
                    # update max with max of curr value and value of min of next agent at same depth
                    # v <- Max(v, MIN-VALUE(Result(s,a), alpha, beta))
                    if maximum >= beta:  # if v >= beta then return v
                        return maximum
                    alpha = max(alpha, maximum)  # alpha <- Max(alpha, v)
                return maximum  # If the next agent is MAX: return max-value(state)
            # -----------MAX-VALUE-----------

            # -----------MIN-VALUE-----------
            else:  # if there are more ghosts to go, keep calling min layers
                actions = state.getLegalActions(agent)
                for action in actions:  # for each successor of state
                    successor = state.generateSuccessor(agent, action)  # compute value(successor)
                    minimum = min(minimum, helper(successor, next_agent, depth, alpha, beta))
                    # update min accordingly
                    # update max with max of curr value and value of min/max of next agent at =depth
                    # v <- Min(v, MAX-VALUE(Result(s,a), alpha, beta))
                    if minimum <= alpha:  # if v <= alpha then return v
                        return minimum
                    beta = min(beta, minimum)  # # beta <- Min(beta, v)
                return minimum  # If the next agent is MIN: return min-value(state)
            # -----------MIN-VALUE-----------

        actions_outcomes = []
        best_moves = []
        actions = gameState.getLegalActions(0)  # all of pacmans actions from the start is root node
        actions.remove("Stop")
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            actions_outcomes.append(helper(successor, 1, 0, float("-inf"), float("inf")))
            # for each valid state from pacmans start state start a branch
        i = 0
        for outcome in actions_outcomes:
            # need to randomize the action taken if there is a tie
            # for the best action so it doesnt get stuck and do the same thing over and over
            if outcome == max(actions_outcomes):
                best_moves.append(actions[i])
            i += 1
        return best_moves[random.randint(0, len(best_moves) - 1)]
        # return actions[actions_outcomes.index(max(actions_outcomes))]

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

    def getAction(self, gameState):

        def helper(state, agent, depth):
            # -----------setup-----------
            if depth == self.getTreeDepth() or state.isWin() or state.isLose():
                # If the state is a terminal state: return the state’s utility
                return self.getEvaluationFunction()(state)
            total = 0
            maximum = float("-inf")
            next_agent = agent + 1
            if next_agent == gameState.getNumAgents():
                # generalization needed to make alphabeta pseudocode from lecture work for pacman
                next_agent = 0
                depth += 1
                # if its the last ghost we are going to go back to pacman and go to a new depth
            # -----------setup-----------

            # -----------MAX-VALUE-----------
            if agent == 0:  # its pacman, we have reached a max layer
                actions = state.getLegalActions(agent)
                if "Stop" in actions:
                    actions.remove("Stop")
                for action in actions:  # for each successor of state
                    successor = state.generateSuccessor(agent, action)  # compute value(successor)
                    maximum = max(maximum, helper(successor, next_agent, depth))
                    # update max accordingly
                    # update max with max of curr value and value of min of next agent at same depth
                return maximum  # If the next agent is MAX: return max-value(state)
            # -----------MAX-VALUE-----------

            # ------------expValue-----------
            else:  # if there are more ghosts to go, keep calling exp layers
                actions = state.getLegalActions(agent)
                for action in actions:  # for each successor of state average
                    successor = state.generateSuccessor(agent, action)  # compute value(successor)
                    total = total + helper(successor, next_agent, depth)
                    # update total accordingly
                    # sum of past moves and this move
                return total / len(actions)  # sum of past moves / total moves
            # -----------MIN-VALUE-----------

        actions_outcomes = []
        best_moves = []
        actions = gameState.getLegalActions(0)
        # all of pacmans actions from the start is the root node
        actions.remove("Stop")
        for action in actions:
            actions_outcomes.append(helper(gameState.generateSuccessor(0, action), 1, 0))
            # for each valid state from pacmans start state start a branch
        i = 0
        for outcome in actions_outcomes:
            # need to randomize the action taken if there is a tie
            # for the best action so it doesnt get stuck and do the same thing over and over
            if outcome == max(actions_outcomes):
                best_moves.append(actions[i])
            i += 1
        return best_moves[random.randint(0, len(best_moves) - 1)]
        # return actions[actions_outcomes.index(max(actions_outcomes))]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: for each ghost, if there is still a reasonable amount of time on the scared timer,
    reward pacman, otherwise penalize pacman for being close to a ghost.
    Add the inverse of the distance to the closest food so pacman is rewarded for being closer
    """
    total = 0
    ghosts = currentGameState.getGhostStates()
    position = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    foods_list = []
    scared = -1  # distance to ghost will detract from score
    # print("---------------")
    for ghost in ghosts:
        if ghost.getScaredTimer() > 5:
            scared = 1
        total += (1 / (manhattan(position, ghost.getPosition()) + .01)) * scared
        # distance from the ghost is good if it isnt scared otherwise its bad
        scared = -1

    for food in foods:
        foods_list.append(manhattan(position, food))
    # print("food modifier: " + str(1 / min(foods_list) * 10))
    total += 1 / min(foods_list)
    # print(food)
    # print("---------------")

    return total + currentGameState.getScore()

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
