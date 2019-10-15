ARROWS = {
    'west': '←',
    'north': '↑',
    'east': '→',
    'south': '↓',
    'random': '?',
}

class TextGridworldDisplay(object):
    """
    A text display for gridworld.
    """

    def __init__(self, gridworld):
        self.gridworld = gridworld

    def start(self):
        pass

    def pause(self):
        pass

    def displayValues(self, agent, currentState = None, message = None):
        grid = self.gridworld.grid

        displayGrid = []
        maxGridWidth = 0

        if (message is not None):
            print(message)

        for y in range(grid.height - 1, -1, -1):
            row = []
            for x in range(0, grid.width, 1):
                state = (x, y)

                gridType = grid[x][y]
                value = agent.getValue(state)
                policy = agent.getPolicy(state)

                value = "%0.4f %s" % (value, self._getArrow(policy))

                isTerminal = isinstance(gridType, int)
                isCurrent = (currentState == state)

                cellText = self._formatCell(gridType, value, isCurrent, isTerminal)
                if (len(cellText) > maxGridWidth):
                    maxGridWidth = len(cellText)

                row.append(cellText)

            displayGrid.append(row)

        self._printGrid(displayGrid, maxGridWidth)
        print()

    def displayNullValues(self, agent, currentState = None, message = None):
        raise RuntimeError("Manual control requires a GUI display.")

    def displayQValues(self, agent, currentState = None, message = None):
        grid = self.gridworld.grid

        displayGrid = []
        maxGridWidth = 0

        if (message is not None):
            print(message)

        for y in range(grid.height - 1, -1, -1):
            row = []
            for x in range(0, grid.width, 1):
                state = (x, y)

                qValues = []
                for action in self.gridworld.getPossibleActions(state):
                    qValue = agent.getQValue(state, action)
                    qValues.append("%0.2f %s" % (qValue, self._getArrow(action)))

                values = ', '.join(qValues)

                gridType = grid[x][y]
                isTerminal = isinstance(gridType, int)
                isCurrent = (currentState == state)

                cellText = self._formatCell(gridType, values, isCurrent, isTerminal)
                if (len(cellText) > maxGridWidth):
                    maxGridWidth = len(cellText)

                row.append(cellText)

            displayGrid.append(row)

        self._printGrid(displayGrid, maxGridWidth)
        print()

    def _getArrow(self, direction):
        direction = direction.lower()

        if (direction in ARROWS):
            return ARROWS[direction]

        return direction

    def _printGrid(self, grid, maxGridWidth):
        if (len(grid) == 0):
            return

        formatString = "{:^%d}" % (maxGridWidth + 2)

        width = len(grid[0])
        textWidth = width * (maxGridWidth + 2 + 1) + 1

        print('-' * textWidth)

        for row in grid:
            for i in range(len(row)):
                row[i] = formatString.format(row[i])

            rowText = '|'.join(row)

            print('|%s|' % (rowText))
            print('-' * textWidth)

    def _formatCell(self, gridType, value, isCurrent, isTerminal):
        text = ''

        if (gridType == 'S'):
            text = 'Start'
        elif (gridType == '#'):
            text = '█████'
        elif (isinstance(gridType, int)):
            text = "[%d]" % (gridType)
        elif (isinstance(value, int)):
            text = str(value)
        elif (isinstance(value, float)):
            text = '%0.4f' % (value)
        else:
            text = str(value)

        if (isCurrent):
            text = '* ' + text

        if (isTerminal):
            text = text + ' Exit'

        return text.strip()
