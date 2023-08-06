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

  __last_line_len = 0

  @staticmethod
  def __print(msg):
    filler_len = max(0, Docker.__last_line_len-len(msg))
    Docker.__last_line_len = len(msg)

    if len(msg):
      if msg[-1] == '\n':
        sys.stdout.write("\r\033[K" + msg[:-1] + ' '*filler_len + '\n')
      else:
        sys.stdout.write("\r\033[K" + msg + ' '*filler_len)
    else:
      sys.stdout.write("\r\033[K" + ' '*filler_len)
    sys.stdout.flush()    

  @staticmethod
  def __progress_bar(ublob, done, total):
    line_len = 0
    nb_traits = int(50*done/total)
    sys.stdout.write('\r' + ublob + ': Downloading [')
    line_len += len(ublob) + 15
    for i in range(0, nb_traits):
      line_len += 1
      if i == nb_traits - 1:
        sys.stdout.write('>')
      else:
        sys.stdout.write('=')
    for i in range(0, 49 - nb_traits):
      line_len += 1
      sys.stdout.write(' ')

    tail = '] {}/{}'.format(done, total)
    line_len += len(tail)
    sys.stdout.write(tail)
    filler_len = max(0, Docker.__last_line_len-line_len)
    if filler_len:
      sys.stdout.write(' '*filler_len)
    sys.stdout.flush()
    Docker.__last_line_len = line_len

  @staticmethod
  def __get_auth_head(repository):
    Docker.__print('{}: Authenticating...'.format(repository))

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
    tag = repository + ':sha256(' + layer['digest'][7:19] + ')'

    Docker.__print('{}: Downloading...'.format(tag))

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

    total_size = int(response.getheader('Content-Length'))
    block_size = max(int(total_size/1000), 1024**2)
    downloaded_size = 0

    fileobj = tempfile.NamedTemporaryFile(dir='.')

    Docker.__progress_bar(tag, 0, total_size)
    while downloaded_size < total_size:
      block = response.read(min(block_size, total_size-downloaded_size))
      if not block:
        break
      fileobj.write(block)
      downloaded_size += len(block)
      Docker.__progress_bar(tag, downloaded_size, total_size)

    Docker.__print('{}: Downloaded Layer...'.format(tag))

    del response

    file = source.strip(os.path.sep)
    Docker.__print('{}: Scanning Layer for {}...'.format(tag, file))

    tarf = tarfile.open(fileobj.name, mode='r:gz')

    for member in tarf.getmembers():
      if member.name != file:
        continue
      Docker.__print('{}: Extracting {}...'.format(tag, file))
      tgt = os.path.realpath(os.path.join(target, os.path.basename(file)))
      
      with tarf.extractfile(member) as fs:
        with open(tgt, 'wb') as fd:
          shutil.copyfileobj(fs, fd)

      Docker.__print('Downloaded {}\n'.format(tgt))
      return True

    Docker.__print('')
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

