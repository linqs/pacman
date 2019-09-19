"""
The core of a Pac-Man game.
"""

import logging
import time

from pacai.core.actions import Actions
from pacai.core.directions import Directions

class Configuration:
    """
    A Configuration holds the (x, y) coordinate of a character, along with its
    traveling direction.

    The convention for positions, like a graph, is that (0, 0) is the lower left corner,
    x increases horizontally and y increases vertically.
    Therefore, north is the direction of increasing y, or (0, 1).
    """

    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def getPosition(self):
        return (self.pos)

    def getDirection(self):
        return self.direction

    def isInteger(self):
        x, y = self.pos
        return x == int(x) and y == int(y)

    def __eq__(self, other):
        if (other is None):
            return False
        return (self.pos == other.pos and self.direction == other.direction)

    def __hash__(self):
        x = hash(self.pos)
        y = hash(self.direction)
        return hash(x + 13 * y)

    def __str__(self):
        return '(x,y)=' + str(self.pos) + ', ' + str(self.direction)

    def generateSuccessor(self, vector):
        """
        Generates a new configuration reached by translating the current configuration
        by the action vector.
        This is a low-level call and does not attempt to respect the legality of the movement.

        Actions are movement vectors.
        """

        x, y = self.pos
        dx, dy = vector

        direction = Actions.vectorToDirection(vector)
        if (direction == Directions.STOP):
            # There is no stop direction.
            direction = self.direction

        return Configuration((x + dx, y + dy), direction)

class AgentState:
    """
    AgentStates hold the state of an agent (configuration, speed, scared, etc).
    """

    def __init__(self, startConfiguration, isPacman):
        # Save the starting configuration for later use.
        self.start = startConfiguration
        self._startIsPacman = isPacman

        self.configuration = startConfiguration
        self._isPacman = isPacman
        self.scaredTimer = 0

    def __str__(self):
        if self._isPacman:
            return 'Pacman: ' + str(self.configuration)
        else:
            return 'Ghost: ' + str(self.configuration)

    def __eq__(self, other):
        if (other is None):
            return False
        return self.configuration == other.configuration and self.scaredTimer == other.scaredTimer

    def __hash__(self):
        return hash(hash(self.configuration) + 13 * hash(self.scaredTimer))

    def copy(self):
        state = AgentState(self.start, self._startIsPacman)

        state._isPacman = self._isPacman
        state.configuration = self.configuration
        state.scaredTimer = self.scaredTimer

        return state

    def getPosition(self):
        if (self.configuration is None):
            return None
        return self.configuration.getPosition()

    def getDirection(self):
        return self.configuration.getDirection()

    def isPacman(self):
        return self._isPacman

    def isGhost(self):
        return not self.isPacman()

    def isScared(self):
        return self.scaredTimer > 0

    def isScaredGhost(self):
        return self.isGhost() and self.isScared()

    def isBraveGhost(self):
        """
        A ghost that is not scared.
        """

        return self.isGhost() and not self.isScared()

    def setIsPacman(self, isPacman):
        self._isPacman = isPacman

    def respawn(self):
        """
        This agent was killed, respawn it at the start as a pacman.
        """

        self.configuration = self.start
        self._isPacman = self._startIsPacman
        self.scaredTimer = 0

