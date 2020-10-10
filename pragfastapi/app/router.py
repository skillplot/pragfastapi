## Copyright (c) 2020 mangalbhaskar.
"""api path router."""
__author__ = 'mangalbhaskar'

import datetime
import os
import sys

from importlib import import_module

import fastapi

this_dir = os.path.dirname(__file__)


def get_mods(basedir):
  """get the python module names with path dynamically from the input basedir"""
  modnames = []
  modpaths = []
  if basedir:
    for f in os.listdir(os.path.join(this_dir, basedir)):
      if os.path.isfile(os.path.join(this_dir, basedir, f)) and f != '__init__.py':
        modnames.append(os.path.splitext(f)[0])
    modpaths = [os.path.basename(this_dir)+'.'+basedir+'.'+m for m in modnames]
  return modpaths, modnames


def get_route_registry(routepaths):
  """Get the route registry function dynamically from the route name list.
  rname should be: `routes.<name>`."""
  for rname in routepaths:
    rmod = import_module(rname)
    rfn = getattr(rmod, 'construct_route')
    yield rfn, rname


def add_app_routes(appcfg):
  """add api routes."""
  api_router = fastapi.APIRouter()
  routepaths, routenames  = get_mods('routes')
  print("routepaths: {}".format(routepaths))
  print("routenames: {}".format(routenames))

  ## Todo: raise exception
  if routepaths is None or len(routepaths) < 1:
    sys.exit()

  for rfn, rname in get_route_registry(routepaths):
    if rfn and rname:
      entity_prefix = os.path.join(appcfg.API_BASE_URL, rname.split('.')[-1])

      api_router.include_router(
        rfn(appcfg)
        ,prefix=entity_prefix
        ,tags=[entity_prefix]
      )
  return api_router

