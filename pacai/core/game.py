"""
The core of a pacman-style game.
"""

import logging
import time

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

    def run(self):
        """
        Main control loop for game play.
        """

        self.numMoves = 0

        agentIndex = self.startingIndex
        numAgents = len(self.agents)

        self.display.initialize(self.state)

        if (not self._registerInitialState()):
            return False

        # Draw the initial frame.
        self.display.update(self.state)

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

            # Track progress.
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
