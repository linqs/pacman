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

        return self.getDistanceOnGrid(self.round2D(pos1), self.round2D(pos2))

    def getDistanceOnGrid(self, pos1, pos2):
        key = (pos1, pos2)
        if key in self._distances:
            return self._distances[key]

        raise Exception("Position not in grid: " + str(key))

    def round2D(self, pos):
        intX = int(pos[0])
        intY = int(pos[1])
        deltaX = float(abs(pos[0] - intX))
        deltaY = float(abs(pos[1] - intY))

        if deltaX >= 0.5 and deltaY >= 0.5:
            return (intX + 1, intY + 1)
        elif deltaX < 0.5 and deltaY >= 0.5:
            return (intX, intY + 1)
        elif deltaX >= 0.5 and deltaY < 0.5:
            return (intX + 1, intY)
        else:
            return (intX, intY)

    def computeDistances(self, layout):

        distances = {}
        allNodes = layout.walls.asList(False)

        for source in allNodes:
            dist = {}
            closed = []

            for node in allNodes:
                dist[node] = DEFAULT_DISTANCE

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
