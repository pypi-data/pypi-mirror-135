from collections import defaultdict
from logging import DEBUG
from typing import Dict

from logzero import LogFormatter, formatter as set_formatter
from logzero import logger as log  # pylint: disable=W0611
from typeguard import typechecked


DEFAULT_FMT = '%(color)s[%(levelname)1.1s %(asctime)s PID:%(process)d(%(processName)s)<%(threadName)s>]%(end_color)s %(message)s'
DEBUG_FMT = '%(color)s[%(levelname)1.1s %(asctime)s PID:%(process)d(%(processName)s)<%(threadName)s>%(module)s:%(funcName)s:%(lineno)d]%(end_color)s %(message)s'


class DefaultLogFormatter(LogFormatter):
    @typechecked
    def __init__(self, formatters: Dict[int, str],
                 default_format: str = DEFAULT_FMT,
                 date_format: str = '%Y-%m-%d %H:%M:%S%z'):
        self.formats = defaultdict(lambda: default_format)
        for key, value in formatters.items():
            self.formats[key] = value
        LogFormatter.__init__(self, fmt=default_format, datefmt=date_format)

    def format(self, record):
        self._fmt = self.formats[record.levelno]
        return LogFormatter.format(self, record)


set_formatter(DefaultLogFormatter({DEBUG: DEBUG_FMT}, default_format=DEFAULT_FMT))
log.debug('Debug logging configured')
