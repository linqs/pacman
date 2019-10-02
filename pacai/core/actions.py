from pacai.core.directions import Directions

class Actions:
    """
    A collection of static methods for manipulating move actions.
    An action is just a `pacai.core.directions.Directions`.
    """

    # Directions
    _directions = {
        Directions.NORTH: (0, 1),
        Directions.SOUTH: (0, -1),
        Directions.EAST: (1, 0),
        Directions.WEST: (-1, 0),
        Directions.STOP: (0, 0),
    }

    _directionsAsList = sorted(list(_directions.items()))

    TOLERANCE = 0.001

    @staticmethod
    def reverseDirection(action):
        if (action == Directions.NORTH):
            return Directions.SOUTH
        elif (action == Directions.SOUTH):
            return Directions.NORTH
        elif (action == Directions.EAST):
            return Directions.WEST
        elif (action == Directions.WEST):
            return Directions.EAST
        else:
            return action

    @staticmethod
    def vectorToDirection(vector):
        dx, dy = vector
        if (dy > 0):
            return Directions.NORTH
        elif (dy < 0):
            return Directions.SOUTH
        elif (dx < 0):
            return Directions.WEST
        elif (dx > 0):
            return Directions.EAST
        else:
            return Directions.STOP

    @staticmethod
    def directionToVector(direction, speed = 1.0):
        dx, dy = Actions._directions[direction]
        return (dx * speed, dy * speed)

    @staticmethod
    def getPossibleActions(position, direction, walls):
        x, y = position
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight.
        if (abs(x - x_int) + abs(y - y_int) > Actions.TOLERANCE):
            return [direction]

        possible = []
        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx

            if (not walls[next_x][next_y]):
                possible.append(dir)

        return possible

    @staticmethod
    def getLegalNeighbors(position, walls):
        x, y = position
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        neighbors = []
        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_x = x_int + dx
            if (next_x < 0 or next_x == walls.getWidth()):
                continue

            next_y = y_int + dy
            if (next_y < 0 or next_y == walls.getHeight()):
                continue

            if (not walls[next_x][next_y]):
                neighbors.append((next_x, next_y))

        return neighbors

    @staticmethod
    def getSuccessor(position, action):
        dx, dy = Actions.directionToVector(action)
        x, y = position
        return (x + dx, y + dy)
