import inspect
import signal
import sys

"""
Functions useful for various course projects
"""

def nearestPoint(pos):
    """
    Finds the nearest grid point to a position (discretizes).
    """

    (current_row, current_col) = pos

    grid_row = int(current_row + 0.5)
    grid_col = int(current_col + 0.5)
    return (grid_row, grid_col)

def sign(x):
    """
    Returns 1 or -1 depending on the sign of x
    """

    if (x >= 0):
        return 1
    else:
        return -1

def arrayInvert(array):
    """
    Inverts a matrix stored as a list of lists.
    """

    result = [[] for i in array]
    for outer in array:
        for inner in range(len(outer)):
            result[inner].append(outer[inner])

    return result

def matrixAsList(matrix, value = True):
    """
    Turns a matrix into a list of coordinates matching the specified value
    """

    rows, cols = len(matrix), len(matrix[0])
    cells = []
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == value:
                cells.append((row, col))

    return cells

def raiseNotDefined():
    print("Method not implemented: %s" % inspect.stack()[1][3])
    sys.exit(1)

# Code to handle timeouts.
class TimeoutFunctionException(Exception):
    """
    Exception to raise on a timeout
    """

    pass

class TimeoutFunction:
    def __init__(self, function, timeout):
        self.timeout = timeout
        self.function = function

    def handle_timeout(self, signum, frame):
        raise TimeoutFunctionException()

    def __call__(self, *args):
        if 'SIGALRM' not in dir(signal):
            return self.function(*args)
        old = signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.timeout)
        try:
            result = self.function(*args)
        finally:
            signal.signal(signal.SIGALRM, old)

        signal.alarm(0)
        return result
