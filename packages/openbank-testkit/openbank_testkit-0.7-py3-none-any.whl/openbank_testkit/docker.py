#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker


class Docker(object):

  def __init__(self):
    self.__cached_docker = None

  @property
  def images(self):
    if not self.__cached_docker:
      self.__cached_docker = docker.from_env()
    return self.__cached_docker.images

  @property
  def containers(self):
    if not self.__cached_docker:
      self.__cached_docker = docker.from_env()
    return self.__cached_docker.containers
