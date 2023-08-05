"""
    GitDataLab Development Server
"""

import logging
import sys

from livereload import Server


class CustomServer(Server):

    def _setup_logging(self):
        super()._setup_logging()

        # gets rid of Browser Connected messages
        logging.getLogger('livereload').setLevel(logging.WARNING)

        # set log level of built-in web server
        logging.getLogger('tornado.access').setLevel(logging.INFO)
        # logging.getLogger('tornado.application').setLevel(logging.INFO)


class ColoredConsoleHandler(logging.StreamHandler):
    """
        custom console log handler with coloured entries
    """

    def emit(self, record):
        levelno = record.levelno
        if levelno >= 50:  # CRITICAL / FATAL
            color = '\x1b[31m'  # red
        elif levelno >= 40:  # ERROR
            color = '\x1b[31m'  # red
        elif levelno >= 30:  # WARNING
            color = '\x1b[33m'  # yellow
        elif levelno >= 20:  # INFO
            color = '\x1b[32m'  # green
        elif levelno >= 10:  # DEBUG
            color = '\x1b[35m'  # pink
        else:  # NOTSET and anything else
            color = '\x1b[0m'  # normal
        record.color = color
        record.nocolor = '\x1b[0m'
        record.location = '%s:%s' % (record.module, record.lineno)
        logging.StreamHandler.emit(self, record)


class LiveReloadFilter(logging.Filter):
    """filters out livereload messages"""

    def filter(self, record):
        # print('livereload', record.module, record.getMessage())
        if 'livereload' in record.getMessage():
            return 0
        return 1


class AppFilter(logging.Filter):
    """filters out livereload messages"""

    def filter(self, record):
        if record.module in ('wsgi', 'autoreload'):
            # suppress these messages because they are already handled by
            # the tornado console handler.
            return 0
        return 1


def setup_logging(level=logging.INFO):
    """Set up custom logging"""
    DEFAULT_FORMAT = (
        '%(color)s[%(levelname)1.1s %(asctime)s '
        '%(location)s]%(nocolor)s %(message)s'
    )
    DATE_FORMAT = '%y%m%d %H:%M:%S'

    con_formatter = logging.Formatter(DEFAULT_FORMAT, datefmt=DATE_FORMAT)
    console_handler = ColoredConsoleHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(con_formatter)
    console_handler.addFilter(AppFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)

    # filter livereload log entries
    tornado_logger = logging.getLogger('tornado.access')
    tornado_logger.addFilter(LiveReloadFilter())


def serve(app, port=5700, level=logging.INFO):
    server = CustomServer(app.wsgi_app)
    server.watch('.')
    setup_logging(level)
    server.serve(port=port)
