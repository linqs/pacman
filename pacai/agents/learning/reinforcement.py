import abc
import logging
import time

from pacai.agents.learning.value import ValueEstimationAgent

class ReinforcementAgent(ValueEstimationAgent):
    """
    An abstract value estimation agent that learns by estimating Q-values from experience.

    You should know the following:
    The environment will call `ReinforcementAgent.observeTransition`,
    which will then call `ReinforcementAgent.update` (which you should override).
    Use `ReinforcementAgent.getLegalActions` to know which actions are available in a state.
    """

    def __init__(self, index, actionFn = None, numTraining = 100, epsilon = 0.5,
            alpha = 0.5, gamma = 1, **kwargs):
        """
        Args:
            actionFn: A function which takes a state and returns the list of legal actions.
            alpha: The learning rate.
            epsilon: The exploration rate.
            gamma: The discount factor.
            numTraining: The number of training episodes.
        """
        super().__init__(index)

        if (actionFn is None):
            actionFn = lambda state: state.getLegalActions()

        self.actionFn = actionFn
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discountRate = float(gamma)

    @abc.abstractmethod
    def update(self, state, action, nextState, reward):
        """
        This class will call this function after observing a transition and reward.
        """

        pass

    def getAlpha(self):
        return self.alpha

    def getDiscountRate(self):
        return self.discountRate

    def getEpsilon(self):
        return self.epsilon

    def getGamma(self):
        return self.discountRate

    def getLegalActions(self, state):
        """
        Get the actions available for a given state.
        This is what you should use to obtain legal actions for a state.
        """

        return self.actionFn(state)

    def observeTransition(self, state, action, nextState, deltaReward):
        """
        Called by environment to inform agent that a transition has been observed.
        This will result in a call to `ReinforcementAgent.update` on the same arguments.
        You should not directly call this function (the environment will).
        """

        self.episodeRewards += deltaReward
        self.update(state, action, nextState, deltaReward)

    def startEpisode(self):
        """
        Called by environment when a new episode is starting.
        """

        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def stopEpisode(self):
        """
        Called by environment when an episode is done.
        """

        if (self.episodesSoFar < self.numTraining):
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards

        self.episodesSoFar += 1
        if (self.episodesSoFar >= self.numTraining):
            # Take off the training wheels.
            self.epsilon = 0.0  # No exploration.
            self.alpha = 0.0  # No learning.

    def isInTraining(self):
        return (self.episodesSoFar < self.numTraining)

    def isInTesting(self):
        return not self.isInTraining()

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setLearningRate(self, alpha):
        self.alpha = alpha

    def setDiscount(self, discount):
        self.discountRate = discount

    def doAction(self, state, action):
        """
        Called by inherited class when an action is taken in a state.
        """

        self.lastState = state
        self.lastAction = action

    def observationFunction(self, state):
        """
        This is where we ended up after our last action.
        """

        if self.lastState is not None:
            reward = state.getScore() - self.lastState.getScore()
            self.observeTransition(self.lastState, self.lastAction, state, reward)

    def registerInitialState(self, state):
        self.startEpisode()
        if self.episodesSoFar == 0:
            logging.debug('Beginning %d episodes of Training' % (self.numTraining))

    def final(self, state):
        """
        Called by Pacman game at the terminal state.
        """

        deltaReward = state.getScore() - self.lastState.getScore()
        self.observeTransition(self.lastState, self.lastAction, state, deltaReward)
        self.stopEpisode()

        if ('episodeStartTime' not in self.__dict__):
            self.episodeStartTime = time.time()

        if ('lastWindowAccumRewards' not in self.__dict__):
            self.lastWindowAccumRewards = 0.0

        self.lastWindowAccumRewards += state.getScore()

        NUM_EPS_UPDATE = 100
        if (self.episodesSoFar % NUM_EPS_UPDATE == 0):
            logging.debug('Reinforcement Learning Status:')
            windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)

            if (self.episodesSoFar <= self.numTraining):
                trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
                logging.debug('\tCompleted %d out of %d training episodes' %
                        (self.episodesSoFar, self.numTraining))
                logging.debug('\tAverage Rewards over all training: %.2f' % (trainAvg))
            else:
                testAvg = float(self.accumTestRewards) / (self.episodesSoFar - self.numTraining)
                logging.debug('\tCompleted %d test episodes' %
                        (self.episodesSoFar - self.numTraining))
                logging.debug('\tAverage Rewards over testing: %.2f' % (testAvg))

            logging.info('\tAverage Rewards for last %d episodes: %.2f' %
                    (NUM_EPS_UPDATE, windowAvg))
            logging.info('\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime))

            self.lastWindowAccumRewards = 0.0
            self.episodeStartTime = time.time()

        if (self.episodesSoFar == self.numTraining):
            msg = 'Training Done (turning off epsilon and alpha)'
            logging.debug('%s\n%s' % (msg, '-' * len(msg)))
