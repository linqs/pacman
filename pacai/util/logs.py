import logging

def initLogging():
    """
    initializes the format and level of the log messages in the program
    """

    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
