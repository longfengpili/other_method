# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 18:03:23
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-11 18:21:38
# @github: https://github.com/longfengpili

from devices.device import Geekbench


class TestGeekbench:

    def setup_method(self, method):
        self.pname = '2206122SC'
        self.gb = Geekbench()

    def teardown_method(self, method):
        pass

    def test_request(self):
        res = self.gb.request(self.pname)
        print(res)

    def test_get_pkinds(self):
        pkinds = self.gb.get_pkinds(1, self.pname)
        print(pkinds)