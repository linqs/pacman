import sys

from pacai.core.distance import manhattan
from pacai.util import priorityQueue

DEFAULT_DISTANCE = 10000

class Distancer(object):
    """
    A class for computing and caching the shortest path between any two points in a given maze.

    Example:
    ```
    distancer = Distancer(gameState.getInitialLayout())
    distancer.getDistance((1, 1), (10, 10))
    ```
    """

    def __init__(self, layout):
        self._distances = None
        self.dc = DistanceCalculator(layout, self)

    def getMazeDistances(self):
        self.dc.run()

    def getDistance(self, pos1, pos2):
        """
        The only function you will need after you create the object.
        """

        if (self._distances is None):
            return manhattan(pos1, pos2)

        if isInt(pos1) and isInt(pos2):
            return self.getDistanceOnGrid(pos1, pos2)

        pos1Grids = getGrids2D(pos1)
        pos2Grids = getGrids2D(pos2)
        bestDistance = DEFAULT_DISTANCE

        for pos1Snap, snap1Distance in pos1Grids:
            for pos2Snap, snap2Distance in pos2Grids:
                gridDistance = self.getDistanceOnGrid(pos1Snap, pos2Snap)
                distance = gridDistance + snap1Distance + snap2Distance
                if bestDistance > distance:
                    bestDistance = distance

        return bestDistance

    def getDistanceOnGrid(self, pos1, pos2):
        key = (pos1, pos2)
        if key in self._distances:
            return self._distances[key]

        raise Exception("Position not in grid: " + str(key))

    def isReadyForMazeDistance(self):
        return (self._distances is not None)

def isInt(pos):
    x, y = pos
    return x == int(x) and y == int(y)

def getGrids2D(pos):
    grids = []
    for x, xDistance in getGrids1D(pos[0]):
        for y, yDistance in getGrids1D(pos[1]):
            grids.append(((x, y), xDistance + yDistance))
    return grids

def getGrids1D(x):
    intX = int(x)
    if x == int(x):
        return [(x, 0)]
    return [(intX, x - intX), (intX + 1, intX + 1 - x)]

##########################################
# MACHINERY FOR COMPUTING MAZE DISTANCES #
##########################################

distanceMap = {}

class DistanceCalculator:
    def __init__(self, layout, distancer):
        self.layout = layout
        self.distancer = distancer
        self.cache = {}

    def run(self):
        if self.layout.walls not in self.cache:
            self.cache[self.layout.walls] = computeDistances(self.layout)

        self.distancer._distances = self.cache[self.layout.walls]

def computeDistances(layout):
    """
    Runs UCS to all other positions from each position.
    """

    distances = {}
    allNodes = layout.walls.asList(False)

    for source in allNodes:
        dist = {}
        closed = {}

        for node in allNodes:
            dist[node] = sys.maxsize

        queue = priorityQueue.PriorityQueue()
        queue.push(source, 0)
        dist[source] = 0

        while not queue.isEmpty():
            node = queue.pop()
            if node in closed:
                continue

            closed[node] = True
            nodeDist = dist[node]
            adjacent = []
            x, y = node

            if not layout.isWall((x, y + 1)):
                adjacent.append((x, y + 1))

            if not layout.isWall((x, y - 1)):
                adjacent.append((x, y - 1))

            if not layout.isWall((x + 1, y)):
                adjacent.append((x + 1, y))

            if not layout.isWall((x - 1, y)):
                adjacent.append((x - 1, y))

            for other in adjacent:
                if other not in dist:
                    continue

                oldDist = dist[other]
                newDist = nodeDist + 1
                if newDist < oldDist:
                    dist[other] = newDist
                    queue.push(other, newDist)

        for target in allNodes:
            distances[(target, source)] = dist[target]

    return distances

def getDistanceOnGrid(distances, pos1, pos2):
    key = (pos1, pos2)
    if key in distances:
        return distances[key]

    return DEFAULT_DISTANCE
