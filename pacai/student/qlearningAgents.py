from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection
from pacai.util.probability import flipCoin
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

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
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

        # You can initialize Q-values here.
        # qValues = {} : {state -> action} -> int
        self.qValues = {}

    def update(self, state, action, nextState, reward):
        if state not in self.qValues:
            self.qValues[state] = {}
        if action not in self.qValues[state]:
            self.qValues[state][action] = 0.0

        # newQValue = oldValue + alpha *((reward + (discount * futureQValue)) - oldValue)
        #           = (1 - a)qold + a(r + y * qnew)
        q_old = self.qValues[state][action]
        alpha = self.getAlpha()
        y = self.getDiscountRate()
        q_next = self.getValue(nextState)

        self.qValues[state][action] = q_old + alpha * (reward + y * q_next - q_old)

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        if not legalActions:
            return 0.0
        if(flipCoin(self.getEpsilon())):
            return random.choice(legalActions)
        else:
            return self.getPolicy(state)

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """
        if(state not in self.qValues
           or action not in self.qValues[state]):
            return 0.0

        return self.qValues[state][action]

    def getValue(self, state):
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
        legalActions = self.getLegalActions(state)
        if not legalActions:
            return 0.0

        return max([self.getQValue(state, action) for action in legalActions])

    def getPolicy(self, state):
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
        legalActions = self.getLegalActions(state)
        if not legalActions:
            return 0.0

        vaList = [(self.getQValue(state, action), action) for action in legalActions]
        return max(vaList, key=lambda x: x[0])[1]

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
        self.featExtractor = reflection.qualifiedImport(extractor)

        # You might want to initialize weights here.
        self.weights = {}

    def getQValue(self, state, action):
        res = 0
        for sa, v in self.featExtractor.getFeatures(self.featExtractor, state, action).items():
            if sa not in self.weights:
                self.weights[sa] = 0
            res += self.weights[sa] * v
        return res

    def update(self, state, action, nextState, reward):
        # newQValue = oldValue + alpha *((reward + (discount * futureQValue)) - oldValue)
        #           = (1 - a)qold + a(r + y * qnew)
        alpha = self.getAlpha()
        y = self.getDiscountRate()
        correction = reward + y * self.getValue(nextState) - self.getQValue(state, action)
        for sa, v in self.featExtractor.getFeatures(self.featExtractor, state, action).items():
            if sa not in self.weights:
                self.weights[sa] = 0
            self.weights[sa] += alpha * correction * v

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
            print(self.weights.values())
            return
