import abc
import glob
import logging
import os

from pacai.util import reflection

class BaseAgent(abc.ABC):
    """
    An agent is something in the pacman world that does something (takes some action).
    Could be a ghost, the player controlled pacman, an AI controlled pacman, etc.

    An agent must define the `BaseAgent.getAction` method,
    but may also override any of the other methods.

    Note that methods that take in a state should assume that they own a shallow copy of the state.
    So the state should not be modified and a deep copy should be made of any information
    they want to keep.

    Non-abstract children should make sure that their constructors accept `**kwargs`,
    since agents are typically created reflexively.
    """

    def __init__(self, index = 0, **kwargs):
        self.index = index
        self.kwargs = kwargs

    @abc.abstractmethod
    def getAction(self, state):
        """
        The BaseAgent will receive an `pacai.core.gamestate.AbstractGameState`,
        and must return an action from `pacai.core.directions.Directions`.
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
        Called once for each round of the game.
        """

        pass

    def final(self, state):
        """
        Inform the agent about the result of a game.
        """

        pass

    @staticmethod
    def loadAgent(name, index, args = {}):
        """
        Load an agent with the given class name.
        The name can be fully qualified or just the bare class name.
        If the bare name is given, the class should appear in the
        `pacai.agents` or `pacai.student` package.
        """

        if (name.startswith('pacai.')):
            # This name looks like a fully qualified name, load it directly.
            agentClass = reflection.qualifiedImport(name)
            return agentClass(index = index, **args)
        else:
            # This is probably just a class name.
            return BaseAgent._loadAgentByName(name, index, args)

    @staticmethod
    def _loadAgentByName(className, index, args = {}):
        """
        Create an agent of the given class with the given index and args.
        This will search the `pacai.agents` package as well as the `pacai.student` package
        for an agent with the given class name.
        """

        thisDir = os.path.dirname(__file__)

        BaseAgent._importAgents(os.path.join(thisDir, '*.py'), 'pacai.agents.%s')
        BaseAgent._importAgents(os.path.join(thisDir, '..', 'student', '*.py'),
                'pacai.student.%s')

        # Also check any subpackages of pacai.agents.
        for path in glob.glob(os.path.join(thisDir, '*')):
            if (os.path.isfile(path)):
                continue

            if (os.path.basename(path).startswith('__')):
                continue

            packageName = os.path.basename(path)
            packageFormatString = 'pacai.agents.%s.%%s' % (packageName)

            BaseAgent._importAgents(os.path.join(path, '*.py'), packageFormatString)

        # Now that the agent classes have been loaded, just look for subclasses.
        for subclass in reflection.getAllDescendents(BaseAgent):
            if (subclass.__name__ == className):
                return subclass(index = index, **args)

        raise LookupError('Could not find an agent with the name: ' + className)

    @staticmethod
    def _importAgents(globPath, packageFormatString):
        """
        Load all the agents from this package.
        Note that we are explicitly doing this now so that others are not
        required to pre-load all the possible agents.
        We don't need the module in scope, we just need the import to run.
        """

        for path in glob.glob(globPath):
            if (not os.path.isfile(path)):
                continue

            if (os.path.basename(path) in ['__init__.py', os.path.basename(__file__)]):
                continue

            # Ignore the rest of the path and extension.
            moduleName = os.path.basename(path)[:-3]

            try:
                __import__(packageFormatString % (moduleName))
            except ImportError as ex:
                logging.warning('Unable to import agent: "%s". -- %s' % (moduleName, str(ex)))
