from pacai.agents.base import BaseAgent
from pacai.core.directions import Directions

class BaseKeyboardAgent(BaseAgent):
    """
    An general agent controlled by the keyboard.
    """

    def __init__(self, index = 0, keyboard = None, directionalKeys = {}, **kwargs):
        """
        directionalKeys is a dict of direction to keys for that direction.
        """

        super().__init__(index)

        self._keyboard = keyboard
        self._lastMove = Directions.STOP
        self._directionalKeys = directionalKeys

        # The keys that we are explictly looking for,
        self._queryKeys = set()
        for keys in self._directionalKeys.values():
            for key in keys:
                self._queryKeys.add(key)

    def getAction(self, state):
        # Note that we delay this check (instead of doing it in the constructor)
        # so that replays can create any agent and not worry about a GUI.
        if (self._keyboard is None):
            raise ValueError("Keyboard agents require a pacai.ui.keyboard.Keyboard.")

        intended_action = None
        legal = state.getLegalActions(self.index)

        keys = self._keyboard.query(self._queryKeys)
        if (keys != []):
            intended_action = self._translateKey(keys)
            if (intended_action not in legal):
                # The keyed action is illegal, ignore the key press.
                intended_action = None

        # If we have no intended action, try to do what we did last time.
        if (intended_action is None):
            intended_action = self._lastMove

        # If the final action is illegal, just stop.
        if (intended_action not in legal):
            intended_action = Directions.STOP

        self._lastMove = intended_action

        return intended_action

    def _translateKey(self, keysPressed):
        """
        Convert key presses into Directions (e.g. Directions.WEST).
        """

        for key in reversed(keysPressed):
            for (direction, possibleKeys) in self._directionalKeys.items():
                if (key in possibleKeys):
                    return direction

        return None

class WASDKeyboardAgent(BaseKeyboardAgent):
    """
    An agent controlled by WASD or the arrow keys.
    """

    KEYS = {
        Directions.NORTH: ['w', 'Up'],
        Directions.WEST: ['a', 'Left'],
        Directions.SOUTH: ['s', 'Down'],
        Directions.EAST: ['d', 'Right'],
    }

    def __init__(self, index = 0, keyboard = None):
        super().__init__(index, keyboard, WASDKeyboardAgent.KEYS)

class IJKLKeyboardAgent(BaseKeyboardAgent):
    """
    An agent controlled by IJKL.
    """

    KEYS = {
        Directions.NORTH: ['i'],
        Directions.WEST: ['j'],
        Directions.SOUTH: ['k'],
        Directions.EAST: ['l'],
    }

    def __init__(self, index = 0, keyboard = None):
        super().__init__(index, keyboard, IJKLKeyboardAgent.KEYS)
