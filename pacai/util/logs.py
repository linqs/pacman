import logging

def initLogging(logging_level = logging.INFO):
    """
    Initializes the logging format and level.
    """

    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging_level)

def updateLoggingLevel(logging_level):
    """
    Updates the logging level.
    """

    logger = logging.getLogger()
    logger.setLevel(logging_level)
