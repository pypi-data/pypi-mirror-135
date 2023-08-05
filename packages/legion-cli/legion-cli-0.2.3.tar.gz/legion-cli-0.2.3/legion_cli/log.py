from collections import defaultdict
from logging import DEBUG
from pathlib import Path
from typing import Dict

from logzero import logger as log, LogFormatter, formatter as set_formatter, logfile
from typeguard import typechecked


DEFAULT_FMT = '%(color)s[%(levelname)1.1s %(asctime)s]%(end_color)s %(message)s'
DEBUG_FMT = '%(color)s[%(levelname)1.1s %(asctime)s PID:%(process)d(%(processName)s)<%(threadName)s>%(module)s:%(funcName)s:%(lineno)d]%(end_color)s %(message)s'


@typechecked
def log_to_file(path: Path, max_megabytes: float = 1,
                backup_count: int = 3) -> None:
    if not path.is_file():
        path.parent.mkdir(parents=True)
        path.touch()
    logfile(str(path), maxBytes=max_megabytes * 1e6,
            backupCount=backup_count, disableStderrLogger=True)


@typechecked
class DefaultLogFormatter(LogFormatter):
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
