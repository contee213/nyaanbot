# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
setup.py
~~~~~~~~~~~~~~
"""

from setuptools import setup, find_packages

version = '0.0.1'

setup(name=version,
      version='1.0',
      description='Twitter Nyaan Bot',
      author='contee213',
      author_email='contee213@gmail.com',
      url='http://github.com/contee213',
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      nyaanbotd = nyaan.nyaanbot:daemon
      """
     )