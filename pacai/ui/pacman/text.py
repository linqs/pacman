from pacai.ui.view import AbstractView
from pacai.ui.view import Frame

class PacmanTextView(AbstractView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        # Only draw after pacman moves.
        if (not forceDraw and state.getLastAgentMoved() != 0):
            return

        print()

        agentTokens = frame.getDiscreteAgents()

        row = frame.getWidth() * [None]

        # Start in the upper left (0, height - 1) amd go row-by-row.
        for y in range(frame.getHeight() - 1, -1, -1):
            for x in range(0, frame.getWidth(), 1):
                # Overlay the agent's onto the board at the closest interger position.
                if ((x, y) in agentTokens):
                    row[x] = self._convertToken(agentTokens[(x, y)])
                else:
                    row[x] = self._convertToken(frame.getToken(x, y))

            print(''.join(row))

    def _convertToken(self, token):
        if (token == Frame.EMPTY):
            return ' '
        if (Frame.isWall(token)):
            return '█'
        if (token == Frame.FOOD):
            return '⋅'
        elif (token == Frame.CAPSULE):
            return 'c'
        elif (Frame.isPacman(token)):
            return 'P'
        elif (Frame.isGhost(token)):
            return 'G'
        elif (token == Frame.SCARED_GHOST):
            return 'S'
        else:
            return "%02d" % (token)
