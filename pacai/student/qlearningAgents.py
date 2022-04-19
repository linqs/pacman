from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection
from collections import Counter
import random

class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.self.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        self.values = Counter()
        # You can initialize Q-values here.

    def getQValue(self, state, action):
        # print("getqvalue called")
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """
        if (state, action) not in self.values:
            self.values[(state, action)] = 0.0
        return self.values[(state, action)]
        # return the q value and 0 if there isnt a q value for that state action pair yet

    def getValue(self, state):
        # print("getvalue called")
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """
        maxq = float("-inf")
        q = 0
        if len(self.getLegalActions(state)) == 0:  # if there are no actions return 0
            return 0.0
        for action in self.getLegalActions(state):
            # find the best q value from all the possible actions
            q = self.getQValue(state, action)
            if q > maxq:  # if q is better than the max make q the max
                maxq = q
        return maxq

    def getPolicy(self, state):
        # print("getpolicy called")
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """
        maxAction = None
        actions = self.getLegalActions(state)
        qvals = []
        maxActions = []
        for action in actions:
            qvals.append(self.getQValue(state, action))
        i = 0
        for q in qvals:
            # need to randomize the action taken if there is a tie
            # for the best action so it doesnt get stuck and do the same thing over and over
            if q == max(qvals):  # find all the actions that are tied for the max q value
                maxActions.append(actions[i])
                maxAction = actions[i]
            i += 1
        if len(maxActions) - 1 >= 0:  # return a random action that tied for best q value
            return maxActions[random.randint(0, len(maxActions) - 1)]
        else:
            return maxAction  # if there were no legal actions return none

    def getAction(self, state):
        if random.randint(1, 100) <= 100 * self.getEpsilon():  # return a random action
            return random.choice(self.getLegalActions(state))
        else:
            return self.getPolicy(state)  # return the optimal policy

    def update(self, state, action, nextState, reward):
        self.values[(state, action)] = (
            1 - self.getAlpha()) * self.getQValue(state, action) + self.getAlpha() * (
            reward + self.getDiscountRate() * self.getValue(nextState))
        # (1 - alpha) * Q(s, a) + alpha[R(s, a, s') + max_a'(Q(s', a'))] (getValue computes max Q)

class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index,
            extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)()
        self.weights = Counter()
        # You might want to initialize weights here.

    def getQValue(self, state, action):
        q = 0
        for feature in self.featExtractor.getFeatures(state, action):
            # dot product of w and featureVector
            q += self.weights[feature] * self.featExtractor.getFeatures(state, action)[feature]
        return q

    def update(self, state, action, nextState, reward):
        correction = (
            reward + self.getDiscountRate() * self.getValue(nextState)) - self.getQValue(
            state, action)
        # (R(s,a) + gammaV(s')) - Q(s,a)
        newWeight = self.getAlpha() * correction  # alpha * correction
        features = self.featExtractor.getFeatures(state, action)
        # have to set it as a variable to avoid weird error
        for feature in features:
            self.weights[feature] = self.weights[feature] + newWeight * features[feature]
            # w_i = w_i + newWeight * f_i(s,a)

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            # *** Your Code Here ***
            pass
