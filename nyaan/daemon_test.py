# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
daemon_test
~~~~~~~~~~~~~~

file commment here.

"""

import daemon
import logging
import time
from nyaan.log import setup_logging

def main():
    logger = logging.getLogger(__name__)
    while True:
        try:
            logger.debug("debug")
            logger.info("info")
            logger.error("error")
        except KeyboardInterrupt:
            break
        time.sleep(5)

if __name__ == '__main__':
    setup_logging()
    with daemon.DaemonContext():
        main()