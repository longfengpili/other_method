# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 18:03:23
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-18 19:07:19
# @github: https://github.com/longfengpili

import pytest

from lxml import etree

from devices.device import Kimovil


class TestKimovil:

    def setup_method(self, method):
        self.pname = '2206122SC'
        self.km = Kimovil()

    def teardown_method(self, method):
        pass

    @pytest.mark.skip()
    def test_request(self):
        res = self.km.request(self.pname)
        print(res)

    def test_get_pkinds(self):
        url, pkinds = self.km.get_pkinds(self.pname)
        print(url)
        print(pkinds)

    def test_parse_pkind(self):
        url, pkinds = self.km.get_pkinds(self.pname)
        pkind = pkinds[0]
        pkind = self.km.parse_pkind(pkind)
        print(pkind)

    def test_get_phone_by_pkind(self):
        url, pkinds = self.km.get_pkinds(self.pname)
        pkind = pkinds[0]
        pkind = self.km.parse_pkind(pkind)
        print(pkind)
        phone = self.km.get_phone_by_pkind(pkind)
        print(phone)

    def test_parse_phone(self):
        url, pkinds = self.km.get_pkinds(self.pname)
        pkind = pkinds[0]
        pkind = self.km.parse_pkind(pkind)
        print(pkind)
        phone = self.km.get_phone_by_pkind(pkind)
        phone_info = self.km.parse_phone(phone)
        print(phone_info)

    def test_get_phones(self):
        # phones = ['vivo 1906', 'CPH2083', '2206122SC']
        phones = ['samsung SM-A025F', '2206122SC']
        for idx, pname in enumerate(phones):
            phone_info = self.km.get_phone(idx, pname)
            print(phone_info)

    def test_get_phones_with_tpool(self):
        phones = ['vivo 1906', 'CPH2083', 'Infinix X670', 'V2026', 'M2101K6G', 'CPH1937', 'SM-A125F', '220333QAG', 
                  '2201117TG', 'Infinix X688B', 'RMX3195', 'RMX2040', 'RMX3511', 'RMX3263']
        phones = self.km.get_phones_with_tpool(phones)
        print(phones)
