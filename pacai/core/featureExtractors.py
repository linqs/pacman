# Feature extractors for Pacman game states and a private search problem to find
# the closest food.

import abc

from pacai.core.actions import Actions
from pacai.core.search import search
from pacai.student.searchAgents import AnyFoodSearchProblem
from pacai.util import counter

class FeatureExtractor(abc.ABC):
    @abc.abstractmethod
    def getFeatures(self, state, action):
        """
        Returns a dict from features to counts
        Usually, the count will just be 1.0 for
        indicator functions.
        """

        pass

class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = counter.Counter()
        feats[(state, action)] = 1.0

        return feats

class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
        - whether food will be eaten
        - how far away the next food is
        - whether a ghost collision is imminent
        - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # Extract the grid of food and wall locations and get the ghost locations.
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = counter.Counter()

        features["bias"] = 1.0

        # Compute the location of pacman after he takes the action.
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # Count the number of ghosts 1-step away.
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in
                Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # If there is no danger of ghosts then add the food feature.
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        prob = AnyFoodSearchProblem(state, start = (next_x, next_y))
        dist = len(search.bfs(prob))
        if dist is not None:
            # Make the distance a number less than one otherwise the update will diverge wildly.
            features["closest-food"] = float(dist) / (walls.getWidth() * walls.getHeight())

        features.divideAll(10.0)
        return features
