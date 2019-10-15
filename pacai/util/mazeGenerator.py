"""
Maze Generator

Algorithm:
 - Start with an empty grid.
 - Draw a wall with gaps, dividing the grid in 2.
 - Repeat recursively for each sub-grid.

Pacman Details:
 - Players 1 and 3 always start in the bottom left; 2 and 4 in the top right.
 - Food is placed in dead ends and then randomly
    (though not too close to the pacmen starting positions).

Notes:
 - The final map includes a symmetric, flipped copy.
 - The first wall has k gaps, the next wall has k / 2 gaps, etc. (min=1).

@author: Dan Gillick
@author: Jie Tang
"""

import logging
import random
import sys

WALL = '%'
FOOD = '.'
CAPSULE = 'o'
EMPTY = ' '

MAX_DIFFERENT_MAZES = 10000

class Maze(object):
    def __init__(self, rows, cols, anchor=(0, 0), root=None):
        """
        Generate an empty maze.
        Anchor is the top left corner of this grid's position in its parent grid.
        """

        self.r = rows
        self.c = cols
        self.grid = [[EMPTY for col in range(cols)] for row in range(rows)]
        self.anchor = anchor
        self.rooms = []

        self.root = root
        if not self.root:
            self.root = self

    def to_map(self):
        """
        Add a flipped symmetric copy on the right.
        Add a border.
        """

        # Add a flipped symmetric copy
        for row in range(self.r):
            for col in range(self.c - 1, -1, -1):
                self.grid[self.r - row - 1].append(self.grid[row][col])
        self.c *= 2

        # Add a border
        for row in range(self.r):
            self.grid[row] = [WALL] + self.grid[row] + [WALL]
        self.c += 2

        self.grid.insert(0, [WALL for c in range(self.c)])
        self.grid.append([WALL for c in range(self.c)])
        self.r += 2

    def __str__(self):
        s = ''

        for row in range(self.r):
            for col in range(self.c):
                s += self.grid[row][col]
            s += '\n'

        return s[:-1]

    def add_wall(self, rng, i, gaps=1, vert=True):
        """
        Add a wall with gaps.
        """

        add_r, add_c = self.anchor
        if vert:
            gaps = min(self.r, gaps)
            slots = [add_r + x for x in range(self.r)]
            if 0 not in slots:
                if self.root.grid[min(slots) - 1][add_c + i] == EMPTY:
                    slots.remove(min(slots))

                if len(slots) <= gaps:
                    return 0
            if (self.root.c - 1) not in slots:
                if self.root.grid[max(slots) + 1][add_c + i] == EMPTY:
                    slots.remove(max(slots))

            if len(slots) <= gaps:
                return 0

            rng.shuffle(slots)
            for row in slots[int(round(gaps)):]:
                self.root.grid[row][add_c + i] = WALL

            self.rooms.append(Maze(self.r, i, (add_r, add_c), self.root))
            self.rooms.append(Maze(self.r, self.c - i - 1, (add_r, add_c + i + 1), self.root))
        else:
            gaps = min(self.c, gaps)
            slots = [add_c + x for x in range(self.c)]

            if 0 not in slots:
                if self.root.grid[add_r + i][min(slots) - 1] == EMPTY:
                    slots.remove(min(slots))

                if len(slots) <= gaps:
                    return 0

            if (self.root.r - 1) not in slots:
                if self.root.grid[add_r + i][max(slots) + 1] == EMPTY:
                    slots.remove(max(slots))

            if len(slots) <= gaps:
                return 0

            rng.shuffle(slots)
            for col in slots[int(round(gaps)):]:
                self.root.grid[add_r + i][col] = WALL

            self.rooms.append(Maze(i, self.c, (add_r, add_c), self.root))
            self.rooms.append(Maze(self.r - i - 1, self.c, (add_r + i + 1, add_c), self.root))

        return 1

def make_with_prison(rng, room, depth, gaps=1, vert=True, min_width=1, gapfactor=0.5):
    """
    Build a maze with 0,1,2 layers of prison (randomly).
    """

    p = rng.randint(0, 2)
    proll = rng.random()
    if proll < 0.5:
        p = 1
    elif proll < 0.7:
        p = 0
    elif proll < 0.9:
        p = 2
    else:
        p = 3

    add_r, add_c = room.anchor
    for j in range(p):
        cur_col = 2 * (j + 1) - 1
        for row in range(room.r):
            room.root.grid[row][cur_col] = WALL

        if j % 2 == 0:
            room.root.grid[0][cur_col] = EMPTY
        else:
            room.root.grid[room.r - 1][cur_col] = EMPTY

    room.rooms.append(Maze(room.r, room.c - (2 * p), (add_r, add_c + (2 * p)), room.root))
    for sub_room in room.rooms:
        make(rng, sub_room, depth + 1, gaps, vert, min_width, gapfactor)

    return 2 * p

