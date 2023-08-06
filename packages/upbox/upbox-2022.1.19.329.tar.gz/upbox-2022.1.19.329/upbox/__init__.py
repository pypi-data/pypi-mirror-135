# -*- coding: utf-8 -*-

'''
################################################################################
#                                                                              #
# upbox                                                                        #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is an uploading website and database system.                    #
#                                                                              #
# copyright (C) 2022 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help             display help message
    --version              display version and exit
    --database=FILENAME    database                                   [default: upbox.db]
    --home=TEXT            home URL                                   [default: home.html]
    --redirect_HTTPS=BOOL  direct loaded HTTP URLS to HTTPS versions  [default: true]
    --logfile=FILENAME     log filename                               [default: upbox.log]
'''

import base64
import datetime
import docopt
import logging
import math
import os
import string
import sys
from urllib.parse import urlparse as urlparse
import uuid

import dataset
from flask import (
  Flask,
  make_response,
  redirect,
  render_template,
  request
)
import technicolor

name        = 'upbox'
__version__ = '2022-01-19T0329Z'

log = logging.getLogger(name)
log.addHandler(technicolor.ColorisingStreamHandler())
log.setLevel(logging.DEBUG)

log.info(f'{name} {__version__}')

app = Flask(__name__)

def WSGI(argv=[]):
  global options
  options = docopt.docopt(__doc__, argv=argv)
  global filename_database
  global home_URL
  global redirect_HTTPS
  filename_database = options['--database']
  home_URL          = options['--home']
  filename_log      = options['--logfile']
  redirect_HTTPS    = options['--redirect_HTTPS'].lower() == 'true'
  ensure_database(filename=filename_database)
  return app

def main():
  global options
  options = docopt.docopt(__doc__)
  if options['--version']:
    print(__version__)
    exit()
  global filename_database
  global home_URL
  global redirect_HTTPS
  filename_database = options['--database']
  home_URL          = options['--home']
  filename_log      = options['--logfile']
  redirect_HTTPS    = options['--redirect_HTTPS'].lower() == 'true'
  ensure_database(filename=filename_database)
  app.run(
    host     = '0.0.0.0',
    #port     = 80,
    port     = 443,
    debug    = False,
    threaded = True
  )
  sys.exit()

def ensure_database(filename='upbox.db'):
  if not os.path.isfile(filename):
    log.info(f'database {filename} nonexistent; creating database')
    create_database(filename=filename)

def create_database(filename='upbox.db'):
  log.info(f'create database {filename}')
  os.system(f'sqlite3 {filename} "create table aTable(field1 int); drop table aTable;"')

def access_database(filename='upbox.db'):
  log.info('access database {filename}')
  database = dataset.connect('sqlite:///{filename}')
  return database

@app.route('/')
def index():
  log.info('route index')
  return redirect(home_URL)

@app.route('/robots.txt', methods=['GET'])
def robots():
  try:
    response = make_response('User-agent: *\nDisallow: /')
    response.headers['Content-type'] = 'text/plain'
    return response
  except:
    pass

@app.route('/upbox', methods=['GET', 'POST'])
def home():
  log.info('route home')
  try:
    if request.method == 'POST':
      text_input = str(request.form.get('text_input'))
      comment    = str(request.form.get('comment'))
      IP         = str(request.remote_addr)
      unique_ID  = str(uuid.uuid4())
      log.info(f'accept text input "{text_input}" with unique ID {unique_ID} for {IP}')
      database = access_database(filename=filename_database)
      table    = database['data']
      log.info('save entry to database')
      table.insert(
        dict(
          comment    = comment,
          IP         = IP,
          text_input = text_input,
          timestamp  = datetime.datetime.utcnow(),
          unique_ID  = unique_ID,
        )
      )
      return render_template(home_URL, message=f'saved input with unique ID {unique_ID}')
    return render_template('home.html')
  except:
    log.error('error')
    return render_template(home_URL, message='error')

if __name__ == '__main__':
  main()
