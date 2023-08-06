import logging
import sys
from typing import Any

from colorama import init
from colorama import Fore, Back


LoggerLevel = Any
Logger = Any

init(autoreset=True)

def fmt_filter(record):
    record.levelname = '[%s]' % record.levelname
    record.name = '[%s]' % record.name
    return True

class CustomFormatter(logging.Formatter):

    FORMATS = {
        logging.DEBUG: [Fore.LIGHTBLACK_EX, Fore.RESET],
        logging.INFO: [Fore.GREEN, Fore.RESET],
        logging.WARNING: [Fore.YELLOW, Fore.RESET],
        logging.ERROR: [Fore.MAGENTA, Fore.RESET],
        logging.CRITICAL: [Back.RED, Back.RESET]
    }

    def format(self, record):
        log_color = self.FORMATS.get(record.levelno)
        log_fmt = f"{Fore.CYAN}[%(asctime)s]{Fore.RESET} {log_color[0]}%(levelname)-10s{log_color[1]} {Fore.LIGHTCYAN_EX}%(name)-15s{Fore.RESET} %(message)s"
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

def get_logger(name:str, level:LoggerLevel=logging.INFO) -> Logger:
    """Get the customized logger with time [level] [name] message format,
    where the time, level and name are colored.

    Args:
        name (str): The name of the logger, use __name__ as default
        level (LoggerLevel, optional): The logging level. Defaults to logging.INFO.

    Returns:
        Logger: The customized logger.
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    logger.setLevel(level)
    formatter = CustomFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addFilter(fmt_filter)
    return logger