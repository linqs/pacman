from pacai.agents.base import BaseAgent
from pacai.core.game import Directions
from pacai.ui import graphicsUtils

class BaseKeyboardAgent(BaseAgent):
    """
    An agent controlled by the keyboard.
    """

    def __init__(self, index = 0, directional_keys = {}):
        """
        directional_keys is a dict of direction to keys for that direction.
        """

        super().__init__(index)

        self.lastMove = Directions.STOP
        self.directional_keys = directional_keys

    def translateKey(self, keys_pressed):
        """
        Convert key presses into Directions (e.g. Directions.WEST).
        """

        for direction in self.directional_keys:
            for key in self.directional_keys[direction]:
                if (key in keys_pressed):
                    return direction

        return None

    def getAction(self, state):
        intended_action = None
        legal = state.getLegalActions(self.index)

        keys = graphicsUtils.keys_waiting() + graphicsUtils.keys_pressed()
        if (keys != []):
            intended_action = self.translateKey(keys)
            if (intended_action not in legal):
                # The keyed action is illegal, ignore the key press.
                intended_action = None

        # If we have no intended action, try to do what we did last time.
        if (intended_action is None):
            intended_action = self.lastMove

        # If the final action is illegal, just stop.
        if (intended_action not in legal):
            intended_action = Directions.STOP

        self.lastMove = intended_action

        return intended_action

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

    def __init__(self, index = 0):
        super().__init__(index, WASDKeyboardAgent.KEYS)

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

    def __init__(self, index = 0):
        super().__init__(index, IJKLKeyboardAgent.KEYS)
