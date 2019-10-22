import math
import sys

from pacai.core.distance import manhattan

DEFAULT_DISTANCE = 10000

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

        if math.isclose(pos1[0], int(pos1[0])) and math.isclose(pos1[1], int(pos1[1])):
            if math.isclose(pos2[0], int(pos2[0])) and math.isclose(pos2[1], int(pos2[1])):
                return self.getDistanceOnGrid(pos1, pos2)

        pos1Grids = self.getGrids2D(pos1)
        pos2Grids = self.getGrids2D(pos2)
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

    def getGrids2D(self, pos):
        grids = grid1Dx = grid1Dy = []
        intX = int(pos[0])
        intY = int(pos[1])
        if math.isclose(pos[0], intX):
            grid1Dx = [(intX, 0)]
        else:
            grid1Dx = [(intX, pos[0] - intX), (intX + 1, intX + 1 - pos[0])]
            
        if math.isclose(pos[1], intY):
            grid1Dy = [(intY, 0)]
        else:
            grid1Dy = [(intY, pos[1] - intY), (intY + 1, intY + 1 - pos[1])]
            
        for x, xDistance in grid1Dx:
            for y, yDistance in grid1Dy:
                grids.append(((x, y), xDistance + yDistance))
                
        return grids

    def computeDistances(self, layout):

        distances = {}
        allNodes = layout.walls.asList(False)

        for source in allNodes:
            dist = {}
            closed = []

            for node in allNodes:
                dist[node] = sys.maxsize

            adjacent = [source]
            dist[source] = 0

            while len(adjacent) != 0:
                node = adjacent.pop(0)
                if node in closed:
                    continue
                closed += [node]
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
                    if dist[other] > dist[node] + 1:
                        dist[other] = dist[node] + 1
            for target in allNodes:
                distances[(target, source)] = dist[target]

        return distances
