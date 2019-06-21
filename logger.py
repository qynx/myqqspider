import logging
import sys

date_fmt = '%Y-%m-%d %H:%M:%S'

fmt = "%(asctime)s %(levelno)s: %(filename)s-%(funcName)s-%(lineno)d %(thread)d message=%(message)s"

formatter = logging.Formatter(fmt, date_fmt)

logger = logging.getLogger("main")

logger.setLevel(logging.DEBUG)

def stream_handler():
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    return sh

def file_handler():
    fh = logging.FileHandler("log.log")
    fh.setFormatter(formatter)
    return fh

logger.addHandler(stream_handler())
logger.addHandler(file_handler())