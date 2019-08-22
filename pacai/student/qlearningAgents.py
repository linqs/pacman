from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import util

# Force the extractors into scope for util.lookup().
# TODO(eriq): I hate util.lookup(), get rid of it and this import.
from pacai.util import featureExtractors

class QLearningAgent(ReinforcementAgent):
    """
    Q-Learning Agent

    Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discountRate (discount rate)

    Functions you should use
        - self.getLegalActions(state) which returns legal actions for a state

    Methods to Implement:

    def getQValue(self, state, action):
        Returns Q(state,action)
        Should return 0.0 if we never seen
        a state or (state,action) tuple

    def getValue(self, state):
        Returns max_action Q(state,action)
        where the max is over legal actions. Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.

    def getPolicy(self, state):
        Compute the best action to take in a state. Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.

    def getAction(self, state):
        Compute the action to take in the current state. With
        probability self.epsilon, we should take a random action and
        take the best policy action otherwise. Note that if there are
        no legal actions, which is the case at the terminal state, you
        should choose None as the action.

        HINT: You might want to use util.flipCoin(prob)
        HINT: To pick randomly from a list, use random.choice(list)
        
    def update(self, state, action, nextState, reward):
        The parent class calls this to observe a state = action => nextState
        and reward transition. You should do your Q-Value update here

        NOTE: You should never call this function,
        it will be called on your behalf
        
    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index, **args):
        """
        You can initialize Q-values here...
        """

        super().__init__(index, **args)

class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as QLearningAgent, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
                python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha - learning rate
        epsilon - exploration rate
        gamma - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """

        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining

        super().__init__(index, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman. Do not change or remove this
        method.
        """

        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    ApproximateQLearningAgent

    You should only have to overwrite getQValue
    and update. All other QLearningAgent functions
    should work as is.

    Methods to Implement:

    def getQValue(self, state, action):
        Should return Q(state,action) = w * featureVector
        where * is the dotProduct operator

    def update(self, state, action, nextState, reward):
        Should update your weights based on transition
        
    DESCRIPTION: <Write something here so we know what you did.>    
    """

    def __init__(self, index, extractor = 'IdentityExtractor', **args):
        super().__init__(index, **args)
        self.featExtractor = util.lookup()()

        # You might want to initialize weights here.

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            util.raiseNotDefined()
