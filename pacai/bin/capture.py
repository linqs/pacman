"""
Capture is a variant of pacman where two teams face off.
The goal is to eat more food than your opponent.
On your side of the map, you are a ghost and can eat pacmen.
On your opponents side of the map, you are a pacman and can eat food and capsules.
"""

import logging
import os
import pickle
import random
import sys

from pacai.agents import keyboard
from pacai.agents.capture.dummy import DummyAgent
from pacai.bin.arguments import getParser
from pacai.core.actions import Actions
from pacai.core.distance import manhattan
from pacai.core.game import Game
from pacai.core.gamestate import AbstractGameState
from pacai.core.grid import Grid
from pacai.core.layout import Layout
from pacai.core.layout import getLayout
from pacai.ui.capture.null import CaptureNullView
from pacai.ui.capture.text import CaptureTextView
from pacai.util import reflection
from pacai.util.logs import initLogging
from pacai.util.logs import updateLoggingLevel
from pacai.util.mazeGenerator import generateMaze
from pacai.util.util import nearestPoint

COLLISION_TOLERANCE = 0.7  # How close ghosts must be to Pacman to kill

KILL_POINTS = 0
FOOD_POINTS = 1  # Points for eating food.

MIN_FOOD = 2

SCARED_TIME = 40

class CaptureGameState(AbstractGameState):
    """
    A game state specific to capture.
    """

    def __init__(self, layout, timeleft):
        super().__init__(layout)

        self._timeleft = timeleft

        # The index of agents on each team.
        self._blueTeam = []
        self._redTeam = []

        # Matches indexes with getAgentStates().
        # True if the agent is on the red team, false otherwise.
        self._teams = []

        for agentIndex in range(self.getNumAgents()):
            agentState = self.getAgentState(agentIndex)
            agentIsRed = self.isOnRedSide(agentState.getPosition())

            self._teams.append(agentIsRed)

            if (agentIsRed):
                self._redTeam.append(agentIndex)
            else:
                self._blueTeam.append(agentIndex)

        # Build some denormalized structures for fast access.

        self._redCapsules = []
        self._blueCapsules = []

        for capsule in self.getCapsules():
            if (self.isOnRedSide(capsule)):
                self._redCapsules.append(capsule)
            else:
                self._blueCapsules.append(capsule)

        self._redFood = Grid(self._food.getWidth(), self._food.getHeight(), initialValue = False)
        self._blueFood = Grid(self._food.getWidth(), self._food.getHeight(), initialValue = False)

        for x in range(self._food.getWidth()):
            for y in range(self._food.getHeight()):
                if (not self._food[x][y]):
                    continue

                if (self.isOnRedSide((x, y))):
                    self._redFood[x][y] = True
                else:
                    self._blueFood[x][y] = True

    # Override
    def generateSuccessor(self, agentIndex, action):
        # Check that successors exist.
        if (self.isOver()):
            raise RuntimeError("Can't generate successors of a terminal state.")

        successor = self._initSuccessor()
        successor._applySuccessorAction(agentIndex, action)

        return successor

    # Override
    def getLegalActions(self, agentIndex = 0):
        if (self.isOver()):
            return []

        return AgentRules.getLegalActions(self, agentIndex)

    # Override
    def eatCapsule(self, x, y):
        if (not self._capsulesCopied):
            self._redCapsules = self._redCapsules.copy()
            self._blueCapsules = self._blueCapsules.copy()

        super().eatCapsule(x, y)

        if (self.isOnRedSide((x, y))):
            self._redCapsules.remove((x, y))
        else:
            self._blueCapsules.remove((x, y))

    # Override
    def eatFood(self, x, y):
        if (not self._foodCopied):
            self._redFood = self._redFood.copy()
            self._blueFood = self._blueFood.copy()

        super().eatFood(x, y)

        if (self.isOnRedSide((x, y))):
            self._redFood[x][y] = False
        else:
            self._blueFood[x][y] = False

    def getBlueCapsules(self):
        """
        Get a list of remaining capsules on the blue side.
        The caller should not modify the list.
        """

        return self._blueCapsules

    def getBlueFood(self):
        """
        Returns a grid of food that corresponds to the food on the blue team's side.
        For the grid g, g[x][y] = True if there is food in (x, y) that belongs to
        blue (meaning blue is protecting it, red is trying to eat it).
        The caller should not modify the grid.
        """

        return self._blueFood

    def getBlueTeamIndices(self):
        """
        Returns a list of the agent index numbers for the agents on the blue team.
        The caller should not modify the list.
        """

        return self._blueTeam

    def getRedCapsules(self):
        """
        Get a list of remaining capsules on the red side.
        The caller should not modify the list.
        """

        return self._redCapsules

    def getRedFood(self):
        """
        Returns a grid of food that corresponds to the food on the red team's side.
        For the grid g, g[x][y] = True if there is food in (x, y) that belongs to
        red (meaning red is protecting it, blue is trying to eat it).
        The caller should not modify the grid.
        """

        return self._redFood

    def getRedTeamIndices(self):
        """
        Returns a list of agent index numbers for the agents on the red team.
        The caller should not modify the list.
        """

        return self._redTeam

    def getTimeleft(self):
        return self._timeleft

    def isOnBlueSide(self, position):
        """
        Check the position see if it is on the blue side.
        Note that this is not checking if a position/agent is on the blue TEAM,
        just the blue side of the board.
        Red is on the left side, blue on the right.
        """

        return not self.isOnRedSide(position)

    def isOnBlueTeam(self, agentIndex):
        """
        Returns true if the agent with the given agentIndex is on the red team.
        """

        return not self.isOnRedTeam(agentIndex)

    def isOnRedSide(self, position):
        """
        Check the position see if it is on the red side.
        Note that this is not checking if a position/agent is on the red TEAM,
        just the red side of the board.
        Red is on the left side, blue on the right.
        """

        return position[0] < int(self._layout.width / 2)

    def isOnRedTeam(self, agentIndex):
        """
        Returns true if the agent with the given agentIndex is on the red team.
        """

        return self._teams[agentIndex]

    def _applySuccessorAction(self, agentIndex, action):
        """
        Apply the action to the context state (self).
        """

        # Find appropriate rules for the agent.
        AgentRules.applyAction(self, action, agentIndex)
        AgentRules.checkDeath(self, agentIndex)
        AgentRules.decrementTimer(self.getAgentState(agentIndex))

        # Book keeping.
        self._lastAgentMoved = agentIndex
        self._timeleft -= 1

        self._hash = None

