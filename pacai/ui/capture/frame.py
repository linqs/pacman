from pacai.ui import token
from pacai.ui.frame import Frame

TIE_TEXT_COLOR = (180, 60, 180)
RED_TEXT_COLOR = (229, 0, 0)
BLUE_TEXT_COLOR = (0, 76, 229)

class CaptureFrame(Frame):
    """
    A frame specific to capture.
    Capture frames understand how to properly color each side of the board.
    """

    # Override
    def _getAgentBaseToken(self, x, y, agentIndex, state):
        if (state.getAgentState(agentIndex).isPacman()):
            return token.PACMAN_2 + agentIndex * 100
        else:
            return token.GHOST_1 + agentIndex * 100

    # Override
    def _getCapsuleBaseToken(self, x, y, state):
        if (x < self._boardWidth / 2):
            return token.RED_FOOD_BASE
        else:
            return token.BLUE_FOOD_BASE

    # Override
    def _getFoodBaseToken(self, x, y, state):
        if (x < self._boardWidth / 2):
            return token.RED_FOOD_BASE
        else:
            return token.BLUE_FOOD_BASE

    # Override
    def _getTextColor(self):
        if (self._score > 0):
            return RED_TEXT_COLOR
        elif (self._score < 0):
            return BLUE_TEXT_COLOR
        else:
            return TIE_TEXT_COLOR

    # Override
    def _getWallBaseToken(self, x, y, state):
        if (x < self._boardWidth / 2):
            return token.RED_WALL_BASE
        else:
            return token.BLUE_WALL_BASE
