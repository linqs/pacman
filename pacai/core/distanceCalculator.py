"""
This file contains a Distancer object which computes and
caches the shortest path between any two points in a given maze.

Example:
distancer = Distancer(gameState.getInitialLayout())
distancer.getDistance((1, 1), (10, 10))
"""

import sys

from pacai.core.distance import manhattan
from pacai.util import priorityQueue

DEFAULT_DISTANCE = 10000

class Distancer(object):
    def __init__(self, layout):
        """
        Initialize with Distancer (layout).
        """

        self._distances = None
        self.dc = DistanceCalculator(layout, self)

    def getMazeDistances(self):
        self.dc.run()

    def getDistance(self, pos1, pos2):
        """
        The getDistance function is the only one you'll need after you create the object.
        """

        if (self._distances is None):
            return manhattan(pos1, pos2)

        if pos1 == int(pos1) and pos2 == int(pos2):
            return self.getDistanceOnGrid(pos1, pos2)

        pos1Grids = []
        xgrid1D = []
        ygrid1D = []
        intX = int(pos1[0])
        intY = int(pos1[1])
        if pos1[0] == intX:
            xgrid1D = [(pos1[0], 0)]
        else:
            xgrid1D = [(intX, pos1[0] - intX), (intX + 1, intX + 1 - pos1[0])]
        for x, xDistance in xgrid1D:
            if pos1[1] == intY:
                ygrid1D = [(pos1[1], 0)]
            else:
                ygrid1D = [(intY, pos1[1] - intY), (intY + 1, intX + 1 - pos1[1])]
            for y, yDistance in ygrid1D:
                pos1Grids.append(((x, y), xDistance + yDistance))

        pos2Grids = []
        xgrid1D = []
        ygrid1D = []
        intX = int(pos2[0])
        intY = int(pos2[1])
        if pos2[0] == intX:
            xgrid1D = [(pos2[0], 0)]
        else:
            xgrid1D = [(intX, pos2[0] - intX), (intX + 1, intX + 1 - pos2[0])]
        for x, xDistance in xgrid1D:
            if pos2[1] == intY:
                ygrid1D = [(pos2[1], 0)]
            else:
                ygrid1D = [(intY, pos2[1] - intY), (intY + 1, intX + 1 - pos2[1])]
            for y, yDistance in ygrid1D:
                pos2Grids.append(((x, y), xDistance + yDistance))

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
