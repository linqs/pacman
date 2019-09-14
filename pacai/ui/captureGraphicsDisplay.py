# TODO(eriq): There is a lot of overlap with graphicsDisplay.py.

import os

from pacai.ui import graphicsUtils
from pacai.ui import graphicsConstants
from pacai.ui.pacmanDisplay import AbstractPane
from pacai.ui.pacmanDisplay import AbstractPacmanGraphics

class CaptureInfoPane(AbstractPane):
    def __init__(self, layout, gridSize, redTeam, blueTeam):
        self.redTeam = redTeam
        self.blueTeam = blueTeam
        super().__init__(layout, gridSize)
        self.drawPane()

    def drawPane(self):
        self.scoreText = graphicsUtils.text(self.toScreen(0, 0), self.textColor,
                self._infoString(0, 1200), "Consolas", self.fontSize, "bold")
        self.redText = graphicsUtils.text(self.toScreen(230, 0), graphicsConstants.TEAM_COLORS[0],
                self._redScoreString(), "Consolas", self.fontSize, "bold")
        self.redText = graphicsUtils.text(self.toScreen(690, 0), graphicsConstants.TEAM_COLORS[1],
                self._blueScoreString(), "Consolas", self.fontSize, "bold")

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
    def __init__(self, redTeam, blueTeam, zoom=1.0, frameTime=0.0, capture=False,
            gif = None, gif_skip_frames = 0, gif_fps = 10):
        super().__init__(zoom, frameTime, capture, gif, gif_skip_frames, gif_fps)
        self.redTeam = redTeam
        self.blueTeam = blueTeam

    # implemented abstract method.
    def startGraphics(self, state):
        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.infoPane = CaptureInfoPane(layout, self.gridSize, self.redTeam, self.blueTeam)
        self.currentState = layout

    # Implemented abstract method.
    def update(self, newState):
        self.frame += 1

        agentIndex = newState._agentMoved
        agentState = newState.agentStates[agentIndex]

        if (self.agentImages[agentIndex][0].isPacman != agentState.isPacman):
            self.swapImages(agentIndex, agentState)

        prevState, prevImage = self.agentImages[agentIndex]
        if (agentState.isPacman):
            self.animatePacman(agentState, prevState, prevImage)
        else:
            self.moveGhost(agentState, agentIndex, prevState, prevImage)
        self.agentImages[agentIndex] = (agentState, prevImage)

        if (newState._foodEaten is not None):
            self.removeFood(newState._foodEaten, self.food)

        if (newState._capsuleEaten is not None):
            self.removeCapsule(newState._capsuleEaten, self.capsules)

        self.infoPane.updateScore(newState.score, newState.timeleft)
        if ('ghostDistances' in dir(newState)):
            self.infoPane.updateGhostDistances(newState.ghostDistances)

        self.save_frame()

    def clearDebug(self):
        if 'expandedCells' in dir(self) and len(self.expandedCells) > 0:
            for cell in self.expandedCells:
                graphicsUtils.remove_from_screen(cell)

    def debugDraw(self, cells, color=[1.0, 0.0, 0.0], clear=False):
        if clear:
            self.clearDebug()
            self.expandedCells = []

        for k, cell in enumerate(cells):
            screenPos = self.to_screen(cell)
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
