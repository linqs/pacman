from pacai.ui import token
from pacai.ui.capture.view import CaptureAbstractView
from pacai.ui.text import AbstractTextView

class CaptureTextView(CaptureAbstractView, AbstractTextView):
    """
    A text view for capture.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _convertToken(self, objectToken):
        if (token.isPacman(objectToken)):
            if (int((objectToken - token.PACMAN_START) / 100) % 2 == 0):
                return 'P'
            else:
                return 'p'
        elif (token.isGhost(objectToken)):
            if (int((objectToken - token.GHOST_START) / 100) % 2 == 0):
                return 'g'
            else:
                return 'G'
        else:
            return super()._convertToken(objectToken)
