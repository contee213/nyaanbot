# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
setup.py
~~~~~~~~~~~~~~
"""

from setuptools import setup

version = '0.0.1'

setup(name='nyaan',
      version=version,
      description='Twitter Nyaan Bot',
      author='contee213',
      author_email='contee213@gmail.com',
      url='http://github.com/contee213',
      packages=['nyaan'],
      entry_points="""
      [console_scripts]
      nyaanbotd = nyaan.nyaanbot:boot_daemon
      """
     )