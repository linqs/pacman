# TODO(eriq): There is a lot of overlap with captureGraphicsDisplay.py.

import os

from pacai.ui import graphicsUtils
from pacai.ui import graphicsConstants
from pacai.ui.pacmanDisplay import AbstractPacmanGraphics
from pacai.ui.pacmanDisplay import AbstractPane

class InfoPane(AbstractPane):
    def __init__(self, layout, gridSize):
        super().__init__(layout, gridSize)
        self.drawPane()

    def drawPane(self):
        self.scoreText = graphicsUtils.text(self.toScreen(0, 0), self.textColor,
                "SCORE:    0", graphicsConstants.DEFAULT_FONT, self.fontSize, graphicsConstants.TEXT_MOD_BOLD)

    def updateScore(self, score):
        graphicsUtils.changeText(self.scoreText, "SCORE: % 4d" % score)

class PacmanGraphics(AbstractPacmanGraphics):
    def __init__(self, zoom = 1.0, frameTime = 0.0, capture = False,
                gif = None, gif_skip_frames = 0, gif_fps = 10):
        super().__init__(zoom, frameTime, capture, gif, gif_skip_frames, gif_fps)

    def startGraphics(self, state):
        self.layout = state.getInitialLayout()
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.makeWindow(self.width, self.height)
        self.infoPane = InfoPane(layout, self.gridSize)
        self.currentState = layout

    def update(self, newState):
        self.frame += 1

        agentIndex = newState.getLastAgentMoved()
        agentState = newState.getAgentState(agentIndex)

        if (self.agentImages[agentIndex][0].isPacman() != agentState.isPacman()):
            self.swapImages(agentIndex, agentState)

        prevState, prevImage = self.agentImages[agentIndex]
        if agentState.isPacman():
            self.animatePacman(agentState, prevState, prevImage)
        else:
            self.moveGhost(agentState, agentIndex, prevState, prevImage)
        self.agentImages[agentIndex] = (agentState, prevImage)

        if (newState.getLastFoodEaten() is not None):
            self.removeFood(newState.getLastFoodEaten(), self.food)

        if (newState.getLastCapsuleEaten() is not None):
            self.removeCapsule(newState.getLastCapsuleEaten(), self.capsules)

        self.infoPane.updateScore(newState.getScore())
        if 'ghostDistances' in dir(newState):
            self.infoPane.updateGhostDistances(newState.ghostDistances)

        self.saveFrame()

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
