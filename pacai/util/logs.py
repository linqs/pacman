import logging

def initLogging(logging_level = logging.INFO):
    """
    Initializes the format and level of the log messages in the program.
    """

    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging_level)

def updateLoggingLevel(logging_level):
    """
    Update the level of the log messages in the program.
    """

    logger = logging.getLogger()
    logger.setLevel(logging_level)
