class Grid:
    """
    A 2-dimensional array of objects backed by a list of lists.
    Data is accessed via grid[x][y] where (x, y) are positions on a Pacman map with x horizontal,
    y vertical and the origin (0, 0) in the bottom left corner.
    """

    def __init__(self, width, height, initialValue = False):
        if (not isinstance(initialValue, bool)):
            raise ValueError('Grids can only contain booleans')

        self._width = width
        self._height = height
        self._data = [[initialValue for y in range(height)] for x in range(width)]

    def asList(self, key = True):
        values = []

        for x in range(self._width):
            for y in range(self._height):
                if self[x][y] == key:
                    values.append((x, y))

        return values

    def copy(self):
        grid = Grid(self._width, self._height)
        grid._data = [row.copy() for row in self._data]
        return grid

    def count(self, item =True):
        return sum([x.count(item) for x in self._data])

    def deepCopy(self):
        return self.copy()

    def getHeight(self):
        return self._height

    def getWidth(self):
        return self._width

    def shallowCopy(self):
        grid = Grid(self._width, self._height)
        grid._data = self._data
        return grid

    def _cellIndexToPosition(self, index):
        x = index / self._height
        y = index % self._height

        return x, y

    def __eq__(self, other):
        if (other is None):
            return False

        return self._data == other._data

    def __getitem__(self, i):
        return self._data[i]

    def __hash__(self):
        hashcode = 0
        base = 1

        for row in self._data:
            for value in row:
                if (value):
                    hashcode += base
                base *= 2

        return hash(hashcode)

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __setitem__(self, key, item):
        self._data[key] = item

    def __str__(self):
        out = [[str(self._data[x][y])[0] for x in range(self._width)] for y in range(self._height)]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])
