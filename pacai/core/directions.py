class Directions:
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
        EAST,
        SOUTH,
        WEST,
    ]
