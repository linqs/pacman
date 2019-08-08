"""
Evaluation functions take a game state and create a score based on that state.
"""

def score(gameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """

    return gameState.getScore()
