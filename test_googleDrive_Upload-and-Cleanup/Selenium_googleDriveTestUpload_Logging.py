"""
SUMMARY: Configures logging for the overall test

NOTES: See README.txt file for requirements to run and all sources used

VERSION INFO:
    Created by R. Reyna
    Date: 9/9/2024
    Version: 1.0.0
"""
import logging

LOGFORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s' # "%(message)s"  # Your format
DATEFMT = '%m-%d %H:%M'
DEFAULT_LEVEL = "info"  # Your default level, usually set to warning or error for production
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL}


def start_logging(filename: str, level=DEFAULT_LEVEL):
    """ Configures logging for this project.

    :param filename: Name of the log file
    :type filename: str
    :param level: Logging level
    :type level: str
    """

    logging.basicConfig(filename=filename, level=LEVELS[level], format=LOGFORMAT, datefmt=DATEFMT, filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
