# TODO(eriq): There is a lot of overlap with captureGraphicsDisplay.py.

import os

from pacai.ui import graphicsUtils
from pacai.ui import graphicsConstants
from pacai.ui.topGraphics import absPane
from pacai.ui.topGraphics import absPacmanGraphics

class InfoPane(absPane):
    def __init__(self, layout, gridSize):
        self.gridSize = gridSize
        self.width = (layout.width) * gridSize
        self.base = (layout.height + 1) * gridSize
        self.height = graphicsConstants.INFO_PANE_HEIGHT
        self.fontSize = 24
        self.textColor = graphicsConstants.PACMAN_COLOR
        self.drawPane()

    def drawPane(self):
        self.scoreText = graphicsUtils.text(self.toScreen(0, 0), self.textColor,
                "SCORE:    0", "Times", self.fontSize, "bold")

    def updateScore(self, score):
        graphicsUtils.changeText(self.scoreText, "SCORE: % 4d" % score)

class PacmanGraphics(absPacmanGraphics):
    def __init__(self, zoom = 1.0, frameTime = 0.0, capture = False,
            gif = None, gif_skip_frames = 0, gif_fps = 10):
        self.have_window = 0
        self.currentGhostImages = {}
        self.pacmanImage = None
        self.zoom = zoom
        self.gridSize = graphicsConstants.DEFAULT_GRID_SIZE * zoom
        self.capture = capture
        self.frameTime = frameTime

        self.gif_path = gif
        self.gif_skip_frames = gif_skip_frames
        self.gif_fps = gif_fps
        self.frame = 0
        self.frame_images = []

    def startGraphics(self, state):
        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.infoPane = InfoPane(layout, self.gridSize)
        self.currentState = layout

    def update(self, newState):
        self.frame += 1

        agentIndex = newState._agentMoved
        agentState = newState.agentStates[agentIndex]

        if (self.agentImages[agentIndex][0].isPacman != agentState.isPacman):
            self.swapImages(agentIndex, agentState)

        prevState, prevImage = self.agentImages[agentIndex]
        if agentState.isPacman:
            self.animatePacman(agentState, prevState, prevImage)
        else:
            self.moveGhost(agentState, agentIndex, prevState, prevImage)
        self.agentImages[agentIndex] = (agentState, prevImage)

        if newState._foodEaten is not None:
            self.removeFood(newState._foodEaten, self.food)

        if newState._capsuleEaten is not None:
            self.removeCapsule(newState._capsuleEaten, self.capsules)

        self.infoPane.updateScore(newState.score)
        if 'ghostDistances' in dir(newState):
            self.infoPane.updateGhostDistances(newState.ghostDistances)

        self.save_frame()

class FirstPersonPacmanGraphics(PacmanGraphics):
    def __init__(self, zoom = 1.0, showGhosts = True, capture = False, frameTime=0):
        super().__init__(zoom, frameTime=frameTime)
        self.showGhosts = showGhosts
        self.capture = capture

    def initialize(self, state, isBlue = False):

        self.isBlue = isBlue
        PacmanGraphics.startGraphics(self, state)
        # Initialize distribution images
        self.layout = state.layout

        # Draw the rest
        self.distributionImages = None  # initialize lazily
        self.drawStaticObjects(state)
        self.drawAgentObjects(state)

        # Information
        self.previousState = state

    def getGhostColor(self, ghost, ghostIndex):
        return graphicsConstants.GHOST_COLORS[ghostIndex]

    def getPosition(self, ghostState):
        if not self.showGhosts and not ghostState.isPacman and ghostState.getPosition()[1] > 1:
            return (-1000, -1000)
        else:
            return PacmanGraphics.getPosition(self, ghostState)

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
