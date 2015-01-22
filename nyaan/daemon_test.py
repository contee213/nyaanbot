# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
daemon_test
~~~~~~~~~~~~~~

file commment here.

"""

import logging
import daemon

logger = logging.getLogger(__name__)

def main():
    logger.info("test")

if __name__ == '__main__':
    with daemon.DaemonContext():
        main()