from pacai.agents.learning.value import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    * Please read pacai.agents.learning before reading this.*

    A ValueIterationAgent takes a Markov decision process
    (see mdp.py) on initialization and runs value iteration
    for a given number of iterations using the supplied
    discount factor.

    Methods to Implement:

    def getQValue(self, state, action):
        The q-value of the state action pair(after the indicated number
        of value iteration passes). Note that value iteration does not
        necessarily create this quantity and you may have to derive it
        on the fly.

    def getPolicy(self, state):
        The policy is the best action in the given state
        according to the values computed by value iteration.
        You may break ties any way you see fit.
        Note that if there are no legal actions, which is the case at the
        terminal state, you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100):
        """
        Your value iteration agent should take an mdp on
        construction, run the indicated number of iterations
        and then act according to the resulting policy.

        Some useful mdp methods you will use:
            mdp.getStates()
            mdp.getPossibleActions(state)
            mdp.getTransitionStatesAndProbs(state, action)
            mdp.getReward(state, action, nextState)
        """

        super().__init__(index)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dict to store Q-values for a state

        """
        Description:
        [Enter a description of what you did here.]
        """

        """ YOUR CODE HERE """
        raise NotImplementedError()
        """ END CODE """

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values[state]

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)
