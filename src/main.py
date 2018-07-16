#! /usr/bin/python
# -*- encode: UTF-8 -*-

from flask import Flask

from os import environ

settings_module = environ.get('GEO_API_SETTINGS_MODULE')
print(settings_module)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'