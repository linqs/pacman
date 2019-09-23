# TODO(eriq): There is a lot of overlap with graphicsDisplay.py.

import os

from pacai.ui import graphicsUtils
from pacai.ui import graphicsConstants
from pacai.ui.pacmanDisplay import AbstractPacmanGraphics
from pacai.ui.pacmanDisplay import AbstractPane

class CaptureInfoPane(AbstractPane):
    def __init__(self, layout, gridSize, redTeam, blueTeam):
        self.redTeam = redTeam
        self.blueTeam = blueTeam
        super().__init__(layout, gridSize)
        self.drawPane()

    def drawPane(self):
        self.scoreText = graphicsUtils.text(self.toScreen(0, 0), self.textColor,
                self._infoString(0, 1200), graphicsConstants.DEFAULT_FONT, self.fontSize,
            graphicsConstants.TEXT_MOD_BOLD)
        self.redText = graphicsUtils.text(self.toScreen(230, 0), graphicsConstants.TEAM_COLORS[0],
                self._redScoreString(), graphicsConstants.DEFAULT_FONT, self.fontSize,
            graphicsConstants.TEXT_MOD_BOLD)
        self.redText = graphicsUtils.text(self.toScreen(690, 0), graphicsConstants.TEAM_COLORS[1],
                self._blueScoreString(), graphicsConstants.DEFAULT_FONT, self.fontSize,
            graphicsConstants.TEXT_MOD_BOLD)

    def _redScoreString(self):
        return "RED: % 10s " % (self.redTeam[:12])

    def _blueScoreString(self):
        return "BLUE: % 10s " % (self.blueTeam[:12])

    def updateRedText(self, score):
        graphicsUtils.changeText(self.redText, self._redScoreString())

    def updateBlueText(self, score):
        graphicsUtils.changeText(self.blueText, self._blueScoreString())

    def _infoString(self, score, timeleft):
        return "SCORE: % 4d, TIME: % 4d" % (score, timeleft)

    def updateScore(self, score, timeleft):
        graphicsUtils.changeText(self.scoreText, self._infoString(score, timeleft))

class CapturePacmanGraphics(AbstractPacmanGraphics):
    def __init__(self, redTeam, blueTeam, zoom=graphicsConstants.DEFAULT_ZOOM,
                frameTime = graphicsConstants.DEFAULT_FRAME_TIME,
                capture = graphicsConstants.DEFAULT_CAPTURE_ARG,
                gif = graphicsConstants.DEFAULT_GIF_ARG,
                gifSkipFrames = graphicsConstants.DEFAULT_GIF_FRAME_SKIP,
                gifFps = graphicsConstants.DEFAULT_GIF_FPS):
        super().__init__(zoom, frameTime, capture, gif, gifSkipFrames, gifFps)
        self.redTeam = redTeam
        self.blueTeam = blueTeam

    # implemented abstract method.
    def startGraphics(self, state):
        self.layout = state.getInitialLayout()
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.makeWindow(self.width, self.height)
        self.infoPane = CaptureInfoPane(layout, self.gridSize, self.redTeam, self.blueTeam)
        self.currentState = layout

    def update(self, newState):
        self.frame += 1

        agentIndex = newState.getLastAgentMoved()
        agentState = newState.getAgentState(agentIndex)

        if (self.agentImages[agentIndex][0].isPacman() != agentState.isPacman()):
            self.swapImages(agentIndex, agentState)

        prevState, prevImage = self.agentImages[agentIndex]
        if (agentState.isPacman()):
            self.animatePacman(agentState, prevState, prevImage)
        else:
            self.moveGhost(agentState, agentIndex, prevState, prevImage)
        self.agentImages[agentIndex] = (agentState, prevImage)

        if (newState.getLastFoodEaten() is not None):
            self.removeFood(newState.getLastFoodEaten(), self.food)

        if (newState.getLastCapsuleEaten() is not None):
            self.removeCapsule(newState.getLastCapsuleEaten(), self.capsules)

        self.infoPane.updateScore(newState.getScore(), newState.getTimeleft())
        if ('ghostDistances' in dir(newState)):
            self.infoPane.updateGhostDistances(newState.ghostDistances)

        self.saveFrame()

    def clearDebug(self):
        if 'expandedCells' in dir(self) and len(self.expandedCells) > 0:
            for cell in self.expandedCells:
                graphicsUtils.remove_from_screen(cell)

    def debugDraw(self, cells, color=[1.0, 0.0, 0.0], clear=False):
        if clear:
            self.clearDebug()
            self.expandedCells = []

        for k, cell in enumerate(cells):
            screenPos = self.toScreen(cell)
            cellColor = graphicsUtils.formatColor(*color)
            block = graphicsUtils.square(screenPos, 0.5 * self.gridSize,
                    color = cellColor, filled = 1, behind = 2)
            self.expandedCells.append(block)
            if self.frameTime < 0:
                graphicsUtils.refresh()

# Saving graphical output
# -----------------------
# Note: to make an animated gif from this postscript output, try the command:
# convert -delay 7 -loop 1 -compress lzw -layers optimize frame* out.gif
# convert is part of imagemagick (freeware)

SAVE_POSTSCRIPT = False
POSTSCRIPT_OUTPUT_DIR = 'frames'
FRAME_NUMBER = 0

def saveFrame():
    "Saves the current graphical output as a postscript file"
    global SAVE_POSTSCRIPT, FRAME_NUMBER, POSTSCRIPT_OUTPUT_DIR

    if not SAVE_POSTSCRIPT:
        return

    if not os.path.exists(POSTSCRIPT_OUTPUT_DIR):
        os.mkdir(POSTSCRIPT_OUTPUT_DIR)

    name = os.path.join(POSTSCRIPT_OUTPUT_DIR, 'frame_%08d.ps' % FRAME_NUMBER)
    FRAME_NUMBER += 1
    graphicsUtils.writePostscript(name)  # writes the current canvas
