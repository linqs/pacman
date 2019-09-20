"""
Capture.py holds the logic for Pacman capture the flag.

    (i) Your interface to the pacman world:
                    Pacman is a complex environment. You probably don't want to
                    read through all of the code we wrote to make the game runs
                    correctly. This section contains the parts of the code
                    that you will need to understand in order to complete the
                    project. There is also some code in game.py that you should
                    understand.

    (ii) The hidden secrets of pacman:
                    This section contains all of the logic code that the pacman
                    environment uses to decide who can move where, who dies when
                    things collide, etc. You shouldn't need to read this section
                    of code, but you can if you want.

    (iii) Framework to start a game:
                    The final section contains the code for reading the command
                    you use to set up the game, then starting up a new game, along with
                    linking in all the external parts (agent functions, graphics).
                    Check this section out to see all the options available to you.

To play your first game, type 'python capture.py' from the command line.
The keys are
    P1: 'a', 's', 'd', and 'w' to move
    P2: 'l', ';', ',', and 'p' to move
"""

import importlib
import logging
import optparse
import pickle
import random
import sys
import traceback

import pacai.core.layout
import pacai.util.mazeGenerator
from pacai.agents import keyboard
from pacai.core.distance import manhattan
from pacai.core.game import Actions
from pacai.core.game import Game
from pacai.core.game import Grid
from pacai.core.gamestate import AbstractGameState
from pacai.util.logs import initLogging
from pacai.util.util import nearestPoint

COLLISION_TOLERANCE = 0.7  # How close ghosts must be to Pacman to kill

KILL_POINTS = 0
FOOD_POINTS = 1  # Points for eating food.

SONAR_NOISE_RANGE = 13  # Must be odd
SONAR_NOISE_VALUES = [i - int((SONAR_NOISE_RANGE - 1) / 2) for i in range(SONAR_NOISE_RANGE)]
SIGHT_RANGE = 5  # Manhattan distance
MIN_FOOD = 2

SCARED_TIME = 40

FIXED_SEED = 140188

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
            agentIsRed = self.isOnRedSide(agentState.configuration.getPosition())

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

        self._redFood = Grid(self._food.width, self._food.height, initialValue = False)
        self._blueFood = Grid(self._food.width, self._food.height, initialValue = False)

        for x in range(self._food.width):
            for y in range(self._food.height):
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

        if 'drawCenterLine' in dir(display):
            display.drawCenterLine()

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

    def getProgress(self, game):
        blue = 1.0 - (game.state.getBlueFood().count() / float(self._totalBlueFood))
        red = 1.0 - (game.state.getRedFood().count() / float(self._totalRedFood))
        moves = len(self.moveHistory) / float(game.length)

        # Return the most likely progress indicator, clamped to [0, 1].
        return min(max(0.75 * max(red, blue) + 0.25 * moves, 0.0), 1.0)

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

        agentConfig = state.getAgentState(agentIndex).configuration
        return Actions.getPossibleActions(agentConfig, state.getWalls())

    @staticmethod
    def applyAction(state, action, agentIndex):
        """
        Edits the state to reflect the results of the action.
        """

        legal = AgentRules.getLegalActions(state, agentIndex)
        if (action not in legal):
            raise ValueError('Illegal action: ' + str(action))

        agentState = state.getAgentState(agentIndex)

        # Update Configuration
        vector = Actions.directionToVector(action, AgentRules.AGENT_SPEED)
        agentState.configuration = agentState.configuration.generateSuccessor(vector)

        # Eat
        nextPosition = agentState.configuration.getPosition()
        nearest = nearestPoint(nextPosition)
        if (agentState.isPacman() and manhattan(nearest, nextPosition) <= 0.9):
            AgentRules.consume(nearest, state, state.isOnRedTeam(agentIndex))

        # Potentially change agent type.
        if (nextPosition == nearest):
            # Agents are pacmen when they are not on their own side.
            position = agentState.configuration.getPosition()
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
                state.getAgentState(agentIndex).scaredTimer = SCARED_TIME

    @staticmethod
    def decrementTimer(agentState):
        agentState.scaredTimer = max(0, agentState.scaredTimer - 1)
        if (agentState.scaredTimer == 0):
            agentState.configuration.pos = nearestPoint(agentState.configuration.pos)

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