class CaptureRules:
    """
    These game rules manage the control flow of a game, deciding when
    and how the game starts and ends.
    """

    def newGame(self, layout, agents, display, length, catchExceptions):
        initState = CaptureGameState(layout, length)
        starter = random.randint(0, 1)
        logging.info('%s team starts' % ['Red', 'Blue'][starter])
        game = Game(agents, display, self, startingIndex = starter,
                catchExceptions = catchExceptions)
        game.state = initState
        game.length = length

        self._totalBlueFood = initState.getBlueFood().count()
        self._totalRedFood = initState.getRedFood().count()

        return game

    def process(self, state, game):
        """
        Checks to see whether it is time to end the game.
        """

        # The two ways a game can end is by eatting food or a timeout.
        # The timeout endgame will be discovered here,
        # and the food endgame will be triggered elsewhere.
        # So, to continue in this method the game must be over (by food),
        # or the time must be out.

        if (not state.isOver() and state.getTimeleft() > 0):
            return

        game.gameOver = True

        redWin = False
        blueWin = False

        if (state.getRedFood().count() <= MIN_FOOD):
            logging.info("The Blue team ate all but %d of the opponents' dots." % MIN_FOOD)
            blueWin = True
        elif (state.getBlueFood().count() <= MIN_FOOD):
            logging.info("The Red team ate all but %d of the opponents' dots." % MIN_FOOD)
            redWin = True
        else:
            logging.info('Time is up.')

            if (state.getScore() < 0):
                blueWin = True
            elif (state.getScore() > 0):
                redWin = True

        if (not redWin and not blueWin):
            logging.info('Tie game!')
            state.endGame(False)
            return

        winner = 'Red'
        if (blueWin):
            winner = 'Blue'

        logging.info('The %s team wins by %d points.' % (winner, abs(state.getScore())))
        state.endGame(True)

    def agentCrash(self, game, agentIndex):
        if (game.state.isOnRedTeam(agentIndex)):
            logging.error("Red agent crashed.")
            game.state.setScore(-1)
        else:
            logging.error("Blue agent crashed.")
            game.state.setScore(1)

    def getMaxTotalTime(self, agentIndex):
        return 900  # Move limits should prevent this from ever happening

    def getMaxStartupTime(self, agentIndex):
        return 15  # 15 seconds for registerInitialState

    def getMoveWarningTime(self, agentIndex):
        return 1  # One second per move

    def getMoveTimeout(self, agentIndex):
        return 3  # Three seconds results in instant forfeit

    def getMaxTimeWarnings(self, agentIndex):
        return 2  # Third violation loses the game

