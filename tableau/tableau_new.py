# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2022-01-05 07:02:14
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2022-01-05 08:16:57


import json
import requests

from mysetting import DOMAIN, APP_ID, HEADERS, COURSESAPI, COURSEAPI
from chrome_cookie import GetCooikiesFromChrome


class Tableau:

    def __init__(self, app_id, domain, headers, coursesapi):
        self.app_id = app_id
        self.domain = domain
        self.headers = headers
        self.coursesapi = coursesapi

    def create_headers(self):
        get_cookies = GetCooikiesFromChrome()
        cookie = get_cookies.get(self.domain)
        if not cookie:
            raise ValueError("please login")

        self.headers['Cookie'] = cookie
        # dslogger.info(headers)
        return self.headers

    def get_courseslist(self):
        data = '{"page_size":20,"goods_id":"term_61c55f79648f9_RYHNiw","last_id":"","goods_type":25,"resource_type":[6],"has_buy":null}'
        headers = self.create_headers()
        res = requests.post(self.coursesapi, headers=headers, data=data)
        res_json = res.json()
        with open('./goods.json', 'w', encoding='utf-8') as f:
            json.dump(res_json, f)
        courseslist = res_json.get('data').get('goods_list')
        return courseslist

    def get_courseinfo(self, course):
        data = {}
        data['page_size'] = 20
        data['goods_id'] = course.get('term_id')
        data['goods_type'] = 25
        data['resource_type'] = [1, 2, 3, 4, 20]
        data['node_id'] = course.get('node_id')
        data['type'] = 1
        data['order_type'] = 0
        print(data)
        headers = self.create_headers()
        print(headers)
        res = requests.post(self.coursesapi, headers=headers, data=data)
        res_json = res.json()
        return res_json





if __name__ == '__main__':
    tableau = Tableau(APP_ID, DOMAIN, HEADERS, COURSESAPI)
    courseslist = tableau.get_courseslist()
    course = courseslist[0]
    res_json = tableau.get_courseinfo(course)
    print(res_json)
    

    
