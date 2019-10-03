class Directions:
    """
    The different directions that agents can move in.
    Agents can only move in cardinal directions.
    In addition to the cardinal directions, there is also STOP,
    indicating an agent should not move.
    """

    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {
        NORTH: WEST,
        SOUTH: EAST,
        EAST: NORTH,
        WEST: SOUTH,
        STOP: STOP,
    }

    RIGHT = dict([(y, x) for x, y in sorted(list(LEFT.items()))])

    REVERSE = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST,
        STOP: STOP
    }

    CARDINAL = [
        NORTH,
        SOUTH,
        EAST,
        WEST,
    ]