class AgentRules:
    """
    These functions govern how each agent interacts with her environment.
    """

    AGENT_SPEED = 1.0

    @staticmethod
    def getLegalActions(state, agentIndex):
        """
        Returns a list of possible actions.
        """

        agentState = state.getAgentState(agentIndex)
        return Actions.getPossibleActions(agentState.getPosition(), agentState.getDirection(),
                state.getWalls())

    @staticmethod
    def applyAction(state, action, agentIndex):
        """
        Edits the state to reflect the results of the action.
        """

        legal = AgentRules.getLegalActions(state, agentIndex)
        if (action not in legal):
            raise ValueError('Illegal action: ' + str(action))

        agentState = state.getAgentState(agentIndex)

        # Update position.
        vector = Actions.directionToVector(action, AgentRules.AGENT_SPEED)
        agentState.updatePosition(vector)

        # Eat.
        nextPosition = agentState.getPosition()
        nearest = nearestPoint(nextPosition)
        if (agentState.isPacman() and manhattan(nearest, nextPosition) <= 0.9):
            AgentRules.consume(nearest, state, state.isOnRedTeam(agentIndex))

        # Potentially change agent type.
        if (nextPosition == nearest):
            # Agents are pacmen when they are not on their own side.
            position = agentState.getPosition()
            agentState.setIsPacman(state.isOnRedTeam(agentIndex) != state.isOnRedSide(position))

    @staticmethod
    def consume(position, state, isRed):
        """
        There is an agent of the specified team on the given position.
        If there is anything they can eat, do it.
        Note that the consuming agent is guarenteed to be in pacman form (not ghost form).
        """

        x, y = position

        # Eat food.
        if (state.hasFood(x, y)):
            state.eatFood(x, y)

            if (isRed):
                state.addScore(FOOD_POINTS)
            else:
                state.addScore(-FOOD_POINTS)

            if ((isRed and state.getBlueFood().count() <= MIN_FOOD)
                    or (not isRed and state.getRedFood().count() <= MIN_FOOD)):
                state.endGame(True)

            return

        # Eat a capsule.
        if (isRed):
            myCapsules = state.getBlueCapsules()
        else:
            myCapsules = state.getRedCapsules()

        if (position in myCapsules):
            state.eatCapsule(x, y)

            # Reset ghosts' scared timers.
            if (isRed):
                otherTeam = state.getBlueTeamIndices()
            else:
                otherTeam = state.getRedTeamIndices()

            for agentIndex in otherTeam:
                state.getAgentState(agentIndex).setScaredTimer(SCARED_TIME)

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
        agentState = state.getAgentState(agentIndex)

        if (state.isOnRedTeam(agentIndex)):
            teamPointModifier = 1
            otherTeam = state.getBlueTeamIndices()
        else:
            teamPointModifier = -1
            otherTeam = state.getRedTeamIndices()

        for otherAgentIndex in otherTeam:
            otherAgentState = state.getAgentState(otherAgentIndex)

            # Ignore agents with a matching type (e.g. two ghosts).
            if (agentState.isPacman() == otherAgentState.isPacman()):
                continue

            otherPosition = otherAgentState.getPosition()

            # Ignore other agents that are too far away.
            if (otherPosition is None
                    or manhattan(otherPosition, agentState.getPosition()) > COLLISION_TOLERANCE):
                continue

            # If we are a brave ghost or they are a scared ghost, then we will eat them.
            # Otherwise, we are being eatten.
            if (agentState.isBraveGhost() or otherAgentState.isScaredGhost()):
                state.addScore(teamPointModifier * KILL_POINTS)
                otherAgentState.respawn()
            else:
                state.addScore(teamPointModifier * -KILL_POINTS)
                agentState.respawn()

#############################
# FRAMEWORK TO START A GAME #
#############################

