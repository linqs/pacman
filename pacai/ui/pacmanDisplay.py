import math
import io

from abc import ABC
from abc import abstractmethod
from pacai.ui import graphicsUtils
from pacai.ui import graphicsConstants
from pacai.core.directions import Directions

class AbstractPane(ABC):

    @abstractmethod
    def drawPane(self):
        pass

    @abstractmethod
    def updateScore(self, score):
        pass

    def __init__(self, layout, gridSize):
        self.gridSize = gridSize
        self.width = layout.width * gridSize
        self.base = (layout.height + 1) * gridSize
        self.height = graphicsConstants.INFO_PANE_HEIGHT
        self.fontSize = graphicsConstants.DEFAULT_PANE_FONT_SIZE
        self.textColor = graphicsConstants.PACMAN_COLOR

    def toScreen(self, position, y = None):
        """
        Translates a point relative from the bottom left of the info pane.
        """

        if y is None:
            x, y = position
        else:
            x = position

        x = self.gridSize + x  # Margin
        y = self.base + y
        return x, y

    def initializeGhostDistances(self, distances):
        self.ghostDistanceText = []

        size = graphicsConstants.DEFAULT_TEXT_SIZE
        if self.width < 240:
            size = 12
        if self.width < 160:
            size = 10

        for i, d in enumerate(distances):
            t = graphicsUtils.text(self.toScreen(self.width / 2 + self.width / 8 * i, 0),
                    graphicsConstants.GHOST_COLORS[i + 1], d, graphicsConstants.TIMES_FONT, size,
                    graphicsConstants.TEXT_MOD_BOLD)
            self.ghostDistanceText.append(t)

    def setTeam(self, isBlue):
        if isBlue:
            text = graphicsConstants.TEAM_BLUE
        else:
            text = graphicsConstants.TEAM_RED
        self.teamText = graphicsUtils.text(self.toScreen(300, 0), self.textColor, text,
                graphicsConstants.TIMES_FONT, self.fontSize, graphicsConstants.TEXT_MOD_BOLD)

    def updateGhostDistances(self, distances):
        if len(distances) == 0:
            return

        if 'ghostDistanceText' not in dir(self):
            self.initializeGhostDistances(distances)
        else:
            for index, ghostDistance in enumerate(distances):
                graphicsUtils.changeText(self.ghostDistanceText[index], ghostDistance)

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

