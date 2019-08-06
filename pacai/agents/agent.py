import glob
import os

import pacai.util.util

# TODO(eriq): Rename to BaseAgent
class Agent(object):
    """
    An agent is something in the pacman world that does something (takes some action).
    Could be a ghost, the player controller Pac-Man, an AI controlling Pac-Man, etc.

    An agent must define the getAction method,
    but may also override any of the other methods.
    """

    def __init__(self, index = 0):
        self.index = index

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """

        pacai.util.util.raiseNotDefined()

    def registerInitialState(self, state):
        """
        Inspect the starting state.
        """

        pass

    def observationFunction(self, state):
        """
        Make an observation on the state of the game.
        """

        return state.deepCopy()

    def final(self, state):
        """
        Inform the agent about the result of a game.
        """

        pass

    def loadAgent(class_name, index, args = {}):
        """
        Create an agent of the given class with the given index and args.
        """

        Agent._import_agents(os.path.join(os.path.dirname(__file__), "*.py"), "pacai.agents.%s")
        Agent._import_agents(os.path.join(os.path.dirname(__file__), '..', 'student', "*.py"), "pacai.student.%s")

        # Now that the agent classes have been loaded, just look for subclasses.
        for subclass in pacai.util.util.getAllDescendents(Agent):
            if (subclass.__name__ == class_name):
                return subclass(index = index, **args)

        raise LookupError("Could not find an agent with the name: " + class_name)

    def _import_agents(glob_path, package_format_string):
        """
        Load all the agents from this package.
        Note that we are explicitly doing this now so that others are not
        required to pre-load all the possible agents.
        We don't need the module in scope, we just need the import to run.
        """

        for path in glob.glob(glob_path):
            if (not os.path.isfile):
                continue

            if (os.path.basename(path) in ['__init__.py', os.path.basename(__file__)]):
                continue

            # Ignore the rest of the path and extension.
            module_name = os.path.basename(path)[:-3]

            try:
                __import__(package_format_string % (module_name))
            except ImportError as ex:
                print("WARN: Unable to import agent: '%s'. -- %s" % (module_name, str(ex)))
