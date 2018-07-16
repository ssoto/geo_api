#!python
# -*- coding: utf-8 -*-
import os

import logging
from logging import handlers

from geo_api import settings


def instanciate_logger() -> logging.Logger:
    """ Create new logger using app settings

    :return: logger
    """
    logger = logging.getLogger('geo_api')
    logger.setLevel(settings.APP_LOG_LEVEL)

    if not logger.hasHandlers():
        bytes_ = 1
        kbytes = 1000 * bytes_
        mbytes = 1000 * kbytes
        _format = ('[%(asctime)s] {%(pathname)s:%(lineno)d}'
                   '%(levelname)s - %(message)s')
        formatter = logging.Formatter(_format)
        # Try to create log folder
        os.makedirs(settings.APP_LOG_PATH, exist_ok=True)
        filename = os.path.join(settings.APP_LOG_PATH, settings.APP_LOG_FILE)

        rotatesizehandler = handlers.RotatingFileHandler(
            filename,
            maxBytes=150 * mbytes,
            backupCount=3,
        )
        rotatesizehandler.setLevel(settings.APP_LOG_LEVEL)
        rotatesizehandler.setFormatter(formatter)
        logger.addHandler(rotatesizehandler)
    return logger
