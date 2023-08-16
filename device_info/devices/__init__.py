# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 11:57:57
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-16 11:28:28
# @github: https://github.com/longfengpili

import logging
import logging.config
from pydbapi.conf import LOGGING_CONFIG
LOGGING_CONFIG['loggers']['']['level'] = 'DEBUG'
logging.config.dictConfig(LOGGING_CONFIG)
# 屏蔽requests log
logging.getLogger('urllib3').setLevel(logging.WARNING)
