""" Logger class to log the messages to the console """
from dataclasses import dataclass
import logging
import colorlog


@dataclass()
class Logger:
    '''
        Logger class to log the messages to the console
    '''

    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        handler = logging.StreamHandler()

        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s [%(name)s] %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S:%f",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
        )
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def info(self, message: object):
        '''
            Logs the message with level INFO
        '''
        self.logger.info(message)

    def error(self, message: object):
        '''
            Logs the message with level ERROR
        '''
        self.logger.error(message)

    def exception(self, message: object):
        '''
            Logs the message with level EXCEPTION
        '''
        self.logger.exception(message)
