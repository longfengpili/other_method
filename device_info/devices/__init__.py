# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 11:57:57
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-11 12:02:20
# @github: https://github.com/longfengpili

import logging
import logging.config
from pydbapi.conf import LOGGING_CONFIG
# LOGGING_CONFIG['handlers']['console']['formatter'] = 'color'
logging.config.dictConfig(LOGGING_CONFIG)