def make(rng, room, depth, gaps=1, vert=True, min_width=1, gapfactor=0.5):
    """
    Recursively build a maze.
    """

    # Extreme base case
    if room.r <= min_width and room.c <= min_width:
        return

    # Decide between vertical and horizontal wall
    if vert:
        num = room.c
    else:
        num = room.r

    if num < min_width + 2:
        vert = not vert
        if vert:
            num = room.c
        else:
            num = room.r

    # Add a wall to the current room
    if depth == 0:
        wall_slots = [num - 2]  # Fix the first wall
    else:
        wall_slots = range(1, num - 1)

    if len(wall_slots) == 0:
        return

    choice = rng.choice(wall_slots)
    if not room.add_wall(rng, choice, gaps, vert):
        return

    # Recursively add walls
    for sub_room in room.rooms:
        make(rng, sub_room, depth + 1, max(1, gaps * gapfactor), not vert, min_width, gapfactor)

def copy_grid(grid):
    new_grid = []

    for row in range(len(grid)):
        new_grid.append([])
        for col in range(len(grid[row])):
            new_grid[row].append(grid[row][col])

    return new_grid

def add_pacman_stuff(rng, maze, max_food=60, max_capsules=4, toskip=0):
    """
    Add pacmen starting position.
    Add food at dead ends plus some extra.
    """

    # Parameters
    max_depth = 2

    # Add food at dead ends
    depth = 0
    total_food = 0

    while True:
        new_grid = copy_grid(maze.grid)
        depth += 1
        num_added = 0

        for row in range(1, maze.r - 1):
            for col in range(1 + toskip, int(maze.c / 2) - 1):
                if (row > maze.r - 6) and (col < 6):
                    continue

                if maze.grid[row][col] != EMPTY:
                    continue

                neighbors = 0
                neighbors += (maze.grid[row - 1][col] == EMPTY)
                neighbors += (maze.grid[row][col - 1] == EMPTY)
                neighbors += (maze.grid[row + 1][col] == EMPTY)
                neighbors += (maze.grid[row][col + 1] == EMPTY)

                if neighbors == 1:
                    new_grid[row][col] = FOOD
                    new_grid[maze.r - row - 1][maze.c - col - 1] = FOOD
                    num_added += 2
                    total_food += 2

        maze.grid = new_grid
        if num_added == 0:
            break

        if depth >= max_depth:
            break

    # Starting pacmen positions
    maze.grid[maze.r - 2][1] = '3'
    maze.grid[maze.r - 3][1] = '1'
    maze.grid[1][maze.c - 2] = '4'
    maze.grid[2][maze.c - 2] = '2'

    # Add capsules
    total_capsules = 0
    while (total_capsules < max_capsules):
        row = rng.randint(1, maze.r - 1)
        col = rng.randint(1 + toskip, int(maze.c / 2) - 2)

        if (row > maze.r - 6) and (col < 6):
            continue

        if (abs(col - int(maze.c / 2)) < 3):
            continue

        if maze.grid[row][col] == EMPTY:
            maze.grid[row][col] = CAPSULE
            maze.grid[maze.r - row - 1][maze.c - col - 1] = CAPSULE
            total_capsules += 2

    # Extra random food
    while (total_food < max_food):
        row = rng.randint(1, maze.r - 1)
        col = rng.randint(1 + toskip, int(maze.c / 2) - 1)

        if (row > maze.r - 6) and (col < 6):
            continue

        if (abs(col - int(maze.c / 2)) < 3):
            continue

        if maze.grid[row][col] == EMPTY:
            maze.grid[row][col] = FOOD
            maze.grid[maze.r - row - 1][maze.c - col - 1] = FOOD
            total_food += 2

def generateMaze(seed = None):
    rng = random.Random()
    if seed is None:
        seed = rng.randint(1, MAX_DIFFERENT_MAZES)
    logging.debug('Seed value for Maze Generation: ' + str(seed))

    rng.seed(seed)
    maze = Maze(16, 16)
    gapfactor = min(0.65, rng.gauss(0.5, 0.1))
    skip = make_with_prison(rng, maze, depth=0, gaps=3, vert=True, min_width=1, gapfactor=gapfactor)
    maze.to_map()
    add_pacman_stuff(rng, maze, 2 * (maze.r * int(maze.c / 20)), 4, skip)

    return str(maze)

if __name__ == '__main__':
    seed = None
    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
    print(generateMaze(seed))