class AbstractPacmanGraphics(ABC):
    @abstractmethod
    def startGraphics(self, state):
        pass

    @abstractmethod
    def update(self, state):
        pass

    def __init__(self, zoom = graphicsConstants.DEFAULT_ZOOM,
            frameTime = graphicsConstants.DEFAULT_FRAME_TIME,
            capture = graphicsConstants.DEFAULT_CAPTURE_ARG,
            gif = graphicsConstants.DEFAULT_GIF_ARG,
            gifSkipFrames = graphicsConstants.DEFAULT_GIF_FRAME_SKIP,
            gifFPS = graphicsConstants.DEFAULT_GIF_FPS):
        self.have_window = 0  # Not used anywhere.
        self.currentGhostImages = {}  # Not used anywhere.
        self.pacmanImage = None  # Not used anywhere.
        self.zoom = zoom
        self.gridSize = graphicsConstants.DEFAULT_GRID_SIZE * zoom
        self.capture = capture
        self.frameTime = frameTime

        self.gifPath = gif
        self.gifSkipFrames = gifSkipFrames
        self.gifFPS = gifFPS
        self.frame = 0
        self.frameImages = []

    def initialize(self, state, isBlue = False):
        self.isBlue = isBlue
        self.startGraphics(state)

        # self.drawDistributions(state)
        self.distributionImages = None  # Initialized lazily
        self.drawStaticObjects(state)
        self.drawAgentObjects(state)

        # Information
        self.previousState = state

        # Get the first frame.
        self.save_frame(force_save = True)

    def save_frame(self, force_save = False):
        """
        Save the current frame as an image.
        If we are not going to save the game as a gif, no image will be saved.
        """

        if not self.gifPath:
            return

        if self.gifSkipFrames != 0 and self.frame % self.gifSkipFrames != 0:
            return

        self.frameImages.append(graphicsUtils.getPostscript())

    def write_gif(self):
        if not self.gifPath:
            return

        # Delay the dependency unless someone actually needs it.
        import imageio

        images = [imageio.imread(io.BytesIO(image.encode())) for image in self.frameImages]
        imageio.mimwrite(self.gifPath, images, fps = self.gifFPS, subrectangles = True)

    def drawDistributions(self, state):
        walls = state.getWalls()
        dist = []
        for x in range(walls.getWidth):
            distx = []
            dist.append(distx)
            for y in range(walls.getHeight):
                screen_x, screen_y = self.to_screen((x, y))
                block = graphicsUtils.square(screen_x, screen_y, 0.5 * self.gridSize,
                    color = graphicsConstants.BACKGROUND_COLOR, filled = 1, behind = 2)
                distx.append(block)
        self.distributionImages = dist

    def drawStaticObjects(self, state):
        layout = self.layout
        self.drawWalls(layout.walls)
        self.food = self.drawFood(layout.food)
        self.capsules = self.drawCapsules(layout.capsules)
        graphicsUtils.refresh()

    def drawAgentObjects(self, state):
        self.agentImages = []  # (agentState, image)
        for index, agent in enumerate(state.getAgentStates()):
            if agent.isPacman():
                image = self.drawPacman(agent, index)
                self.agentImages.append((agent, image))
            else:
                image = self.drawGhost(agent, index)
                self.agentImages.append((agent, image))
        graphicsUtils.refresh()

    def swapImages(self, agentIndex, newState):
        """
        Changes an image from a ghost to a pacman or vis versa (for capture)
        """
        prevState, prevImage = self.agentImages[agentIndex]
        for item in prevImage:
            graphicsUtils.remove_from_screen(item)

        if newState.isPacman():
            image = self.drawPacman(newState, agentIndex)
            self.agentImages[agentIndex] = (newState, image)
        else:
            image = self.drawGhost(newState, agentIndex)
            self.agentImages[agentIndex] = (newState, image)
        graphicsUtils.refresh()

    def make_window(self, width, height):
        grid_width = (width - 1) * self.gridSize
        grid_height = (height - 1) * self.gridSize
        screen_width = 2 * self.gridSize + grid_width
        screen_height = 2 * self.gridSize + grid_height + graphicsConstants.INFO_PANE_HEIGHT

        graphicsUtils.begin_graphics(screen_width, screen_height,
                graphicsConstants.BACKGROUND_COLOR, "Pacman")

    def drawPacman(self, pacman, index):
        position = self.getPosition(pacman)
        screen_point = self.to_screen(position)
        endpoints = self.getEndpoints(self.getDirection(pacman))

        width = graphicsConstants.PACMAN_OUTLINE_WIDTH
        outlineColor = graphicsConstants.PACMAN_COLOR
        fillColor = graphicsConstants.PACMAN_COLOR

        if self.capture:
            outlineColor = graphicsConstants.TEAM_COLORS[index % 2]
            fillColor = graphicsConstants.GHOST_COLORS[index]
            width = graphicsConstants.PACMAN_CAPTURE_OUTLINE_WIDTH

        return [graphicsUtils.circle(
                screen_point, graphicsConstants.PACMAN_SCALE * self.gridSize,
                fillColor = fillColor, outlineColor = outlineColor,
                endpoints = endpoints, width = width)]

    def getEndpoints(self, direction, position=(0, 0)):
        x, y = position
        pos = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi * pos)

        delta = width / 2
        if (direction == 'West'):
            endpoints = (180 + delta, 180 - delta)
        elif (direction == 'North'):
            endpoints = (90 + delta, 90 - delta)
        elif (direction == 'South'):
            endpoints = (270 + delta, 270 - delta)
        else:
            endpoints = (0 + delta, 0 - delta)

        return endpoints

    def movePacman(self, position, direction, image):
        screenPosition = self.to_screen(position)
        endpoints = self.getEndpoints(direction, position)
        r = graphicsConstants.PACMAN_SCALE * self.gridSize
        graphicsUtils.moveCircle(image[0], screenPosition, r, endpoints)
        graphicsUtils.refresh()

    def animatePacman(self, pacman, prevPacman, image):
        if self.frameTime < 0:
            print('Press any key to step forward, "q" to play')
            keys = graphicsUtils.wait_for_keys()
            if 'q' in keys:
                self.frameTime = 0.1

        if self.frameTime > 0.01 or self.frameTime < 0:
            fx, fy = self.getPosition(prevPacman)
            px, py = self.getPosition(pacman)
            frames = 4.0
            for i in range(1, int(frames) + 1):
                pos = (px * i / frames + fx * (frames - i) / frames,
                    py * i / frames + fy * (frames - i) / frames)
                self.movePacman(pos, self.getDirection(pacman), image)
                graphicsUtils.refresh()
                graphicsUtils.sleep(abs(self.frameTime) / frames)
        else:
            self.movePacman(self.getPosition(pacman), self.getDirection(pacman), image)

        graphicsUtils.refresh()

    def getGhostColor(self, ghost, ghostIndex):
        if ghost.isScared():
            return graphicsConstants.SCARED_COLOR
        else:
            return graphicsConstants.GHOST_COLORS[ghostIndex]

    def drawGhost(self, ghost, agentIndex):
        pos = self.getPosition(ghost)
        dir = self.getDirection(ghost)
        screen_x, screen_y = (self.to_screen(pos))
        ghostSize = self.gridSize * graphicsConstants.GHOST_SIZE
        coords = []
        for x, y in graphicsConstants.GHOST_SHAPE:
            coords.append((x * ghostSize + screen_x, y * ghostSize + screen_y))

        colour = self.getGhostColor(ghost, agentIndex)
        body = graphicsUtils.polygon(coords, colour, filled = 1)

        dx = 0
        dy = 0

        if dir == 'North':
            dy = -0.2

        if dir == 'South':
            dy = 0.2

        if dir == 'East':
            dx = 0.2

        if dir == 'West':
            dx = -0.2

        coords = (screen_x + ghostSize * (-0.3 + dx / 1.5),
                screen_y - ghostSize * (0.3 - dy / 1.5))
        leftEye = graphicsUtils.circle(coords, ghostSize * 0.2, graphicsConstants.WHITE,
                graphicsConstants.WHITE)

        coords = (screen_x + ghostSize * (0.3 + dx / 1.5),
                screen_y - ghostSize * (0.3 - dy / 1.5))
        rightEye = graphicsUtils.circle(coords, ghostSize * 0.2, graphicsConstants.WHITE,
                graphicsConstants.WHITE)

        coords = (screen_x + ghostSize * (-0.3 + dx),
                screen_y - ghostSize * (0.3 - dy))
        leftPupil = graphicsUtils.circle(coords, ghostSize * 0.08, graphicsConstants.BLACK,
                graphicsConstants.BLACK)

        coords = (screen_x + ghostSize * (0.3 + dx),
                screen_y - ghostSize * (0.3 - dy))
        rightPupil = graphicsUtils.circle(coords, ghostSize * 0.08, graphicsConstants.BLACK,
                graphicsConstants.BLACK)

        ghostImageParts = []
        ghostImageParts.append(body)
        ghostImageParts.append(leftEye)
        ghostImageParts.append(rightEye)
        ghostImageParts.append(leftPupil)
        ghostImageParts.append(rightPupil)

        return ghostImageParts

    def moveEyes(self, pos, dir, eyes):
        screen_x, screen_y = (self.to_screen(pos))
        dx = 0
        dy = 0

        if dir == 'North':
            dy = -0.2

        if dir == 'South':
            dy = 0.2

        if dir == 'East':
            dx = 0.2

        if dir == 'West':
            dx = -0.2

        ghostSize = self.gridSize * graphicsConstants.GHOST_SIZE

        coords = (screen_x + ghostSize * (-0.3 + dx / 1.5),
                screen_y - ghostSize * (0.3 - dy / 1.5))
        graphicsUtils.moveCircle(eyes[0], coords, ghostSize * 0.2)

        coords = (screen_x + ghostSize * (0.3 + dx / 1.5),
                screen_y - ghostSize * (0.3 - dy / 1.5))
        graphicsUtils.moveCircle(eyes[1], coords, ghostSize * 0.2)

        coords = (screen_x + ghostSize * (-0.3 + dx),
                screen_y - ghostSize * (0.3 - dy))
        graphicsUtils.moveCircle(eyes[2], coords, ghostSize * 0.08)

        coords = (screen_x + ghostSize * (0.3 + dx),
                screen_y - ghostSize * (0.3 - dy))
        graphicsUtils.moveCircle(eyes[3], coords, ghostSize * 0.08)

    def moveGhost(self, ghost, ghostIndex, prevGhost, ghostImageParts):
        old_x, old_y = self.to_screen(self.getPosition(prevGhost))
        new_x, new_y = self.to_screen(self.getPosition(ghost))
        delta = new_x - old_x, new_y - old_y

        for ghostImagePart in ghostImageParts:
            graphicsUtils.move_by(ghostImagePart, delta)
        graphicsUtils.refresh()

        if (ghost.isScared()):
            color = graphicsConstants.SCARED_COLOR
        else:
            color = graphicsConstants.GHOST_COLORS[ghostIndex]

        graphicsUtils.edit(ghostImageParts[0], ('fill', color), ('outline', color))
        self.moveEyes(self.getPosition(ghost), self.getDirection(ghost), ghostImageParts[-4:])
        graphicsUtils.refresh()

    def getPosition(self, agentState):
        return agentState.getPosition()

    def getDirection(self, agentState):
        return agentState.getDirection()

    def finish(self):
        # Get the last frame.
        self.save_frame(force_save = True)

        graphicsUtils.end_graphics()

        self.write_gif()

    def to_screen(self, point):
        x, y = point
        x = (x + 1) * self.gridSize
        y = (self.height - y) * self.gridSize

        return x, y

    # Fixes some TK issue with off - center circles
    def to_screen2(self, point):
        x, y = point
        x = (x + 1) * self.gridSize
        y = (self.height - y) * self.gridSize

        return (x, y)

    def drawWalls(self, wallMatrix):
        wallColor = graphicsConstants.WALL_COLOR
        for xNum, x in enumerate(wallMatrix):
            if self.capture and (xNum * 2) < wallMatrix.getWidth():
                wallColor = graphicsConstants.TEAM_COLORS[0]

            if self.capture and (xNum * 2) >= wallMatrix.getWidth():
                wallColor = graphicsConstants.TEAM_COLORS[1]

            for yNum, cell in enumerate(x):
                # Skip if there is no wall here.
                if not cell:
                    continue

                pos = xNum, yNum
                screen = self.to_screen(pos)
                screen2 = self.to_screen2(pos)

                # draw each quadrant of the square based on adjacent walls
                wIsWall = self.isWall(xNum - 1, yNum, wallMatrix)
                eIsWall = self.isWall(xNum + 1, yNum, wallMatrix)
                nIsWall = self.isWall(xNum, yNum + 1, wallMatrix)
                sIsWall = self.isWall(xNum, yNum - 1, wallMatrix)
                nwIsWall = self.isWall(xNum - 1, yNum + 1, wallMatrix)
                swIsWall = self.isWall(xNum - 1, yNum - 1, wallMatrix)
                neIsWall = self.isWall(xNum + 1, yNum + 1, wallMatrix)
                seIsWall = self.isWall(xNum + 1, yNum - 1, wallMatrix)

                wallSize = graphicsConstants.WALL_RADIUS * self.gridSize

                # NE quadrant
                if not nIsWall and not eIsWall:
                    # inner circle
                    graphicsUtils.circle(screen2, wallSize, wallColor, wallColor, (0, 91), 'arc')

                if nIsWall and not eIsWall:
                    # vertical line
                    graphicsUtils.line(self.add(screen, (wallSize, 0)),
                            self.add(screen, (wallSize, self.gridSize * (-0.5) - 1)), wallColor)

                if not nIsWall and eIsWall:
                    # horizontal line
                    graphicsUtils.line(self.add(screen, (0, -1 * wallSize)),
                            self.add(screen, (self.gridSize * 0.5 + 1, -1 * wallSize)), wallColor)

                if nIsWall and eIsWall and not neIsWall:
                    # outer circle
                    graphicsUtils.circle(self.add(screen2, (2 * wallSize, -1 * wallSize)),
                            wallSize - 1, wallColor, wallColor, (180, 271), 'arc')
                    graphicsUtils.line(self.add(screen, (2 * wallSize - 1, -1 * wallSize)),
                            self.add(screen, (self.gridSize * 0.5 + 1, -1 * wallSize)), wallColor)
                    graphicsUtils.line(self.add(screen, (wallSize, -2 * wallSize + 1)),
                            self.add(screen, (wallSize, self.gridSize * (-0.5))), wallColor)

                # NW quadrant
                if not nIsWall and not wIsWall:
                    # inner circle
                    graphicsUtils.circle(screen2, wallSize, wallColor, wallColor, (90, 181), 'arc')

                if nIsWall and not wIsWall:
                    # vertical line
                    graphicsUtils.line(self.add(screen, (-1 * wallSize, 0)),
                            self.add(screen, (-1 * wallSize, self.gridSize * (-0.5) - 1)),
                        wallColor)

                if not nIsWall and wIsWall:
                    # horizontal line
                    graphicsUtils.line(self.add(screen, (0, -1 * wallSize)),
                            self.add(screen, (self.gridSize * (-0.5) - 1, -1 * wallSize)),
                        wallColor)

                if nIsWall and wIsWall and not nwIsWall:
                    # outer circle
                    graphicsUtils.circle(self.add(screen2, (-2 * wallSize, -2 * wallSize)),
                            wallSize - 1, wallColor, wallColor, (270, 361), 'arc')
                    graphicsUtils.line(self.add(screen, (-2 * wallSize + 1, -1 * wallSize)),
                            self.add(screen, (self.gridSize * (-0.5), -1 * wallSize)), wallColor)
                    graphicsUtils.line(self.add(screen, (-1 * wallSize, -2 * wallSize + 1)),
                            self.add(screen, (-1 * wallSize, self.gridSize * (-0.5))), wallColor)

                # SE quadrant
                if not sIsWall and not eIsWall:
                    # inner circle
                    graphicsUtils.circle(screen2, wallSize, wallColor, wallColor,
                            (270, 361), 'arc')

                if sIsWall and not eIsWall:
                    # vertical line
                    graphicsUtils.line(self.add(screen, (wallSize, 0)),
                            self.add(screen, (wallSize, self.gridSize * (0.5) + 1)), wallColor)

                if not sIsWall and eIsWall:
                    # horizontal line
                    graphicsUtils.line(self.add(screen, (0, wallSize)),
                            self.add(screen, (self.gridSize * 0.5 + 1, wallSize)), wallColor)

                if sIsWall and eIsWall and not seIsWall:
                    # outer circle
                    graphicsUtils.circle(self.add(screen2, (2 * wallSize, 2 * wallSize)),
                            wallSize - 1, wallColor, wallColor, (90, 181), 'arc')
                    graphicsUtils.line(self.add(screen, (2 * wallSize - 1, wallSize)),
                            self.add(screen, (self.gridSize * 0.5, wallSize)), wallColor)
                    graphicsUtils.line(self.add(screen, (wallSize, 2 * wallSize - 1)),
                            self.add(screen, (wallSize, self.gridSize * (0.5))), wallColor)

                # SW quadrant
                if not sIsWall and not wIsWall:
                    # inner circle
                    graphicsUtils.circle(screen2, wallSize, wallColor, wallColor,
                            (180, 271), 'arc')

                if sIsWall and not wIsWall:
                    # vertical line
                    graphicsUtils.line(self.add(screen, (-1 * wallSize, 0)),
                            self.add(screen, (-1 * wallSize, self.gridSize * (0.5) + 1)), wallColor)

                if not sIsWall and wIsWall:
                    # horizontal line
                    graphicsUtils.line(self.add(screen, (0, wallSize)),
                            self.add(screen, (self.gridSize * (-0.5) - 1, wallSize)), wallColor)

                if sIsWall and wIsWall and not swIsWall:
                    # outer circle
                    graphicsUtils.circle(self.add(screen2, (-2 * wallSize, 2 * wallSize)),
                            wallSize - 1, wallColor, wallColor, (0, 91), 'arc')
                    graphicsUtils.line(self.add(screen, (-2 * wallSize + 1, wallSize)),
                            self.add(screen, (self.gridSize * (-0.5), wallSize)), wallColor)
                    graphicsUtils.line(self.add(screen, (-1 * wallSize, 2 * wallSize - 1)),
                            self.add(screen, (-1 * wallSize, self.gridSize * (0.5))), wallColor)

    def isWall(self, x, y, walls):
        if x < 0 or y < 0:
            return False

        if x >= walls.getWidth() or y >= walls.getHeight():
            return False

        return walls[x][y]

    def drawFood(self, foodMatrix):
        foodImages = []
        color = graphicsConstants.FOOD_COLOR
        for xNum, x in enumerate(foodMatrix):
            if self.capture and (xNum * 2) <= foodMatrix.getWidth():
                color = graphicsConstants.TEAM_COLORS[0]

            if self.capture and (xNum * 2) > foodMatrix.getWidth():
                color = graphicsConstants.TEAM_COLORS[1]

            imageRow = []
            foodImages.append(imageRow)
            for yNum, cell in enumerate(x):
                if cell:  # There's food here
                    screen = self.to_screen((xNum, yNum))
                    dot = graphicsUtils.circle(screen, graphicsConstants.FOOD_SIZE * self.gridSize,
                            outlineColor = color, fillColor = color, width = 1)
                    imageRow.append(dot)
                else:
                    imageRow.append(None)

        return foodImages

    def drawCapsules(self, capsules):
        capsuleImages = {}
        for capsule in capsules:
            screen_x, screen_y = self.to_screen(capsule)
            dot = graphicsUtils.circle((screen_x, screen_y),
                    graphicsConstants.CAPSULE_SIZE * self.gridSize,
                    outlineColor = graphicsConstants.CAPSULE_COLOR,
                    fillColor = graphicsConstants.CAPSULE_COLOR, width = 1)
            capsuleImages[capsule] = dot

        return capsuleImages

    def removeFood(self, cell, foodImages):
        x, y = cell
        graphicsUtils.remove_from_screen(foodImages[x][y])

    def removeCapsule(self, cell, capsuleImages):
        x, y = cell
        graphicsUtils.remove_from_screen(capsuleImages[(x, y)])

    def drawExpandedCells(self, cells):
        """
        Draws an overlay of expanded grid positions for search agents
        """

        n = float(len(cells))
        baseColor = [1.0, 0.0, 0.0]
        self.clearExpandedCells()
        self.expandedCells = []

        for k, cell in enumerate(cells):
            screenPos = self.to_screen(cell)
            cellColor = graphicsUtils.formatColor(*[(n - k) * c * .5 / n + .25 for c in baseColor])
            block = graphicsUtils.square(screenPos, 0.5 * self.gridSize, color = cellColor,
                    filled = 1, behind = 2)
            self.expandedCells.append(block)
            if self.frameTime < 0:
                graphicsUtils.refresh()

    def clearExpandedCells(self):
        if 'expandedCells' in dir(self) and len(self.expandedCells) > 0:
            for cell in self.expandedCells:
                graphicsUtils.remove_from_screen(cell)

    def updateDistributions(self, distributions):
        "Draws an agent's belief distributions"
        if (self.distributionImages is None):
            self.drawDistributions(self.previousState)

        for x in range(len(self.distributionImages)):
            for y in range(len(self.distributionImages[0])):
                image = self.distributionImages[x][y]
                weights = [dist[(x, y)] for dist in distributions]

                if (sum(weights) != 0):
                    pass

                # Fog of war
                color = [0.0, 0.0, 0.0]
                colors = graphicsConstants.GHOST_VEC_COLORS[1:]  # With Pacman
                if self.capture:
                    colors = graphicsConstants.GHOST_VEC_COLORS

                for weight, gcolor in zip(weights, colors):
                    color = [min(1.0, c + 0.95 * g * weight ** .3) for c, g in zip(color, gcolor)]
                graphicsUtils.changeColor(image, graphicsUtils.formatColor(*color))
        graphicsUtils.refresh()

    def add(self, x, y):
        return (x[0] + y[0], x[1] + y[1])
