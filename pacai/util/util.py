"""
Functions that could be used for various course projects.
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
