## Copyright (c) 2020 mangalbhaskar.
"""Main stub."""
__author__ = 'mangalbhaskar'

import os
import sys

this = sys.modules[__name__]
this_dir = os.path.dirname(__file__)

clear = lambda: os.system('clear')
clear()


def echo():
  print("__name__: {}".format(__name__))
  pass

def main():
  """
  stub for now.
  """
  echo()


if __name__ == "__main__":
  main()
