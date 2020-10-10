## Copyright (c) 2020 mangalbhaskar.
"""web utility functions."""
__author__ = 'mangalbhaskar'


import os
import sys
import uuid


def add_path(path):
  if path not in sys.path:
    sys.path.insert(0, path)


def add_pythonpath(pythonpath):
  """Add to PYTHONPATH."""
  for k in pythonpath.keys():
    add_path(pythonpath[k])


def allowed_file(filename, allowed_type):
  fn, ext = os.path.splitext(os.path.basename(filename))
  return ext.lower() in allowed_type


def create_uuid(prefix='uid'):
  """Create uuid4 specific UUID which uses pseudo random generators."""
  return prefix+'-'+str(uuid.uuid4())
