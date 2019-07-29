import random

import game
import pacman
import util

class LeftTurnAgent(game.Agent):
    """
    An agent that turns left at every opportunity
    """

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == pacman.Directions.STOP:
            current = pacman.Directions.NORTH

        left = pacman.Directions.LEFT[current]
        if left in legal:
            return left

        if current in legal:
            return current

        if pacman.Directions.RIGHT[current] in legal:
            return pacman.Directions.RIGHT[current]

        if pacman.Directions.LEFT[left] in legal:
            return pacman.Directions.LEFT[left]

        return pacman.Directions.STOP

class GreedyAgent(game.Agent):
    def __init__(self, evalFn = "scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if pacman.Directions.STOP in legal:
            legal.remove(pacman.Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]

        return random.choice(bestActions)

def scoreEvaluation(state):
    return state.getScore()
