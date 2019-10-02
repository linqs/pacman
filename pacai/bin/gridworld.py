import argparse
import logging
import os
import random
import sys
import textwrap

from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.core.environment import Environment
from pacai.core.mdp import MarkovDecisionProcess
from pacai.student.qlearningAgents import QLearningAgent
from pacai.student.valueIterationAgent import ValueIterationAgent
from pacai.ui.gridworld.text import TextGridworldDisplay
from pacai.ui.gridworld.utils import wait_for_keys
from pacai.util.counter import Counter
from pacai.util.logs import initLogging
from pacai.util.logs import updateLoggingLevel

class Gridworld(MarkovDecisionProcess):
    def __init__(self, grid):
        # layout
        if (isinstance(grid, list)):
            grid = makeGrid(grid)

        self.grid = grid

        # parameters
        self.livingReward = 0.0
        self.noise = 0.2

    def setLivingReward(self, reward):
        """
        The (negative) reward for exiting "normal" states.

        Note that in the R+N text, this reward is on entering
        a state and therefore is not clearly part of the state's
        future rewards.
        """

        self.livingReward = reward

    def setNoise(self, noise):
        """
        The probability of moving in an unintended direction.
        """

        self.noise = noise

    def getPossibleActions(self, state):
        """
        Returns list of valid actions for 'state'.

        Note that you can request moves into walls and
        that "exit" states transition to the terminal
        state under the special action "done".
        """

        if state == self.grid.terminalState:
            return ()

        x, y = state
        if isinstance(self.grid[x][y], int):
            return ('exit', )

        return ('north', 'west', 'south', 'east')

    def getStates(self):
        """
        Return list of all states.
        """

        # The true terminal state.
        states = [self.grid.terminalState]
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid[x][y] != '#':
                    state = (x, y)
                    states.append(state)

        return states

    def getReward(self, state, action, nextState):
        """
        Get reward for state, action, nextState transition.

        Note that the reward depends only on the state being
        departed (as in the R+N book examples, which more or
        less use this convention).
        """

        if state == self.grid.terminalState:
            return 0.0

        x, y = state
        cell = self.grid[x][y]
        if isinstance(cell, int) or isinstance(cell, float):
            return cell

        return self.livingReward

    def getStartState(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid[x][y] == 'S':
                    return (x, y)

        raise Exception('Grid has no start state')

    def isTerminal(self, state):
        """
        Only the TERMINAL_STATE state is *actually* a terminal state.
        The other "exit" states are technically non-terminals with
        a single action "exit" which leads to the true terminal state.
        This convention is to make the grids line up with the examples
        in the R+N textbook.
        """

        return state == self.grid.terminalState

    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """

        if action not in self.getPossibleActions(state):
            raise Exception('Illegal action!')

        if self.isTerminal(state):
            return []

        x, y = state

        if isinstance(self.grid[x][y], int) or isinstance(self.grid[x][y], float):
            termState = self.grid.terminalState
            return [(termState, 1.0)]

        successors = []

        northState = (self.__isAllowed(y + 1, x) and (x, y + 1)) or state
        westState = (self.__isAllowed(y, x - 1) and (x - 1, y)) or state
        southState = (self.__isAllowed(y - 1, x) and (x, y - 1)) or state
        eastState = (self.__isAllowed(y, x + 1) and (x + 1, y)) or state

        if action == 'north' or action == 'south':
            if action == 'north':
                successors.append((northState, 1 - self.noise))
            else:
                successors.append((southState, 1 - self.noise))

            massLeft = self.noise
            successors.append((westState, massLeft / 2.0))
            successors.append((eastState, massLeft / 2.0))

        if action == 'west' or action == 'east':
            if action == 'west':
                successors.append((westState, 1 - self.noise))
            else:
                successors.append((eastState, 1 - self.noise))

            massLeft = self.noise
            successors.append((northState, massLeft / 2.0))
            successors.append((southState, massLeft / 2.0))

        successors = self.__aggregate(successors)
        return successors

    def __aggregate(self, statesAndProbs):
        counter = Counter()
        for state, prob in statesAndProbs:
            counter[state] += prob

        newStatesAndProbs = []
        for state, prob in list(counter.items()):
            newStatesAndProbs.append((state, prob))

        return newStatesAndProbs

    def __isAllowed(self, y, x):
        if y < 0 or y >= self.grid.height:
            return False

        if x < 0 or x >= self.grid.width:
            return False

        return self.grid[x][y] != '#'

class GridworldEnvironment(Environment):
    def __init__(self, gridWorld):
        self.gridWorld = gridWorld
        self.reset()

    def getCurrentState(self):
        return self.state

    def getPossibleActions(self, state):
        return self.gridWorld.getPossibleActions(state)

    def doAction(self, action):
        successors = self.gridWorld.getTransitionStatesAndProbs(self.state, action)
        sum = 0.0
        rand = random.random()
        state = self.getCurrentState()

        for nextState, prob in successors:
            sum += prob
            if sum > 1.0:
                raise Exception('Total transition probability more than one; sample failure.')

            if rand < sum:
                reward = self.gridWorld.getReward(state, action, nextState)
                self.state = nextState
                return (nextState, reward)

        raise Exception('Total transition probability less than one; sample failure.')

    def reset(self):
        self.state = self.gridWorld.getStartState()

class Grid(object):
    """
    A 2-dimensional array of immutables backed by a list of lists.
    Data is accessed via grid[x][y] where (x, y) are cartesian coordinates with x horizontal,
    y vertical and the origin (0, 0) in the bottom left corner.

    The __str__ method constructs an output that is oriented appropriately.
    """

    def __init__(self, width, height, initialValue=' '):
        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(height)] for x in range(width)]
        self.terminalState = 'TERMINAL_STATE'

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __eq__(self, other):
        if (other is None):
            return False
        return self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def _getLegacyText(self):
        t = [[self.data[x][y] for x in range(self.width)] for y in range(self.height)]
        t.reverse()
        return t

    def __str__(self):
        return str(self._getLegacyText())

def makeGrid(gridString):
    width, height = len(gridString[0]), len(gridString)
    grid = Grid(width, height)
    for ybar, line in enumerate(gridString):
        y = height - ybar - 1
        for x, el in enumerate(line):
            grid[x][y] = el

    return grid

def getUserAction(state, actionFunction):
    """
    Get an action from the user (rather than the agent).

    Used for debugging and lecture demos.
    """

    action = None

    while True:
        keys = wait_for_keys()

        if ('Up' in keys):
            action = 'north'

        if ('Down' in keys):
            action = 'south'

        if ('Left' in keys):
            action = 'west'

        if ('Right' in keys):
            action = 'east'

        if ('q' in keys):
            sys.exit(0)

        if (action is None):
            continue

        break

    actions = actionFunction(state)
    if action not in actions:
        action = actions[0]

    return action

def runEpisode(agent, environment, discount, decision, display, message, pause, episode):
    returns = 0
    totalDiscount = 1.0
    environment.reset()

    if (isinstance(agent, ReinforcementAgent)):
        agent.startEpisode()

    logging.info('BEGINNING EPISODE: ' + str(episode) + "\n")

    while True:
        # DISPLAY CURRENT STATE
        state = environment.getCurrentState()
        display(state)
        pause()

        # END IF IN A TERMINAL STATE
        actions = environment.getPossibleActions(state)
        if (len(actions) == 0):
            logging.info('EPISODE ' + str(episode) + ' COMPLETE: RETURN WAS ' + str(returns) + '\n')
            return returns

        # GET ACTION (USUALLY FROM AGENT)
        action = decision(state)
        if (action is None):
            raise Exception('Error: Agent returned None action')

        # EXECUTE ACTION
        nextState, reward = environment.doAction(action)
        logString = ''
        logString += '\nStarted in state: ' + str(state)
        logString += '\nTook action: ' + str(action)
        logString += '\nEnded in state: ' + str(nextState)
        logString += '\nGot reward: ' + str(reward) + '\n'
        logging.debug(logString)

        # Update learner.
        if (isinstance(agent, ReinforcementAgent)):
            agent.observeTransition(state, action, nextState, reward)

        returns += reward * totalDiscount
        totalDiscount *= discount

    if (isinstance(agent, ReinforcementAgent)):
        agent.stopEpisode()

def parseOptions(argv):
    """
    Processes the command used to run gridworld from the command line.
    """

    description = """
    DESCRIPTION:
        This program will create a gridworld. Explore and find the best path to the reward!

    EXAMPLES:
        (1) python -m pacai.bin.gridworld
            - Creats a gridworld with default settings.
        (2) python -m pacai.bin.gridworld --discount 0.7
            - Creats a gridworld with a 0.7 discount factor.
    """

    parser = argparse.ArgumentParser(description = textwrap.dedent(description),
        prog = os.path.basename(__file__), formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument('-a', '--agent', dest = 'agent',
            action = 'store', type = str, default = 'random',
            help = 'agent type (options are \'random\', \'value\' and \'q\', default %(default)s)')

    parser.add_argument('-d', '--debug', dest = 'debug',
            action = 'store_true', default = False,
            help = 'set logging level to debug (default: %(default)s)')

    parser.add_argument('-e', '--epsilon', dest = 'epsilon',
            action = 'store', type = float, default = 0.3,
            help = 'chance of taking a random action in q-learning (default %(default)s)')

    parser.add_argument('-g', '--grid', dest = 'grid',
            action = 'store', type = str, default = 'BookGrid',
            help = 'grid type: BookGrid, BridgeGrid, CliffGrid, MazeGrid, %(default)s (default)')

    parser.add_argument('-i', '--iterations', dest = 'iters',
            action = 'store', type = int, default = 10,
            help = 'number of rounds of value iteration (default %(default)s)')

    parser.add_argument('-k', '--episodes', dest = 'episodes',
            action = 'store', type = int, default = 1,
            help = 'number of epsiodes of the MDP to run (default %(default)s)')

    parser.add_argument('-l', '--learning-rate', dest = 'learningRate',
            action = 'store', type = float, default = 0.5,
            help = 'set the learning rate (default %(default)s)')

    parser.add_argument('-n', '--noise', dest = 'noise',
            action = 'store', type = float, default = 0.2,
            help = 'set how often actions result in unintended directions (default %(default)s)')

    parser.add_argument('-p', '--pause', dest = 'pause',
            action = 'store_true', default = False,
            help = 'pause GUI after each time step when running the MDP (default %(default)s)')

    parser.add_argument('-q', '--quiet', dest = 'quiet',
            action = 'store_true', default = False,
            help = 'set logging level to warning (default: %(default)s)')

    parser.add_argument('-r', '--living-reward', dest = 'livingReward',
            action = 'store', type = float, default = 0.0,
            help = 'reward for living for a time step (default %(default)s)')

    parser.add_argument('-s', '--speed', dest = 'speed',
            action = 'store', type = float, default = 1.0,
            help = 'speed of animation, S>1.0 is faster, 0<S<1 is slower (default %(default)s)')

    parser.add_argument('-v', '--value-steps', dest = 'valueSteps',
            action = 'store_true', default = False,
            help = 'display each step of value iteration (default %(default)s)')

    parser.add_argument('-y', '--discount', dest = 'discount',
            action = 'store', type = float, default = 0.9,
            help = 'discount on future (default %(default)s)')

    parser.add_argument('--manual', dest = 'manual',
            action = 'store_true', default = False,
            help = 'manually control agent (default %(default)s)')

    parser.add_argument('--null-graphics', dest = 'nullGraphics',
            action = 'store_true', default = False,
            help = 'generate no graphics (default: %(default)s)')

    parser.add_argument('--text-graphics', dest = 'textGraphics',
            action = 'store_true', default = False,
            help = 'display output as text only (default: %(default)s)')

    parser.add_argument('--window-size', dest = 'gridSize',
            action = 'store', type = int, default = 150,
            help = 'request a window width of X pixels *per grid cell* (default %(default)s)')

    options, otherjunk = parser.parse_known_args(argv)

    if len(otherjunk) != 0:
        raise ValueError('Unrecognized options: \'%s\'.' % (str(otherjunk)))

    # Set the logging level
    if options.quiet and options.debug:
        raise ValueError('Logging cannont be set to both debug and quiet.')

    if options.quiet:
        updateLoggingLevel(logging.WARNING)
    elif options.debug:
        updateLoggingLevel(logging.DEBUG)

    if options.manual and options.agent != 'q':
        logging.info('Disabling Agents in Manual Mode.')
        options.agent = None

    # MANAGE CONFLICTS
    if options.textGraphics or options.nullGraphics:
        options.pause = False

    if options.manual:
        options.pause = True

    return options

def main(argv):
    """
    Entry point for the gridworld simulation
    The args are a blind pass of `sys.argv` with the executable stripped.
    """

    initLogging()

    opts = parseOptions(argv)

    ###########################
    # GET THE GRIDWORLD
    ###########################

    mdp = _getGridWorld(opts.grid)
    mdp.setLivingReward(opts.livingReward)
    mdp.setNoise(opts.noise)
    env = GridworldEnvironment(mdp)

    ###########################
    # GET THE DISPLAY ADAPTER
    ###########################

    display = TextGridworldDisplay(mdp)
    if not opts.textGraphics and not opts.nullGraphics:
        from pacai.ui.gridworld.gui import GraphicsGridworldDisplay
        display = GraphicsGridworldDisplay(mdp, opts.gridSize, opts.speed)

    display.start()

    ###########################
    # GET THE AGENT
    ###########################

    a = None
    if (opts.agent == 'value'):
        a = ValueIterationAgent(0, mdp, opts.discount, opts.iters)
    elif (opts.agent == 'q'):
        qLearnOpts = {
            'gamma': opts.discount,
            'alpha': opts.learningRate,
            'epsilon': opts.epsilon,
            'actionFn': lambda state: mdp.getPossibleActions(state),
        }
        a = QLearningAgent(0, **qLearnOpts)
    elif (opts.agent == 'random'):
        # No reason to use the random agent without episodes.
        if (opts.episodes == 0):
            opts.episodes = 10

        class RandomMDPAgent:
            def getAction(self, state):
                return random.choice(mdp.getPossibleActions(state))

            def getValue(self, state):
                return 0.0

            def getQValue(self, state, action):
                return 0.0

            def getPolicy(self, state):
                "NOTE: 'random' is a special policy value; don't use it in your code."
                return 'random'

            def update(self, state, action, nextState, reward):
                pass

        a = RandomMDPAgent()
    else:
        if (not opts.manual):
            raise 'Unknown agent type: ' + opts.agent

    ###########################
    # RUN EPISODES
    ###########################

    # Display q/v values before simulation of episodes.
    if (not opts.manual and opts.agent == 'value'):
        if (opts.valueSteps):
            for i in range(opts.iters):
                tempAgent = ValueIterationAgent(0, mdp, opts.discount, i)
                display.displayValues(tempAgent, message = 'VALUES AFTER ' + str(i) + ' ITERATIONS')
                display.pause()

        display.displayValues(a, message = 'VALUES AFTER ' + str(opts.iters) + ' ITERATIONS')
        display.pause()
        display.displayQValues(a, message = 'Q-VALUES AFTER ' + str(opts.iters) + ' ITERATIONS')
        display.pause()

    # Figure out what to display each time step (if anything).
    displayCallback = lambda x: None
    if (not opts.nullGraphics):
        if (opts.manual and opts.agent is None):
            displayCallback = lambda state: display.displayNullValues(state)
        else:
            if (opts.agent == 'random'):
                displayCallback = lambda state: display.displayValues(a, state, 'CURRENT VALUES')
            elif (opts.agent == 'value'):
                displayCallback = lambda state: display.displayValues(a, state, 'CURRENT VALUES')
            elif (opts.agent == 'q'):
                displayCallback = lambda state: display.displayQValues(a, state, 'CURRENT Q-VALUES')

    messageCallback = lambda x: print(x)
    if (opts.nullGraphics):
        messageCallback = lambda x: None

    # FIGURE OUT WHETHER TO WAIT FOR A KEY PRESS AFTER EACH TIME STEP
    pauseCallback = lambda: None
    if (opts.pause):
        pauseCallback = lambda: display.pause()

    # Figure out whether the user wants manual control (for debugging and demos).
    if (opts.manual):
        decisionCallback = lambda state: getUserAction(state, mdp.getPossibleActions)
    else:
        decisionCallback = a.getAction

    # Run episodes.
    if (opts.episodes > 0):
        logging.debug('RUNNING ' + str(opts.episodes) + ' EPISODES')

    returns = 0
    for episode in range(1, opts.episodes + 1):
        returns += runEpisode(a, env, opts.discount, decisionCallback, displayCallback,
                messageCallback, pauseCallback, episode)

    if (opts.episodes > 0):
        logging.debug('AVERAGE RETURNS FROM START STATE:' + str((returns + 0.0) / opts.episodes))

    # Display post-learning values / q-values.
    if (opts.agent == 'q' and not opts.manual):
        display.displayQValues(a, message = 'Q-VALUES AFTER ' + str(opts.episodes) + ' EPISODES')
        display.pause()
        display.displayValues(a, message = 'VALUES AFTER ' + str(opts.episodes) + ' EPISODES')
        display.pause()

def _getGridWorld(name):
    name = name.lower()

    grid = None
    if (name == 'bookgrid'):
        grid = BOOK_GRID
    elif (name == 'bridgegrid'):
        grid = BRIDGE_GRID
    elif (name == 'cliffgrid'):
        grid = CLIFF_GRID
    elif (name == 'cliff2grid'):
        grid = CLIFF2_GRID
    elif (name == 'discountgrid'):
        grid = DISCOUNT_GRID
    elif (name == 'mazegrid'):
        grid = MAZE_GRID
    else:
        raise ValueError("Unknown grid name: '%s'." % (name))

    return Gridworld(grid)

BOOK_GRID = [
    [' ', ' ', ' ', +1],
    [' ', '#', ' ', -1],
    ['S', ' ', ' ', ' '],
]

BRIDGE_GRID = [
    ['#', -100, -100, -100, -100, -100, '#'],
    [1, 'S', ' ', ' ', ' ', ' ', 10],
    ['#', -100, -100, -100, -100, -100, '#'],
]

CLIFF_GRID = [
    [' ', ' ', ' ', ' ', ' '],
    ['S', ' ', ' ', ' ', 10],
    [-100, -100, -100, -100, -100],
]

CLIFF2_GRID = [
    [' ', ' ', ' ', ' ', ' '],
    [8, 'S', ' ', ' ', 10],
    [-100, -100, -100, -100, -100],
]

DISCOUNT_GRID = [
    [' ', ' ', ' ', ' ', ' '],
    [' ', '#', ' ', ' ', ' '],
    [' ', '#', 1, '#', 10],
    ['S', ' ', ' ', ' ', ' '],
    [-10, -10, -10, -10, -10],
]

MAZE_GRID = [
    [' ', ' ', ' ', +1],
    ['#', '#', ' ', '#'],
    [' ', '#', ' ', ' '],
    [' ', '#', '#', ' '],
    ['S', ' ', ' ', ' '],
]

if __name__ == '__main__':
    main(sys.argv[1:])
