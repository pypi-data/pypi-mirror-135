#! /usr/bin/env python3
#
# Copyright (c) 2022, Gabriel Linder <linder.gabriel@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

import logging
import os
import sys
import warnings
from contextlib import contextmanager, suppress

logging.DUMP = logging.INFO + 1


def showwarning(_message, _category, _filename, _lineno,
                _file=None, _line=None):
    pass


def formatwarning(message, category, filename, lineno, _line=None):
    return f'{filename}:{lineno}: {category.__name__}: {message}'


if os.name == 'posix' and sys.stderr.isatty():

    def format_color(_level, color_code):
        return f'\033[1;{color_code}m'

    FORMAT_STRING = '%(levelname)s%(asctime)s\033[0m' \
                    ' \033[90m|\033[0m' \
                    ' %(message)s'

else:

    def format_color(level, _color_code):
        return logging.getLevelName(level)

    FORMAT_STRING = '%(asctime)s | %(levelname)s\t| %(message)s'


verbosity = logging.DEBUG if 'DEBUG' in os.environ else logging.WARNING

logging.basicConfig(level=verbosity,
                    format=FORMAT_STRING,
                    datefmt='%Y-%m-%d %H:%M:%S')

for level, color in ((logging.DEBUG, 36),
                     (logging.DUMP, 34),
                     (logging.INFO, 32),
                     (logging.WARNING, 33),
                     (logging.ERROR, 31),
                     (logging.CRITICAL, 35)):
    logging.addLevelName(level, format_color(level, color))


if os.environ.get('DEBUG', '') == 'ALL':
    # print the first occurrence of matching warnings,
    # for each location where the warning is issued.
    warnings.simplefilter('default')
    # catch common pandas errors, if installed
    with suppress(ImportError):
        from pandas.core.common import SettingWithCopyWarning
        warnings.simplefilter('error', SettingWithCopyWarning)
    # we also want to catch future and deprecation warnings
    warnings.simplefilter('error', FutureWarning)
    warnings.simplefilter('error', DeprecationWarning)


warnings.showwarning = showwarning
warnings.formatwarning = formatwarning
logging.captureWarnings(True)


@contextmanager
def ignore_warnings():
    try:
        logging.captureWarnings(False)
        yield
    finally:
        logging.captureWarnings(True)


assert not hasattr(logging, 'ignore_warnings')
logging.ignore_warnings = ignore_warnings


def dump(*args, **kwargs):

    for v in args:
        logging.log(logging.DUMP, f'{v}')

    for k, v in kwargs.items():
        logging.log(logging.DUMP, f'{k}: {v}')


assert not hasattr(logging, 'dump')
logging.dump = dump

logging.warn = logging.warning
logging.err = logging.error
logging.crit = logging.critical


def current_loggers():
    for logger in logging.Logger.manager.loggerDict:
        print(logger)


for module in [
        'matplotlib',
        'parso',
        'urllib3',
]:
    logging.getLogger(module).setLevel(logging.WARNING)


if __name__ == '__main__':
    logging.debug('This is a debug message')
    logging.dump('This is a dump message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')
