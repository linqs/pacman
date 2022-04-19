from pacai.agents.learning.value import ValueEstimationAgent
from collections import Counter
class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        states = mdp.getStates()
        self.values = Counter()  # A dictionary which holds the q-values for each state.
        # Compute the values here.
        for i in range(self.iters):
            # for each iteration (iters being the iterations passed into the function)
            temp = Counter()  # empty dictionary for updated q values
            for state in states:  # for each state
                actions = self.mdp.getPossibleActions(state)
                maxq = float("-inf")
                for action in actions:
                    q = self.getQValue(state, action)
                    if q > maxq:  # find the best action based on max q value
                        maxq = q
                        temp[state] = q  # update the q value in temp
            self.values = temp  # replace values with new updated values

    def getQValue(self, state, action):
        q = 0
        for transition in self.mdp.getTransitionStatesAndProbs(state, action):  # for ech transition
            reward = self.mdp.getReward(state, action, transition[0])  # R(s, a, s')
            q += transition[1] * (reward + self.discountRate * self.getValue(transition[0]))
            # sum T(s, a, s')  * [R(s, a, s') + gamma        * Vstar(s')]
            # transition[0] is the state, transition[1] is the probability
        return q

    def getPolicy(self, state):
        actions = self.mdp.getPossibleActions(state)
        maxq = float("-inf")
        maxAction = None
        for action in actions:  # for each action compute its q
            q = self.getQValue(state, action)
            if q > maxq:  # save the q value as maxq if it is the current biggest
                maxq = q
                maxAction = action  # save the action to return
        return maxAction

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
