from pacai.core.actions import getLegalNeighbors
from pacai.core.distance import manhattan

class Distancer(object):
    """
    This file contains a Distancer object which computes and
    caches the shortest path between any two points in a given maze.
    Example:
    distancer = Distancer(gameState.getInitialLayout())
    distancer.getDistance((1, 1), (10, 10))
    """

    def __init__(self, layout):
        """
        Initialize with Distancer (layout).
        """
        self._distances = None
        self.layout = layout
        self.cache = {}

    def getMazeDistance(self):
        if self.layout.walls not in self.cache:
            self.cache[self.layout.walls] = self.computeDistances(self.layout)

        self._distances = self.cache[self.layout.walls]

    def getDistance(self, pos1, pos2):
        """
        The getDistance function is the only one you'll need after you create the object.
        """
        if (self._distances is None):
            return manhattan(pos1, pos2)
        
        key = ((round(pos1[0]), round(pos1[1])), (round(pos2[0]), round(pos2[1])))
        if key in self._distances:
            return self._distances[key]

        raise Exception("Position not in grid: " + str(key))

    def computeDistances(self, layout):
        """
        layout.walls.asList(False) returns the positions on a layout that are not walls.
        """
        positions = layout.walls.asList(False) 
        distances = {}
        
        for startPosition in positions:
            queue = [startPosition]
            distances[(startPosition, startPosition)] = 0

            while len(queue) != 0:
                previousPosition = queue.pop(0)
                queue += Actions.getLegalNeighbors(previousPosition, layout.walls)
                oldDist = distances[(previousPosition, startPosition)]
                for other in queue:
                    if distances[(other, startPosition)] > oldDist + 1:
                        distances[(other, startPosition)] = oldDist + 1

        return distances
