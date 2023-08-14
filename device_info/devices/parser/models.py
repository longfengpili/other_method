# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-14 10:48:41
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-14 11:19:59
# @github: https://github.com/longfengpili

import json


class Phone:

    def __init__(self, pname: str, mname: str, purl: str, **kwargs):
        self.pname = pname
        self.mname = mname
        self.purl = purl
        self.kwargs = kwargs

    def __getattr__(self, item: str):
        if item in self.kwargs:
            return self.kwargs.get(item)
        return f"{item} not exists"

    def __getattribute__(self, item):
        return super(Phone, self).__getattribute__(item)

    def __repr__(self):
        return f"{self.pname}({self.mname}::{self.purl})"

    @classmethod
    def load(cls, phone: dict):
        pname = phone.get('pname')
        mname = phone.get('mname')
        purl = phone.get('purl')
        kwargs = {k: v for k, v in phone.items() if k not in ('pname', 'mname', 'purl')}
        return cls(pname, mname, purl, **kwargs)

    def dump(self):
        phone = {}
        phone['pname'] = self.pname
        phone['mname'] = self.mname
        phone['purl'] = self.purl
        phone.update(self.kwargs)
        phone = json.dumps(phone)
        return phone
