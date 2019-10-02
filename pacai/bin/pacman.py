"""
This file holds the logic for a classic pacman game along with the main code to run a game.

To play your first game, type 'python -m pacai.bin.pacman' from the command line.
Use WASD (or the arrow keys) to move.

Have fun!
"""

import logging
import os
import pickle
import random
import sys

from pacai.agents.base import BaseAgent
from pacai.agents.ghost.random import RandomGhost
from pacai.agents.greedy import GreedyAgent
from pacai.bin.arguments import getParser
from pacai.core.actions import Actions
from pacai.core.directions import Directions
from pacai.core.distance import manhattan
from pacai.core.game import Game
from pacai.core.gamestate import AbstractGameState
from pacai.core.layout import getLayout
from pacai.ui.pacman.null import PacmanNullView
from pacai.ui.pacman.text import PacmanTextView
from pacai.util.logs import initLogging
from pacai.util.logs import updateLoggingLevel
from pacai.util.util import nearestPoint

PACMAN_AGENT_INDEX = 0

SCARED_TIME = 40  # The number of moves that ghosts are scared for.
COLLISION_TOLERANCE = 0.7  # How close ghosts must be to Pacman to kill.

TIME_PENALTY = 1  # Number of points lost each round.
FOOD_POINTS = 10  # Points for eating food.
BOARD_CLEAR_POINTS = 500  # Points for clearning all the food from the board.
GHOST_POINTS = 200  # Points for eating a ghost.
LOSE_POINTS = -500  # Points for getting eatten.

