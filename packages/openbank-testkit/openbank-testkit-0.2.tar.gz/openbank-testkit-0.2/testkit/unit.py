#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker
import platform
import tarfile
import tempfile
import errno
import os
import sys
from . import execute


class UnitHelper(object):

  def __get_arch(self):
    return {
      'x86_64': 'amd64',
      'armv8': 'arm64',
      'aarch64': 'arm64'
    }.get(platform.uname().machine, 'amd64')

  def __init__(self, name, version, meta):
    self.__arch = self.__get_arch()
    self.__name = name
    self.__version = version
    self.__docker = docker.from_env()

  def verify(self, file):
    cwd = os.path.realpath('{}/../..'.format(os.path.dirname(__file__)))
    (code, result, error) = execute(['dpkg', '-c', file])
    if code != 'OK':
      raise RuntimeError('code: {}, stdout: [{}], stderr: [{}]'.format(code, result, error))

  def download(self):
    failure = None

    cwd = os.path.realpath('{}/../..'.format(os.path.dirname(__file__)))

    package = '{}/packaging/bin/{}_{}_{}.deb'.format(cwd, self.__name, self.__version, self.__arch)

    if os.path.exists(package):
      self.verify(package)
      return

    os.makedirs(os.path.dirname(package), exist_ok=True)

    image_s = 'docker.io/openbank/{}:{}-{}.{}'.format(self.__name, self.__arch, self.__version, self.__meta)
    package_s = '/opt/artifacts/{}_{}_{}.deb'.format(self.__name, self.__version, self.__arch)

    scratch_docker_cmd = ['FROM alpine']

    scratch_docker_cmd.append('COPY --from={} {} {}'.format(image_s, package_s, package))

    tag = 'bbtest_{}-artifacts-scratch'.format(self.__name)
    temp = tempfile.NamedTemporaryFile(delete=True)
    try:
      with open(temp.name, 'w') as fd:
        fd.write(str(os.linesep).join(scratch_docker_cmd))
      image, stream = self.__docker.images.build(fileobj=temp, rm=True, pull=True, tag=tag)
      for chunk in stream:
        if not 'stream' in chunk:
          continue
        for line in chunk['stream'].splitlines():
          l = line.strip(os.linesep)
          if not len(l):
            continue
          sys.stderr.write(l+'\n')

      scratch = self.__docker.containers.run(tag, ['/bin/true'], detach=True)

      tar_name = tempfile.NamedTemporaryFile(delete=True)
      with open(tar_name.name, 'wb') as fd:
        bits, stat = scratch.get_archive(package)
        for chunk in bits:
          fd.write(chunk)

      archive = tarfile.TarFile(tar_name.name)
      archive.extract(os.path.basename(package), os.path.dirname(package))
      self.verify(package)
      scratch.remove()
    except Exception as ex:
      failure = ex
    finally:
      temp.close()
      try:
        self.__docker.images.remove(tag, force=True)
      except:
        pass

    if failure:
      raise failure
