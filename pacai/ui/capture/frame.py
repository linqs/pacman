from pacai.ui import token
from pacai.ui.frame import Frame

class CaptureFrame(Frame):
    # Override
    def _getAgentBaseToken(self, x, y, agentIndex, state):
        if (state.getAgentState(agentIndex).isPacman()):
            return token.PACMAN_2 + agentIndex * 100
        else:
            return token.GHOST_1 + agentIndex * 100

    # Override
    def _getCapsuleBaseToken(self, x, y, state):
        if (x < self._width / 2):
            return token.RED_FOOD_BASE
        else:
            return token.BLUE_FOOD_BASE

    # Override
    def _getFoodBaseToken(self, x, y, state):
        if (x < self._width / 2):
            return token.RED_FOOD_BASE
        else:
            return token.BLUE_FOOD_BASE

    # Override
    def _getWallBaseToken(self, x, y, state):
        if (x < self._width / 2):
            return token.RED_WALL_BASE
        else:
            return token.BLUE_WALL_BASE
