import abc

from pacai.agents.base import BaseAgent

class ValueEstimationAgent(BaseAgent):
    """
    An abstract agent which assigns Q-values to (state, action) pairs.
    The best values and policies are estimated by:
    ```
    V(state) = max_{action in actions} Q(state ,action)
    policy(state) = arg_max_{action in actions} Q(state, action)
    ```
    """

    def __init__(self, index, alpha = 1.0, epsilon = 0.05,
            gamma = 0.8, numTraining = 10, **kwargs):
        """
        Args:
            alpha: The learning rate.
            epsilon: The exploration rate.
            gamma: The discount factor.
            numTraining: The number of training episodes.
        """

        super().__init__(index)

        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discountRate = float(gamma)
        self.numTraining = int(numTraining)

    @abc.abstractmethod
    def getQValue(self, state, action):
        """
        Should return Q(state,action).
        """

        pass

    @abc.abstractmethod
    def getValue(self, state):
        """
        What is the value of this state under the best action?
        Concretely, this is given by:
        ```
        V(state) = max_{action in actions} Q(state ,action)
        ```
        """

        pass

    @abc.abstractmethod
    def getPolicy(self, state):
        """
        What is the best action to take in the state?
        Note that because we might want to explore,
        this might not coincide with `ValueEstimationAgent.getAction`.
        Concretely, this is given by:
        ```
        policy(state) = arg_max_{action in actions} Q(state, action)
        ```
        If many actions achieve the maximal Q-value,
        it doesn't matter which is selected.
        """

        pass
