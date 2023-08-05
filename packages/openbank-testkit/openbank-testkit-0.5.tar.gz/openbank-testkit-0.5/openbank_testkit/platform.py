#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform


class Platform(object):

  def __init__(self):
    self.__cached_arch = None

  @property
  def arch(self):
    if not self.__cached_arch:
      self.__cached_arch = {
        'x86_64': 'amd64',
        'armv8': 'arm64',
        'aarch64': 'arm64'
      }.get(platform.uname().machine, 'amd64')
    return self.__cached_arch
