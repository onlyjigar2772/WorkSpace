#!/usr/bin/python


import logging
import logging.handlers
import thirdpartylib


f = logging.Formatter(fmt='%(levelname)s:%(name)s: %(message)s '
    '(%(asctime)s; %(filename)s:%(lineno)d)',
    datefmt="%Y-%m-%d %H:%M:%S")

handlers = [
    logging.handlers.RotatingFileHandler('rorarted.log', encoding='utf8',
         maxBytes=1000000, backupCount=1),
    logging.StreamHandler()
]

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

for h in handlers:
    h.setFormatter(f)
    h.setLevel(logging.DEBUG)
    root_logger.addHandler(h)


logging.info('started')
thirdpartylib.do_something()
logging.info('finished')

