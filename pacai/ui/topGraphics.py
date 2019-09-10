from pacai.ui import graphicsUtils
from pacai.ui import graphicsConstants
from abc import ABC, abstractmethod

class Pane(ABC):
    @abstractmethod
    def drawPane(self):
        pass

    @abstractmethod
    def updateScore(self, score):
        pass

    def toScreen(self, pos, y = None):
        """
        Translates a point relative from the bottom left of the info pane.
        """

        if (y is None):
            x, y = pos
        else:
            x = pos

        x = self.gridSize + x  # Margin
        y = self.base + y
        return x, y

    def initializeGhostDistances(self, distances):
        self.ghostDistanceText = []

        size = 20
        if self.width < 240:
            size = 12
        if self.width < 160:
            size = 10

        for i, d in enumerate(distances):
            t = graphicsUtils.text(self.toScreen(self.width / 2 + self.width / 8 * i, 0),
                    graphicsConstants.GHOST_COLORS[i + 1], d, "Times", size, "bold")
            self.ghostDistanceText.append(t)

    def setTeam(self, isBlue):
        text = "RED TEAM"
        if isBlue:
            text = "BLUE TEAM"

        self.teamText = graphicsUtils.text(self.toScreen(300, 0), self.textColor, text, "Times",
                self.fontSize, "bold")

    def updateGhostDistances(self, distances):
        if len(distances) == 0:
            return

        if 'ghostDistanceText' not in dir(self):
            self.initializeGhostDistances(distances)
        else:
            for i, d in enumerate(distances):
                graphicsUtils.changeText(self.ghostDistanceText[i], d)

    def drawGhost(self):
        pass

    def drawPacman(self):
        pass

    def drawWarning(self):
        pass

    def clearIcon(self):
        pass

    def updateMessage(self, message):
        pass

    def clearMessage(self):
        pass