def default(str):
    return str + ' [Default: %default]'

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
    Processes the command used to run pacman from the command line.
    """
    usageStr = """
    USAGE:        python pacman.py <options>
    EXAMPLES:    (1) python capture.py
                                    - starts a game with two baseline agents
                            (2) python capture.py --keys0
                                    - starts a two-player interactive game
                                        where the arrow keys control agent 0,
                                        and all other agents are baseline agents
                            (3) python capture.py -r pacai.core.baselineTeam -b pacai.student.myTeam
                                    - starts a fully automated game where the red team
                                        is a baseline team and blue team is pacai.student.myTeam
    """
    parser = optparse.OptionParser(usageStr)

    parser.add_option('-r', '--red', help=default('Red team'), default='pacai.core.baselineTeam')
    parser.add_option('-b', '--blue', help=default('Blue team'), default='pacai.core.baselineTeam')
    parser.add_option('--redOpts', help=default('Options for red team (e.g. first=keys)'),
            default='')
    parser.add_option('--blueOpts', help=default('Options for blue team (e.g. first=keys)'),
            default='')
    parser.add_option('--keys0', help='Make agent 0 (first red player) a keyboard agent',
            action='store_true', default=False)
    parser.add_option('--keys1', help='Make agent 1 (second red player) a keyboard agent',
            action='store_true', default=False)
    parser.add_option('--keys2', help='Make agent 2 (first blue player) a keyboard agent',
            action='store_true', default=False)
    parser.add_option('--keys3', help='Make agent 3 (second blue player) a keyboard agent',
            action='store_true', default=False)
    parser.add_option('-l', '--layout', dest='layout',
            help=default('the LAYOUT_FILE from which to load the layout; use RANDOM for a random'
                    + 'maze; use RANDOM<seed> to use a specified random seed, e.g., RANDOM23'),
            metavar='LAYOUT_FILE', default='defaultCapture')
    parser.add_option('-t', '--textgraphics', action='store_true', dest='textgraphics',
            help='Display output as text only', default=False)
    parser.add_option('-q', '--quiet', action='store_true',
            help='Display minimal output and no graphics', default=False)
    parser.add_option('-z', '--zoom', type='float', dest='zoom',
            help=default('Zoom in the graphics'), default=1)
    parser.add_option('-i', '--time', type='int', dest='time',
            help=default('TIME limit of a game in moves'), default=1200, metavar='TIME')
    parser.add_option('-n', '--numGames', type='int',
            help=default('Number of games to play'), default=1)
    parser.add_option('-f', '--fixRandomSeed', action='store_true',
            help='Fixes the random seed to always play the same game', default=False)
    parser.add_option('--record', type='string', dest='record',
            help='Writes game histories to the named file')
    parser.add_option('--replay', default=None, help='Replays a recorded game file.')
    parser.add_option('-x', '--numTraining', dest='numTraining', type='int',
            help=default('How many episodes are training (suppresses output)'), default=0)
    parser.add_option('-c', '--catchExceptions', action='store_true', default=False,
            help='Catch exceptions and enforce time limits')
    parser.add_option('--gif', dest='gif',
            help=default('Save the game as a gif to the specified path'))
    parser.add_option('--gif-skip-frames', dest='gifSkipFrames', type='int', default=0,
            help=default('Skip this number of frames between frames of the gif.'))
    parser.add_option('--gif-fps', dest='gifFPS', type='float', default=10,
            help=default('FPS of the gif.'))

    options, otherjunk = parser.parse_args(argv)
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)
    args = dict()

    # Choose a display format
    if options.textgraphics:
        import pacai.ui.textDisplay
        args['display'] = pacai.ui.textDisplay.PacmanGraphics()
    elif options.quiet:
        import pacai.ui.textDisplay
        args['display'] = pacai.ui.textDisplay.NullGraphics()
    else:
        import pacai.ui.captureGraphicsDisplay
        # Hack for agents writing to the display
        pacai.ui.captureGraphicsDisplay.FRAME_TIME = 0
        args['display'] = pacai.ui.captureGraphicsDisplay.CapturePacmanGraphics(options.red,
                options.blue,
                options.zoom, 0, capture=True,
                gif = options.gif, gifSkipFrames = options.gifSkipFrames,
                gifFps = options.gifFPS)
        import __main__
        __main__.__dict__['_display'] = args['display']

    args['redTeamName'] = options.red
    args['blueTeamName'] = options.blue

    if options.fixRandomSeed:
        random.seed(FIXED_SEED)

    # Choose a pacman agent
    redArgs, blueArgs = parseAgentArgs(options.redOpts), parseAgentArgs(options.blueOpts)
    if options.numTraining > 0:
        redArgs['numTraining'] = options.numTraining
        blueArgs['numTraining'] = options.numTraining
    nokeyboard = options.textgraphics or options.quiet or options.numTraining > 0
    logging.debug('\nRed team %s with %s:' % (options.red, redArgs))
    redAgents = loadAgents(True, options.red, nokeyboard, redArgs)
    logging.debug('\nBlue team %s with %s:' % (options.blue, blueArgs))
    blueAgents = loadAgents(False, options.blue, nokeyboard, blueArgs)
    args['agents'] = sum([list(el) for el in zip(redAgents, blueAgents)], [])  # list of agents

    numKeyboardAgents = 0
    for index, val in enumerate([options.keys0, options.keys1, options.keys2, options.keys3]):
        if not val:
            continue

        if numKeyboardAgents == 0:
            agent = keyboard.WASDKeyboardAgent(index)
        elif numKeyboardAgents == 1:
            agent = keyboard.IJKLKeyboardAgent(index)
        else:
            raise Exception('Max of two keyboard agents supported')
        numKeyboardAgents += 1
        args['agents'][index] = agent

    # Choose a layout
    if options.layout.startswith('RANDOM'):
        seed = random.randint(0, 99999999)
        if (options.layout != 'RANDOM'):
            seed = int(options.layout[6:])

        args['layout'] = pacai.core.layout.Layout(randomLayout(seed).split('\n'))
    elif options.layout.lower().find('capture') == -1:
        raise Exception('You must use a capture layout with capture.py')
    else:
        args['layout'] = pacai.core.layout.getLayout(options.layout)

    if (args['layout'] is None):
        raise Exception("The layout " + options.layout + " cannot be found")

    args['length'] = options.time
    args['numGames'] = options.numGames
    args['numTraining'] = options.numTraining
    args['record'] = options.record
    args['catchExceptions'] = options.catchExceptions
    args['replay'] = options.replay

    return args

def randomLayout(seed = None):
    if not seed:
        seed = random.randint(0, 99999999)
    return pacai.util.util.mazeGenerator.generateMaze(seed)

def loadAgents(isRed, agent_module, textgraphics, cmdLineArgs):
    "Calls agent factories and returns lists of agents"
    try:
        module = importlib.import_module(agent_module)
    except ImportError:
        logging.error('The team "' + agent_module + '" could not be loaded! ')
        traceback.print_exc()
        return [None for i in range(2)]

    args = dict()
    args.update(cmdLineArgs)  # Add command line args with priority

    logging.info('Loading Team:%s', agent_module)
    logging.info('Arguments:%s', args)

    try:
        createTeamFunc = getattr(module, 'createTeam')
    except AttributeError:
        logging.error('The team "' + agent_module + '" could not be loaded! ')
        traceback.print_exc()
        return [None for i in range(2)]

    indexAddend = 0
    if not isRed:
        indexAddend = 1
    indices = [2 * i + indexAddend for i in range(2)]
    return createTeamFunc(indices[0], indices[1], isRed, **args)

def replayGame(layout, agents, actions, display, length, redTeamName, blueTeamName):
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

    if numTraining > 0:
        logging.info('Playing %d training games' % numTraining)

    for i in range(numGames):
        beQuiet = (i < numTraining)
        if beQuiet:
            # Suppress output and graphics
            import textDisplay
            gameDisplay = textDisplay.NullGraphics()
        else:
            gameDisplay = display

        g = rules.newGame(layout, agents, gameDisplay, length, catchExceptions)
        g.run()

        if (not beQuiet):
            games.append(g)

        g.record = None
        if record:
            components = {
                'layout': layout,
                'agents': agents,
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
    The main function called when pacman.py is run
    from the command line:

    > python capture.py

    See the usage string for more details.

    > python capture.py --help

    argv already has the executable stripped.
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