def parseAgentArgs(str):
    if (str is None or str == ''):
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
    Processes the command used to run capture from the command line.
    """

    description = """
    DESCRIPTION:
        This program will run a capture game. Two teams of pacman agents are pitted against
        one another in a capture the flag style game. Collect the most pellets to win!

    EXAMPLES:
        (1) python -m pacai.bin.capture
          - Starts a game with two baseline agents.
        (2) python -m pacai.bin.capture --keys0
          - Starts an interactive game where the arrow keys control agent 0 and all other
            agents are baseline agents.
        (3) python -m pacai.bin.capture.py -r pacai.core.baselineTeam -b pacai.student.myTeam
          - Starts an automated game where the red team is a baseline team and blue
            team is pacai.student.myTeam.
    """

    parser = getParser(description, os.path.basename(__file__))

    parser.add_argument('-b', '--blue', dest = 'blue',
            action = 'store', type = str, default = 'pacai.core.baselineTeam',
            help = 'set blue team (default: %(default)s)')

    parser.add_argument('-l', '--layout', dest = 'layout',
            action = 'store', type = str, default = 'defaultCapture',
            help = 'use the specified map layout or input RANDOM<seed> '
                + 'for a random seeded map (i.e. RANDOM23) (default: %(default)s)')

    parser.add_argument('-r', '--red', dest = 'red',
            action = 'store', type = str, default = 'pacai.core.baselineTeam',
            help = 'set red team (default: %(default)s)')

    parser.add_argument('--blue-args', dest = 'blueArgs',
            action = 'store', type = str, default = None,
            help = 'comma separated arguments to be passed to blue team (e.g. \'opt1=val1,opt2\') '
                + '(default: %(default)s)')

    parser.add_argument('--keys0', dest = 'keys0',
            action = 'store_true', default = False,
            help = 'make agent 0 (first red player) a keyboard agent (default: %(default)s)')

    parser.add_argument('--keys1', dest = 'keys1',
            action = 'store_true', default = False,
            help = 'make agent 1 (first blue player) a keyboard agent (default: %(default)s)')

    parser.add_argument('--keys2', dest = 'keys2',
            action = 'store_true', default = False,
            help = 'make agent 2 (second red player) a keyboard agent (default: %(default)s)')

    parser.add_argument('--keys3', dest = 'keys3',
            action = 'store_true', default = False,
            help = 'make agent 3 (second blue player) a keyboard agent (default: %(default)s)')

    parser.add_argument('--max-moves', dest = 'maxMoves',
            action = 'store', type = int, default = 1200,
            help = 'set maximum number of moves in a game (default: %(default)s)')

    parser.add_argument('--red-args', dest = 'redArgs',
            action = 'store', type = str, default = None,
            help = 'comma separated arguments to be passed to red team (e.g. \'opt1=val1,opt2\') '
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

    viewOptions = {
        'gifFPS': options.gifFPS,
        'gifPath': options.gif,
        'skipFrames': options.gifSkipFrames,
        'spritesPath': options.spritesPath,
    }

    # Choose a display format.
    if options.textGraphics:
        args['display'] = CaptureTextView(**viewOptions)
    elif options.nullGraphics:
        args['display'] = CaptureNullView(**viewOptions)
    else:
        # Defer importing the GUI unless we actually need it.
        # This allows people to not have tkinter installed.
        from pacai.ui.capture.gui import CaptureGUIView

        args['display'] = CaptureGUIView(fps = options.fps, title = 'Capture', **viewOptions)

    args['redTeamName'] = options.red
    args['blueTeamName'] = options.blue

    # If no seed entry generate a random seed value.
    seed = options.seed
    if seed is None:
        seed = random.randint(0, 2**32)
    random.seed(seed)
    logging.debug('Seed value: ' + str(seed))

    # Choose a pacman agent.
    redArgs = parseAgentArgs(options.redArgs)
    blueArgs = parseAgentArgs(options.blueArgs)

    if options.numTraining > 0:
        redArgs['numTraining'] = options.numTraining
        blueArgs['numTraining'] = options.numTraining

    nokeyboard = options.textGraphics or options.nullGraphics or options.numTraining > 0
    logging.debug('\nRed team %s with %s:' % (options.red, redArgs))
    redAgents = loadAgents(True, options.red, nokeyboard, redArgs)
    logging.debug('\nBlue team %s with %s:' % (options.blue, blueArgs))
    blueAgents = loadAgents(False, options.blue, nokeyboard, blueArgs)
    args['agents'] = sum([list(el) for el in zip(redAgents, blueAgents)], [])  # List of agents.

    numKeyboardAgents = 0
    for index, val in enumerate([options.keys0, options.keys1, options.keys2, options.keys3]):
        if (not val):
            continue

        if (numKeyboardAgents == 0):
            agent = keyboard.WASDKeyboardAgent(index, keyboard = args['display'].getKeyboard())
        elif (numKeyboardAgents == 1):
            agent = keyboard.IJKLKeyboardAgent(index, keyboard = args['display'].getKeyboard())
        else:
            raise ValueError('Max of two keyboard agents supported.')

        numKeyboardAgents += 1
        args['agents'][index] = agent

    # Choose a layout.
    if options.layout.startswith('RANDOM'):
        layoutSeed = None
        if (options.layout != 'RANDOM'):
            layoutSeed = int(options.layout[6:])

        args['layout'] = Layout(generateMaze(layoutSeed).split('\n'))
    elif options.layout.lower().find('capture') == -1:
        raise ValueError('You must use a capture layout with capture.py.')
    else:
        args['layout'] = getLayout(options.layout)

    if (args['layout'] is None):
        raise ValueError('The layout ' + options.layout + ' cannot be found.')

    args['length'] = options.maxMoves
    args['numGames'] = options.numGames
    args['numTraining'] = options.numTraining
    args['record'] = options.record
    args['catchExceptions'] = options.catchExceptions
    args['replay'] = options.replay

    return args

def loadAgents(isRed, agentModule, textgraphics, args):
    """
    Calls agent factories and returns lists of agents.
    """

    createTeamFunctionPath = agentModule + '.createTeam'
    createTeamFunction = reflection.qualifiedImport(createTeamFunctionPath)

    logging.info('Loading Team: %s', agentModule)
    logging.info('Arguments: %s', args)

    indexAddend = 0
    if (not isRed):
        indexAddend = 1
    indices = [2 * i + indexAddend for i in range(2)]

    return createTeamFunction(indices[0], indices[1], isRed, **args)

def replayGame(layout, agents, actions, display, length, redTeamName, blueTeamName):
    agents = [DummyAgent(index) for index in range(len(agents))]
    rules = CaptureRules()
    game = rules.newGame(layout, agents, display, length, False)
    state = game.state
    display.redTeam = redTeamName
    display.blueTeam = blueTeamName
    display.initialize(state)

    for action in actions:
        # Execute the action
        state = state.generateSuccessor(*action)
        # Change the display
        display.update(state)
        # Allow for game specific conditions (winning, losing, etc.)
        rules.process(state, game)

    display.finish()

def runGames(layout, agents, display, length, numGames, record, numTraining,
        redTeamName, blueTeamName, catchExceptions = False, **kwargs):
    rules = CaptureRules()
    games = []

    nullView = None
    if (numTraining > 0):
        logging.info('Playing %d training games.' % numTraining)
        nullView = CaptureNullView()

    for i in range(numGames):
        isTraining = (i < numTraining)

        if (isTraining):
            # Suppress graphics for training.
            gameDisplay = nullView
        else:
            gameDisplay = display

        g = rules.newGame(layout, agents, gameDisplay, length, catchExceptions)
        g.run()

        if (not isTraining):
            games.append(g)

        g.record = None
        if record:
            components = {
                'layout': layout,
                'agents': [agent.__class__.__name__ for agent in agents],
                'actions': g.moveHistory,
                'length': length,
                'redTeamName': redTeamName,
                'blueTeamName': blueTeamName
            }

            path = 'replay'
            if (isinstance(record, str)):
                path = record

            g.record = pickle.dumps(components)
            with open(path, 'wb') as file:
                file.write(g.record)

            logging.info("Game recorded to: '%s'." % (path))

    if (numGames > 0):
        scores = [game.state.getScore() for game in games]
        redWinRate = [s > 0 for s in scores].count(True) / float(len(scores))
        blueWinRate = [s < 0 for s in scores].count(True) / float(len(scores))
        logging.info('Average Score:%s', sum(scores) / float(len(scores)))
        logging.info('Scores:%s', ', '.join([str(score) for score in scores]))
        logging.info('Red Win Rate: %d/%d (%.2f)' %
                ([s > 0 for s in scores].count(True), len(scores), redWinRate))
        logging.info('Blue Win Rate: %d/%d (%.2f)' %
                ([s < 0 for s in scores].count(True), len(scores), blueWinRate))
        logging.info('Record: %s',
                ', '.join([('Blue', 'Tie', 'Red')[max(0, min(2, 1 + s))] for s in scores]))

    return games


def main(argv):
    """
    Entry point for a capture game.
    The args are a blind pass of `sys.argv` with the executable stripped.
    """

    initLogging()

    # Get game components based on input
    options = readCommand(argv)

    # Special case: recorded games don't use the runGames method.
    if (options['replay'] is not None):
        logging.info('Replaying recorded game %s.' % options['replay'])

        recorded = None
        with open(options['replay'], 'rb') as file:
            recorded = pickle.load(file)

        recorded['display'] = options['display']
        replayGame(**recorded)

        return

    return runGames(**options)

if __name__ == '__main__':
    main(sys.argv[1:])
