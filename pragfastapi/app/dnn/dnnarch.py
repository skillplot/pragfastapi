## Copyright (c) 2020 mangalbhaskar.
"""APP configuration"""
__author__ = 'mangalbhaskar'

import enum

class DnnArch(str, enum.Enum):
  maskrcnn = 'maskrcnn'
  lanenet = 'lanenet'
  cascadeld = 'cascadeld'
  yolo = 'yolo'
  resnet = 'resnet'
  hrnet = 'hrnet'
  vgg16 = 'vgg16'
