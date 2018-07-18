#!python
# -*- coding: utf-8 -*-

from .base import Config as BaseConfig

class Config(BaseConfig):

    DB_HOST = '127.0.0.1'
    DB_PORT = '5433'
    DB_USER = 'postgres'
    DB_PASSWORD = 'example'
    DB_NAME = 'Urbo'
