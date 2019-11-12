'''
@Author: longfengpili
@Date: 2019-07-12 10:51:48
@LastEditTime: 2019-10-16 16:05:48
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import json
import re

import logging
from logging import config

config.fileConfig('parselog.conf')
repairbi_logger = logging.getLogger('repairbi')

class RepairJsonData(object):
    '''
    修复json数据
    '''
    def __init__(self, myjson, error_max=5, error=None):
        self.myjson_origin = myjson
        self.myjson = myjson
        self.error_num = 0
        self.error_max = error_max
        self.error = error
        self.errors = None

    def loads_json(self):
        try:
            self.myjson = json.loads(self.myjson)
            self.error = None
        except Exception as e:
            self.error = f'>>>>>>>>{e}'
            # repairbi_logger.error(f'{self.error}')
            # repairbi_logger.error(f'{self.myjson}')
            self.errors.append(self.error)
            self.error_num += 1

    def repair_for_bomerror(self):
        self.myjson = self.myjson.encode('utf-8')[3:].decode('utf-8')
        self.loads_json()

    def repair_for_innerjson(self):
        self.myjson = self.myjson.replace('":"{"', '":{"').replace('}","', '},"') #去掉json内部json结构双引号
        self.myjson = self.myjson.replace('}"}', '}}') # 去掉结尾的双引号
        self.myjson = re.sub('(?<!\:)""', '"', self.myjson) # 去掉多个双引号(前边非冒号)
        self.myjson = self.myjson.replace('"[', '[').replace(']"', ']') #数组后的双引号
        self.myjson = self.myjson.replace('}{', '},{') #数组后的双引号
        self.loads_json()

    def repair_for_preerror(self):
        self.myjson = self.myjson.strip()
        result = re.search('\{', self.myjson)
        if result:
            prenumber = result.span()[0]
            self.myjson = self.myjson[prenumber:]
        self.loads_json()

    def repair_main(self):
        if not self.errors:
            self.errors = []
        self.loads_json()
        
        while self.error:
            if 'UTF-8 BOM' in self.error:
                self.repair_for_bomerror()
            elif "Expecting ',' delimiter" in self.error:
                self.repair_for_innerjson()
            elif "line 1 column 1 (char 0)" in self.error:
                self.repair_for_preerror()
            else:
                self.errors.append(self.error)
                self.error_num += 1
            
            if self.error_num >= self.error_max:
                error_json = {}
                # msg_type = re.search('"msg_type":"(.*?)"', str(self.myjson_origin))
                # msg_type = msg_type.group(1) if msg_type else 'error'
                msg_type = 'error'
                    
                msg_type = f'{msg_type}'
                self.errors.insert(0, f'【{msg_type}】\n{self.myjson_origin}')

                error_json['msg_type'] = msg_type
                error_json['error_status'] = 'error'
                error_json['error_content'] = self.myjson_origin
                self.error = None
                self.myjson = error_json
        self.myjson = json.dumps(self.myjson)
        return self.myjson

