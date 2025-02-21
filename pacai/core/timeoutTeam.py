from pacai.util import reflection

def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.agents.capture.timeout.TimeoutAgent',
        second = 'pacai.agents.capture.timeout.TimeoutAgent'):
    """
    A team for testing timeouts.
    """

    firstAgent = reflection.qualifiedImport(first)
    secondAgent = reflection.qualifiedImport(second)

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]