class PacmanGameState(AbstractGameState):
    """
    A game state specific to pacman.
    Note that in classic Pacman, Pacman is always agent PACMAN_AGENT_INDEX.
    """

    def __init__(self, layout):
        super().__init__(layout)

    # Override
    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """

        # Check that successors exist.
        if (self.isOver()):
            raise RuntimeError("Can't generate successors of a terminal state.")

        successor = self._initSuccessor()
        successor._applySuccessorAction(agentIndex, action)

        return successor

    # Override
    def getLegalActions(self, agentIndex = PACMAN_AGENT_INDEX):
        if (self.isOver()):
            return []

        # Pacman's turn.
        if (agentIndex == PACMAN_AGENT_INDEX):
            return PacmanRules.getLegalActions(self)

        return GhostRules.getLegalActions(self, agentIndex)

    def generatePacmanSuccessor(self, action):
        return self.generateSuccessor(PACMAN_AGENT_INDEX, action)

    def getGhostIndexes(self):
        return range(1, self.getNumAgents())

    def getGhostPosition(self, agentIndex):
        if (agentIndex <= PACMAN_AGENT_INDEX or agentIndex >= self.getNumAgents()):
            raise ValueError("Invalid index passed to getGhostPosition(): %d." % (agentIndex))

        return self._agentStates[agentIndex].getPosition()

    def getGhostPositions(self):
        return [ghost.getPosition() for ghost in self.getGhostStates()]

    def getGhostState(self, agentIndex):
        if (agentIndex <= PACMAN_AGENT_INDEX or agentIndex >= self.getNumAgents()):
            raise ValueError("Invalid index passed to getGhostState(): %d." % (agentIndex))

        return self._agentStates[agentIndex]

    def getGhostStates(self):
        return self._agentStates[1:]

    def getLegalPacmanActions(self):
        return self.getLegalActions(PACMAN_AGENT_INDEX)

    def getNumGhosts(self):
        return self.getNumAgents() - 1

    def getPacmanPosition(self):
        return self._agentStates[PACMAN_AGENT_INDEX].getPosition()

    def getPacmanState(self):
        """
        Returns an AgentState object for pacman.

        state.getPosition() gives the current position.
        state.getDirection() gives the travel vector.
        """

        return self._agentStates[PACMAN_AGENT_INDEX]

    def _applySuccessorAction(self, agentIndex, action):
        """
        Apply the action to the context state (self).
        """

        # Let the agent's logic deal with its action's effects on the board.
        if (agentIndex == PACMAN_AGENT_INDEX):
            PacmanRules.applyAction(self, action)
        else:
            GhostRules.applyAction(self, action, agentIndex)

        # Time passes.
        if (agentIndex == PACMAN_AGENT_INDEX):
            # Penalty for waiting around.
            self.addScore(-TIME_PENALTY)
        else:
            GhostRules.decrementTimer(self.getAgentState(agentIndex))

        # Resolve multi-agent effects.
        GhostRules.checkDeath(self, agentIndex)

        # Book keeping.
        self._lastAgentMoved = agentIndex

        self._hash = None

class ClassicGameRules(object):
    """
    These game rules manage the control flow of a game, deciding when
    and how the game starts and ends.
    """

    def __init__(self, timeout = 30):
        self.timeout = timeout

    def newGame(self, layout, pacmanAgent, ghostAgents, display, catchExceptions = False):
        agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
        initState = PacmanGameState(layout)
        game = Game(agents, display, self, catchExceptions = catchExceptions)
        game.state = initState

        self._initialFoodCount = initState.getNumFood()

        return game

    def process(self, state, game):
        """
        Checks to see whether it is time to end the game.
        """

        if (state.isWin()):
            self.win(state, game)
        elif (state.isLose()):
            self.lose(state, game)

    def win(self, state, game):
        logging.info('Pacman emerges victorious! Score: %d' % state.getScore())
        game.gameOver = True

    def lose(self, state, game):
        logging.info('Pacman died! Score: %d' % state.getScore())
        game.gameOver = True

    def agentCrash(self, game, agentIndex):
        if (agentIndex == PACMAN_AGENT_INDEX):
            logging.error('Pacman crashed')
        else:
            logging.error('A ghost crashed')

    def getMaxTotalTime(self, agentIndex):
        return self.timeout

    def getMaxStartupTime(self, agentIndex):
        return self.timeout

    def getMoveWarningTime(self, agentIndex):
        return self.timeout

    def getMoveTimeout(self, agentIndex):
        return self.timeout

    def getMaxTimeWarnings(self, agentIndex):
        return 0

class PacmanRules:
    """
    These functions govern how pacman interacts with his environment under
    the classic game rules.
    """

    PACMAN_SPEED = 1

    @staticmethod
    def getLegalActions(state):
        """
        Returns a list of possible actions.
        """

        agentState = state.getPacmanState()
        return Actions.getPossibleActions(agentState.getPosition(), agentState.getDirection(),
                state.getWalls())

    @staticmethod
    def applyAction(state, action):
        """
        Edits the state to reflect the results of the action.
        """

        legal = PacmanRules.getLegalActions(state)
        if (action not in legal):
            raise ValueError('Illegal pacman action: ' + str(action))

        pacmanState = state.getPacmanState()

        # Update position.
        vector = Actions.directionToVector(action, PacmanRules.PACMAN_SPEED)
        pacmanState.updatePosition(vector)

        # Eat.
        nextPosition = pacmanState.getPosition()
        nearest = nearestPoint(nextPosition)
        if (manhattan(nearest, nextPosition) <= 0.5):
            # Remove food
            PacmanRules.consume(nearest, state)

    @staticmethod
    def consume(position, state):
        x, y = position

        if (state.hasFood(x, y)):
            # Eat food.
            state.eatFood(x, y)
            state.addScore(FOOD_POINTS)

            if (state.getNumFood() == 0 and not state.isLose()):
                state.addScore(BOARD_CLEAR_POINTS)
                state.endGame(True)
        elif (state.hasCapsule(x, y)):
            # Eat a capsule.
            state.eatCapsule(x, y)

            # Reset all ghosts' scared timers.
            for ghostState in state.getGhostStates():
                ghostState.setScaredTimer(SCARED_TIME)

class GhostRules:
    """
    These functions dictate how ghosts interact with their environment.
    """

    GHOST_SPEED = 1.0

    @staticmethod
    def getLegalActions(state, ghostIndex):
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.
        """

        agentState = state.getGhostState(ghostIndex)
        possibleActions = Actions.getPossibleActions(agentState.getPosition(),
                agentState.getDirection(), state.getWalls())
        reverse = Actions.reverseDirection(agentState.getDirection())

        if (Directions.STOP in possibleActions):
            possibleActions.remove(Directions.STOP)

        if (reverse in possibleActions and len(possibleActions) > 1):
            possibleActions.remove(reverse)

        return possibleActions

    @staticmethod
    def applyAction(state, action, ghostIndex):
        legal = GhostRules.getLegalActions(state, ghostIndex)
        if (action not in legal):
            raise ValueError('Illegal ghost action: ' + str(action))

        ghostState = state.getGhostState(ghostIndex)
        speed = GhostRules.GHOST_SPEED
        if (ghostState.isScared()):
            speed /= 2.0

        vector = Actions.directionToVector(action, speed)
        ghostState.updatePosition(vector)

    @staticmethod
    def decrementTimer(agentState):
        if (not agentState.isScared()):
            return

        agentState.decrementScaredTimer()
        if (not agentState.isScared()):
            # If the ghost is done being scared, snap it to the closest point.
            agentState.snapToNearestPoint()

    @staticmethod
    def checkDeath(state, agentIndex):
        pacmanPosition = state.getPacmanPosition()

        # Did pacman just move?
        if (agentIndex == PACMAN_AGENT_INDEX):
            # See if a ghost can kill pacman.
            for index in state.getGhostIndexes():
                ghostState = state.getGhostState(index)
                ghostPosition = ghostState.getPosition()

                if (GhostRules.canKill(pacmanPosition, ghostPosition)):
                    GhostRules.collide(state, ghostState, index)

            return
        else:
            # A ghost just moved.
            ghostState = state.getGhostState(agentIndex)
            ghostPosition = ghostState.getPosition()
            if (GhostRules.canKill(pacmanPosition, ghostPosition)):
                GhostRules.collide(state, ghostState, agentIndex)

    @staticmethod
    def collide(state, ghostState, agentIndex):
        if (ghostState.isScared()):
            # Pacman ate a ghost.
            state.addScore(GHOST_POINTS)
            ghostState.respawn()
        elif (not state.isOver()):
            # A ghost ate pacman.
            state.addScore(LOSE_POINTS)
            state.endGame(False)

    @staticmethod
    def canKill(pacmanPosition, ghostPosition):
        return manhattan(ghostPosition, pacmanPosition) <= COLLISION_TOLERANCE

