from pacai.ui import token
from pacai.ui.view import AbstractView

class AbstractTextView(AbstractView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Override
    def _drawFrame(self, state, frame, forceDraw = False):
        # Only draw after agents moves.
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

        print('Score: %d' % (state.getScore()))

    def _convertToken(self, objectToken):
        if (objectToken == token.EMPTY_TOKEN):
            return ' '
        if (token.isWall(objectToken)):
            return '█'
        if (token.isFood(objectToken)):
            return '⋅'
        elif (token.isCapsule(objectToken)):
            return 'c'
        elif (token.isPacman(objectToken)):
            return 'P'
        elif (token.isGhost(objectToken)):
            return 'G'
        elif (objectToken == token.SCARED_GHOST_TOKEN):
            return 'S'
        else:
            return "%02d" % (objectToken)
