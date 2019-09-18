import abc
import glob
import logging
import os

from pacai.util import reflection

class BaseAgent(abc.ABC):
    """
    An agent is something in the pacman world that does something (takes some action).
    Could be a ghost, the player controller Pac-Man, an AI controlling Pac-Man, etc.

    An agent must define the getAction method,
    but may also override any of the other methods.

    Note that methods that take in a state should assume that they own a shallow copy of the state.
    So the state should not be modified and a deep copy should be made of any information
    they want to keep.
    """

    def __init__(self, index = 0):
        self.index = index

    @abc.abstractmethod
    def getAction(self, state):
        """
        The BaseAgent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """

        pass

    def registerInitialState(self, state):
        """
        Inspect the starting state.
        """

        pass

    def observationFunction(self, state):
        """
        Make an observation on the state of the game.
        """

        pass

    def final(self, state):
        """
        Inform the agent about the result of a game.
        """

        pass

    def loadAgent(class_name, index, args = {}):
        """
        Create an agent of the given class with the given index and args.
        """

        this_dir = os.path.dirname(__file__)

        BaseAgent._import_agents(os.path.join(this_dir, '*.py'), 'pacai.agents.%s')
        BaseAgent._import_agents(os.path.join(this_dir, '..', 'student', '*.py'),
                'pacai.student.%s')

        # Also check any subpackages of pacai.agents.
        for path in glob.glob(os.path.join(this_dir, '*')):
            if (os.path.isfile(path)):
                continue

            if (os.path.basename(path).startswith('__')):
                continue

            package_name = os.path.basename(path)
            package_format_string = 'pacai.agents.%s.%%s' % (package_name)

            BaseAgent._import_agents(os.path.join(path, '*.py'), package_format_string)

        # Now that the agent classes have been loaded, just look for subclasses.
        for subclass in reflection.getAllDescendents(BaseAgent):
            if (subclass.__name__ == class_name):
                return subclass(index = index, **args)

        raise LookupError('Could not find an agent with the name: ' + class_name)

    def _import_agents(glob_path, package_format_string):
        """
        Load all the agents from this package.
        Note that we are explicitly doing this now so that others are not
        required to pre-load all the possible agents.
        We don't need the module in scope, we just need the import to run.
        """

        for path in glob.glob(glob_path):
            if (not os.path.isfile(path)):
                continue

            if (os.path.basename(path) in ['__init__.py', os.path.basename(__file__)]):
                continue

            # Ignore the rest of the path and extension.
            module_name = os.path.basename(path)[:-3]

            try:
                __import__(package_format_string % (module_name))
            except ImportError as ex:
                logging.warning('Unable to import agent: "%s". -- %s' % (module_name, str(ex)))