#############################
# FRAMEWORK TO START A GAME #
#############################

def parseAgentArgs(str):
    if (str is None):
        return {}

    pieces = str.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key, val = p, 1
        opts[key] = val

    return opts

def readCommand(argv):
    """
    Processes the command used to run pacman from the command line.
    """

    description = """
    DESCRIPTION:
        This program will run a classic pacman game. Collect all the pellets before
        the ghosts catch you!

    EXAMPLES:
        (1) python -m pacai.bin.pacman
            - Starts an interactive game.
        (2) python -m pacai.bin.pacman --layout smallClassic
            - Starts an interactive game on a smaller board.
    """

    parser = getParser(description, os.path.basename(__file__))

    parser.add_argument('-g', '--ghosts', dest = 'ghost',
            action = 'store', type = str, default = 'RandomGhost',
            help = 'use the specified ghostAgent module for the ghosts (default: %(default)s)')

    parser.add_argument('-k', '--num-ghosts', dest = 'numGhosts',
            action = 'store', type = int, default = 4,
            help = 'set the maximum number of ghosts (default: %(default)s)')

    parser.add_argument('-l', '--layout', dest = 'layout',
            action = 'store', type = str, default = 'mediumClassic',
            help = 'use the specified map layout (default: %(default)s)')

    parser.add_argument('-p', '--pacman', dest = 'pacman',
            action = 'store', type = str, default = 'WASDKeyboardAgent',
            help = 'use the specified pacmanAgent module for pacman (default: %(default)s)')

    parser.add_argument('--agent-args', dest = 'agentArgs',
            action = 'store', type = str, default = None,
            help = 'comma separated arguments to be passed to agents (e.g. \'opt1=val1,opt2\')'
                + '(default: %(default)s)')

    parser.add_argument('--timeout', dest = 'timeout',
            action = 'store', type = int, default = 30,
            help = 'maximum time limit (seconds) an agent can spend computing per game '
                + '(default: %(default)s)')

    options, otherjunk = parser.parse_known_args(argv)
    args = dict()

    if len(otherjunk) != 0:
        raise ValueError('Unrecognized options: \'%s\'.' % (str(otherjunk)))

    # Set the logging level.
    if options.quiet and options.debug:
        raise ValueError('Logging cannont be set to both debug and quiet.')

    if options.quiet:
        updateLoggingLevel(logging.WARNING)
    elif options.debug:
        updateLoggingLevel(logging.DEBUG)

    # If seed value is not entered generate a random seed value.
    seed = options.seed
    if seed is None:
        seed = random.randint(0, 2**32)
    random.seed(seed)
    logging.debug('Seed value: ' + str(seed))

    # Choose a layout.
    args['layout'] = getLayout(options.layout, maxGhosts = options.numGhosts)
    if (args['layout'] is None):
        raise ValueError('The layout ' + options.layout + ' cannot be found.')

    # Choose a Pacman agent.
    noKeyboard = (options.replay is None and (options.textGraphics or options.nullGraphics))
    if (noKeyboard and ('KeyboardAgent' in options.pacman)):
        raise ValueError('Keyboard agents require graphics.')

    agentOpts = parseAgentArgs(options.agentArgs)
    if options.numTraining > 0:
        args['numTraining'] = options.numTraining
        if 'numTraining' not in agentOpts:
            agentOpts['numTraining'] = options.numTraining

    # Don't display training games.
    if 'numTrain' in agentOpts:
        options.numQuiet = int(agentOpts['numTrain'])
        options.numIgnore = int(agentOpts['numTrain'])

    viewOptions = {
        'gifFPS': options.gifFPS,
        'gifPath': options.gif,
        'skipFrames': options.gifSkipFrames,
        'spritesPath': options.spritesPath,
    }

    # Choose a display format.
    if options.nullGraphics:
        args['display'] = PacmanNullView(**viewOptions)
    elif options.textGraphics:
        args['display'] = PacmanTextView(**viewOptions)
    else:
        # Defer importing the GUI unless we actually need it.
        # This allows people to not have tkinter installed.
        from pacai.ui.pacman.gui import PacmanGUIView

        args['display'] = PacmanGUIView(fps = options.fps, title = 'Pacman', **viewOptions)
        agentOpts['keyboard'] = args['display'].getKeyboard()

    args['catchExceptions'] = options.catchExceptions
    args['gameToReplay'] = options.replay
    args['ghosts'] = [BaseAgent.loadAgent(options.ghost, i + 1) for i in range(options.numGhosts)]
    args['numGames'] = options.numGames
    args['pacman'] = BaseAgent.loadAgent(options.pacman, PACMAN_AGENT_INDEX, agentOpts)
    args['record'] = options.record
    args['timeout'] = options.timeout

    return args

