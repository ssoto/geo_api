#!python
# -*- coding: utf-8 -*-

import logging
import os


class ConfigObj(object):
    """
    Config object class
    """

class Config(ConfigObj):

    APP_LOG_PATH = os.path.join('.', 'logs' )
    APP_LOG_FILE = 'geo_api.log'
    APP_LOG_LEVEL = logging.DEBUG

    DB_HOST = None
    DB_PORT = None
    DB_USER = None
    DB_PASSWORD = None
    DB_NAME = None

