import abc

from pacai.agents.base import BaseAgent
from pacai.util import containers

class ValueEstimationAgent(BaseAgent):
    """
    Abstract agent which assigns values to (state,action)
    Q-Values for an environment. As well as a value to a
    state and a policy given respectively by,

    V(s) = max_{a in actions} Q(s,a)
    policy(s) = arg_max_{a in actions} Q(s,a)

    Both ValueIterationAgent and QLearningAgent inherit
    from this agent. While a ValueIterationAgent has
    a model of the environment via a MarkovDecisionProcess
    (see mdp.py) that is used to estimate Q-Values before
    ever actually acting, the QLearningAgent estimates
    Q-Values while acting in the environment.
    """

    def __init__(self, index, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining = 10):
        """
        Sets options, which can be passed in via the Pacman command line using -a alpha=0.5,...
        alpha - learning rate
        epsilon - exploration rate
        gamma - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """

        super().__init__(index)

        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discountRate = float(gamma)
        self.numTraining = int(numTraining)

    ############################
    # Override These Functions #
    ############################

    @abc.abstractmethod
    def getQValue(self, state, action):
        """
        Should return Q(state,action)
        """

        pass

    @abc.abstractmethod
    def getValue(self, state):
        """
        What is the value of this state under the best action?
        Concretely, this is given by

        V(s) = max_{a in actions} Q(s,a)
        """

        pass

    @abc.abstractmethod
    def getPolicy(self, state):
        """
        What is the best action to take in the state. Note that because
        we might want to explore, this might not coincide with getAction
        Concretely, this is given by

        policy(s) = arg_max_{a in actions} Q(s,a)

        If many actions achieve the maximal Q-value,
        it doesn't matter which is selected.
        """

        pass

    @abc.abstractmethod
    def getAction(self, state):
        """
        state: can call state.getLegalActions()
        Choose an action and return it.
        """

        pass
