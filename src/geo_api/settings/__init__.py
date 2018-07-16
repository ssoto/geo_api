# -* coding: utf-8 *-
"""
Config import handler
This let us import settings, and don't care about:
>>> settings = importlib.import_module('module_name')
"""
import os
import importlib

config_module_name = os.getenv('GEO_API_SETTINGS_MODULE')
config_module = importlib.import_module(config_module_name)
config_class = config_module.__dict__['Config']

if not config_class:
    raise Exception('Configuration class not found')

config_attributes = dir(config_class)

to_import = [name for name in config_attributes if not name.startswith('_')]
globals().update({name: getattr(config_class, name) for name in to_import})
