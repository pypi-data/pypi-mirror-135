#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tarfile
import tempfile
import functools
import os
import shutil
import sys
import json
import io
from distutils.version import StrictVersion
from .shell import Shell
from .platform import Platform
from .http import Request


class Docker(object):

  @staticmethod
  def __progress_bar(ublob, nb_traits):
    sys.stdout.write('\r' + ublob + ': Downloading [')
    for i in range(0, nb_traits):
      if i == nb_traits - 1:
        sys.stdout.write('>')
      else:
        sys.stdout.write('=')
    for i in range(0, 49 - nb_traits):
      sys.stdout.write(' ')
    sys.stdout.write(']')
    sys.stdout.flush()

  @staticmethod
  def __get_auth_head(repository):
    sys.stdout.write("\r{}: Authenticating...{}".format(repository, " "*52))
    sys.stdout.flush()

    uri = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:{}:pull'.format(repository)
    
    request = Request(method='GET', url=uri)
    response = request.do()
    
    assert response.status == 200, 'unable to authorize docker pull for {} with {} {}'.format(repository, response.status, response.read().decode('utf-8'))
    
    data = json.loads(response.read().decode('utf-8'))

    sys.stdout.write("\r\033[K")
    sys.stdout.flush()
    return {
      'Authorization': 'Bearer {}'.format(data['token']),
      'Accept': 'application/vnd.docker.distribution.manifest.v2+json'
    }

  @staticmethod
  def get_metadata(repository, tag):
    uri = 'https://index.docker.io/v2/{}/manifests/{}'.format(repository, tag)
    
    auth_headers = Docker.__get_auth_head(repository)
    request = Request(method='GET', url=uri)
    for key, value in auth_headers.items():
      request.add_header(key, value)
    response = request.do()
    
    assert response.status == 200, 'unable to obtain metadata of {}:{} with {} {}'.format(repository, tag, response.status, response.read().decode('utf-8'))
    
    data = json.loads(response.read().decode('utf-8'))
    return {
      'layers': data['layers'],
      'digest': data['config']['digest']
    }

  @staticmethod
  def extract_file(repository, layer, source, target):
    short_digest = layer['digest'][7:19]

    sys.stdout.write('{}: Downloading...'.format(short_digest))
    sys.stdout.flush()

    if len(layer.get('urls', [])):
      uri = layer['urls'][0]
    else:
      uri = 'https://index.docker.io/v2/{}/blobs/{}'.format(repository, layer['digest'])
    
    auth_headers = Docker.__get_auth_head(repository)
    request = Request(method='GET', url=uri)
    for key, value in auth_headers.items():
      request.add_header(key, value)
    response = request.do()

    assert response.status == 200, 'unable to download layer {}:{} with {} {}'.format(repository, layer['digest'], response.status, response.read().decode('utf-8'))

    unit = int(response.getheader('Content-Length')) / 50
    acc = 0
    nb_traits = 0

    fileobj = tempfile.TemporaryFile()

    Docker.__progress_bar(short_digest, nb_traits)
    while 1:
      buf = response.read(8 * 1024)
      if not buf:
        break
      fileobj.write(buf)
      acc = acc + 8192
      if acc > unit:
        nb_traits = nb_traits + 1
        Docker.__progress_bar(short_digest, nb_traits)
        acc = 0

    fileobj.seek(0)

    sys.stdout.write("\r\033[K{}: Scanning...".format(short_digest))
    sys.stdout.flush()

    tarf = tarfile.open(fileobj=fileobj, mode='r:gz')
    file = source.strip(os.path.sep)

    for member in tarf.getmembers():
      if member.name != file:
        continue
      sys.stdout.write("\r\033[K{}: Extracting...".format(short_digest))
      sys.stdout.flush()
      tmp_dir = tempfile.TemporaryDirectory()
      tarf.extract(member, path=tmp_dir.name)
      tgt = os.path.realpath(os.path.join(target, os.path.basename(file)))
      shutil.move(os.path.join(tmp_dir.name, file), tgt)
      tmp_dir.cleanup()
      sys.stdout.write("\r\033[KDownloaded {}\n".format(tgt))
      sys.stdout.flush()
      return True

    sys.stdout.write("\r\033[K")
    sys.stdout.flush()
    return False


class Package(object):

  def __init__(self, name):
    self.__name = name

  @property
  def latest_version(self):
    uri = "https://hub.docker.com/v2/repositories/openbank/{}/tags?page=1".format(self.__name)

    request = Request(method='GET', url=uri)
    request.add_header('Accept', 'application/json')
    response = request.do()

    if not response.status == 200:
      return None

    body = json.loads(response.read().decode('utf-8')).get('results', [])
    tags = []

    for entry in body:
      version = entry['name']
      if not version.startswith('{}-'.format(Platform.arch)):
        continue
      if not version.endswith('.main'):
        continue
      tags.append({
        'semver': StrictVersion(version[len(Platform.arch)+1:-5]),
        'version': version[len(Platform.arch)+1:-5],
        'tag': entry['name'],
        'ts': entry['tag_last_pushed']
      })

    compare = lambda x, y: x['ts'] > y['ts'] if x['semver'] == y['semver'] else x['semver'] > y['semver']

    latest = max(tags, key=functools.cmp_to_key(compare))

    if not latest:
      return None

    return latest['version']

  def download(self, version, meta, output):
    os.makedirs(output, exist_ok=True)

    file = '{}_{}_{}.deb'.format(self.__name, version, Platform.arch)
    package = '{}/{}'.format(output, file)

    if os.path.exists(package):
      return True

    repository = 'openbank/{}'.format(self.__name)
    tag = '{}-{}.{}'.format(Platform.arch, version, meta)
    metadata = Docker.get_metadata(repository, tag)

    if len(metadata['layers']):
      metadata['layers'].pop()

    for layer in metadata['layers']:
      if Docker.extract_file(repository, layer, '/opt/artifacts/{}'.format(file), output):
        return os.path.exists(package)

    return False

