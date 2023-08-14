# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 18:03:23
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-14 14:36:12
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
        pkinds = self.km.get_pkinds(self.pname)
        print(pkinds)

    def test_parse_pkind(self):
        pkinds = self.km.get_pkinds(self.pname)
        pkind = pkinds[0]
        pkind = self.km.parse_pkind(pkind)
        print(pkind)

    def test_get_phone(self):
        pkinds = self.km.get_pkinds(self.pname)
        pkind = pkinds[0]
        pkind = self.km.parse_pkind(pkind)
        print(pkind)
        phone = self.km.get_phone(pkind)
        print(phone)

    def test_parse_phone(self):
        pkinds = self.km.get_pkinds(self.pname)
        pkind = pkinds[0]
        pkind = self.km.parse_pkind(pkind)
        print(pkind)
        phone = self.km.get_phone(pkind)
        phone_info = self.km.parse_phone(phone)
        print(phone_info)

    def test_get_phones(self):
        phones = ['CPH2083', '2206122SC']
        self.km.get_phones(phones)