def replayGame(layout, actions, display):
    rules = ClassicGameRules()

    agents = []
    agents.append(GreedyAgent(PACMAN_AGENT_INDEX))
    agents += [RandomGhost(i + 1) for i in range(layout.getNumGhosts())]

    game = rules.newGame(layout, agents[PACMAN_AGENT_INDEX], agents[1:], display)
    state = game.state
    display.initialize(state)

    for action in actions:
        # Execute the action
        state = state.generateSuccessor(*action)

        # Change the display
        display.update(state)

        # Allow for game specific conditions (winning, losing, etc.)
        rules.process(state, game)

    display.finish()

def runGames(layout, pacman, ghosts, display, numGames, record = None, numTraining = 0,
        catchExceptions = False, timeout = 30, **kwargs):
    rules = ClassicGameRules(timeout)
    games = []

    nullView = None
    if (numTraining > 0):
        logging.info('Playing %d training games.' % numTraining)
        nullView = PacmanNullView()

    for i in range(numGames):
        isTraining = (i < numTraining)

        if (isTraining):
            # Suppress graphics for training.
            gameDisplay = nullView
        else:
            gameDisplay = display

        game = rules.newGame(layout, pacman, ghosts, gameDisplay, catchExceptions)
        game.run()

        if (not isTraining):
            games.append(game)

        if (record):
            path = 'pacman.replay'
            if (isinstance(record, str)):
                path = record

            components = {'layout': layout, 'actions': game.moveHistory}
            with open(path, 'wb') as file:
                pickle.dump(components, file)

    if ((numGames - numTraining) > 0):
        scores = [game.state.getScore() for game in games]
        wins = [game.state.isWin() for game in games]
        winRate = wins.count(True) / float(len(wins))
        logging.info('Average Score: %s', sum(scores) / float(len(scores)))
        logging.info('Scores:        %s', ', '.join([str(score) for score in scores]))
        logging.info('Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate))
        logging.info('Record:        %s', ', '.join([['Loss', 'Win'][int(w)] for w in wins]))

    return games

def main(argv):
    """
    Entry point for a pacman game.
    The args are a blind pass of `sys.argv` with the executable stripped.
    """

    initLogging()

    # Get game components based on input
    args = readCommand(argv)

    # Special case: recorded games don't use the runGames method.
    if (args['gameToReplay'] is not None):
        logging.info('Replaying recorded game %s.' % args['gameToReplay'])

        recorded = None
        with open(args['gameToReplay'], 'rb') as file:
            recorded = pickle.load(file)

        recorded['display'] = args['display']
        replayGame(**recorded)

        return

    return runGames(**args)

if __name__ == '__main__':
    main(sys.argv[1:])
