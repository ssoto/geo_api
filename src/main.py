#! /usr/bin/python
# -*- encode: UTF-8 -*-

from flask import Flask

from geo_api.utils.common import instanciate_logger

LOGGER = instanciate_logger()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

LOGGER.debug('App is up now')