class Game:
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, agents, display, rules, startingIndex = 0, catchExceptions = False):
        self.agentCrashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.startingIndex = startingIndex
        self.gameOver = False
        self.moveHistory = []
        self.totalAgentTimes = [0 for agent in agents]
        self.totalAgentTimeWarnings = [0 for agent in agents]
        self.agentTimeout = False

        self.enforceTimeouts = catchExceptions
        self.catchExceptions = catchExceptions

    def getProgress(self):
        if (self.gameOver):
            return 1.0
        else:
            return self.rules.getProgress(self)

    def run(self):
        """
        Main control loop for game play.
        """

        self.display.initialize(self.state)
        self.numMoves = 0

        if (not self._registerInitialState()):
            return False

        agentIndex = self.startingIndex
        numAgents = len(self.agents)

        while (not self.gameOver):
            # Fetch the next agent
            agent = self.agents[agentIndex]

            action = None
            startTime = time.time()

            # Get an action from the agent.
            try:
                agent.observationFunction(self.state)
                action = agent.getAction(self.state)
            except Exception as ex:
                if (not self.catchExceptions):
                    raise ex

                self._agentCrash(agentIndex, ex)
                return False

            timeTaken = time.time() - startTime
            self.totalAgentTimes[agentIndex] += timeTaken

            if (self._checkForTimeouts(agentIndex, timeTaken)):
                return False

            # Execute the action.
            self.moveHistory.append((agentIndex, action))
            try:
                self.state = self.state.generateSuccessor(agentIndex, action)
            except Exception as ex:
                if (not self.catchExceptions):
                    raise ex

                self._agentCrash(agentIndex, ex)
                return False

            # Update the display.
            self.display.update(self.state)

            # Allow for game specific conditions (winning, losing, etc.).
            self.rules.process(self.state, self)

            # Track progress
            if (agentIndex == numAgents + 1):
                self.numMoves += 1

            # Next agent.
            agentIndex = (agentIndex + 1) % numAgents

        if (not self._registerFinalState()):
            return False

        self.display.finish()

    def _agentCrash(self, agentIndex, exception = None):
        """
        Helper method for handling agent crashes.
        """

        logging.warning('Agent %d crashedtimed out on a single move!' % agentIndex,
                exc_info = exception)

        self.gameOver = True
        self.agentCrashed = True
        self.rules.agentCrash(self, agentIndex)

    def _checkForTimeouts(self, agentIndex, timeTaken):
        """
        Check if an agent timed out.
        Return: True if an agent times out.
        """

        if (not self.enforceTimeouts):
            return False

        # Check for a single move timeout (results in an instant loss).
        moveTimeout = self.rules.getMoveTimeout(agentIndex)
        if (timeTaken > moveTimeout):
            logging.warning('Agent %d timed out on a single move!' % agentIndex)
            self.agentTimeout = True
            self._agentCrash(agentIndex)
            return True

        # Check for a timeout warning (you get a few of theses).
        moveWarningTime = self.rules.getMoveWarningTime(agentIndex)
        if (timeTaken > moveWarningTime):
            self.totalAgentTimeWarnings[agentIndex] += 1
            logging.warning('Agent %d took too long to move! This is warning %d' %
                    (agentIndex, self.totalAgentTimeWarnings[agentIndex]))

            maxTimeouts = self.rules.getMaxTimeWarnings(agentIndex)
            if (self.totalAgentTimeWarnings[agentIndex] > maxTimeouts):
                logging.warning('Agent %d exceeded the maximum number of warnings: %d' %
                        (agentIndex, self.totalAgentTimeWarnings[agentIndex]))
                self.agentTimeout = True
                self._agentCrash(agentIndex)
                return True

        # Check if the agent has used too much time overall.
        maxTotalTime = self.rules.getMaxTotalTime(agentIndex)
        if (self.totalAgentTimes[agentIndex] > maxTotalTime):
            logging.warning('Agent %d ran out of time! (time: %1.2f)' %
                    (agentIndex, self.totalAgentTimes[agentIndex]))
            self.agentTimeout = True
            self._agentCrash(agentIndex)
            return True

        return False

    def _registerInitialState(self):
        """
        Inform agents of the game start.
        """

        for agentIndex in range(len(self.agents)):
            agent = self.agents[agentIndex]

            if (not agent):
                # this is a null agent, meaning it failed to load the other team wins.
                self._agentCrash(agentIndex)
                return False

            maxStartupTime = int(self.rules.getMaxStartupTime(agentIndex))
            startTime = time.time()

            try:
                agent.registerInitialState(self.state)
            except Exception as ex:
                if (not self.catchExceptions):
                    raise ex

                self._agentCrash(agentIndex, ex)
                return False

            timeTaken = time.time() - startTime
            self.totalAgentTimes[agentIndex] += timeTaken

            if (self.enforceTimeouts and timeTaken > maxStartupTime):
                logging.warning('Agent %d ran out of time on startup!' % agentIndex)
                self.agentTimeout = True
                self._agentCrash(agentIndex)
                return False

        return True

    def _registerFinalState(self):
        # Inform a learning agent of the game's result.
        for agent in self.agents:
            try:
                agent.final(self.state)
            except Exception as ex:
                if (not self.catchExceptions):
                    raise ex

                self._agentCrash(agent.index, ex)
                return False

        return True
