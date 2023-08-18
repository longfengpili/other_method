# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 18:03:23
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-18 16:26:52
# @github: https://github.com/longfengpili


import json
import pytest

from devices.device import Geekbench


class TestGeekbench:

    def setup_method(self, method):
        self.pname = '2206122SC'
        self.gb = Geekbench()

    def teardown_method(self, method):
        pass

    @pytest.mark.skip()
    def test_request(self):
        res = self.gb.request(self.pname)
        print(res)

    def test_get_pkinds(self):
        url, pkinds = self.gb.get_pkinds(self.pname)
        print(url)
        print(pkinds)

    def test_parse_pkind(self):
        url, pkinds = self.gb.get_pkinds(self.pname)
        pkind = pkinds[0]
        pkind = self.gb.parse_pkind(pkind)
        print(pkind)

    def test_get_phone_by_pkind(self):
        url, pkinds = self.gb.get_pkinds(self.pname)
        pkind = pkinds[0]
        print(pkind)
        pkind = self.gb.parse_pkind(pkind)
        phone = self.gb.get_phone_by_pkind(pkind)
        print(phone)

    def test_parse_phone(self):
        url, pkinds = self.gb.get_pkinds(self.pname)
        pkind = pkinds[0]
        pkind = self.gb.parse_pkind(pkind)
        print(pkind)
        phone = self.gb.get_phone_by_pkind(pkind)
        phone_info = self.gb.parse_phone(phone)
        print(phone_info)

    def test_get_phones(self):
        phones = ['samsung SM-A025F', '2206122SC']
        for idx, pname in enumerate(phones):
            phone_info = self.gb.get_phone(idx, pname)
            print(phone_info)

    def test_get_phones_with_tpool(self):
        phones = ['vivo 1906', 'CPH2083', 'Infinix X670', 'V2026', 'M2101K6G', 'CPH1937', 'SM-A125F', '220333QAG', 
                  '2201117TG', 'Infinix X688B', 'RMX3195', 'RMX2040', 'RMX3511', 'RMX3263']
        phones = self.gb.get_phones_with_tpool(phones, max_workers=3)
        print(phones)
