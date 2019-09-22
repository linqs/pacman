from pacai.ui.view import AbstractView
from pacai.ui.view import Frame

class PacmanTextView(AbstractView):
    def __init__(self):
        super().__init__()

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        # Only draw after pacman moves.
        if (not forceDraw and state.getLastAgentMoved() != 0):
            return

        print()

        row = frame.getWidth() * [None]

        # Start in the upper left (0, height - 1) amd go row-by-row.
        for y in range(frame.getHeight() - 1, -1, -1):
            for x in range(0, frame.getWidth(), 1):
                row[x] = self._convertToken(frame.getToken(x, y))

            print(''.join(row))

    def _convertToken(self, token):
        if (token == Frame.EMPTY):
            return ' '
        if (token == Frame.WALL):
            return '█'
        if (token == Frame.FOOD):
            return '⋅'
        elif (token == Frame.CAPSULE):
            return 'c'
        elif (token >= Frame.PACMAN_1 and token <= Frame.PACMAN_6):
            return 'P'
        elif (token >= Frame.GHOST_1 and token <= Frame.GHOST_6):
            return 'G'
        elif (token == Frame.SCARED_GHOST):
            return 'S'
        else:
            return "%02d" % (token)
