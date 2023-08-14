# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-14 10:48:41
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-14 16:50:45
# @github: https://github.com/longfengpili

import json


class Phone:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, item: str):
        if item in self.kwargs:
            return self.kwargs.get(item)
        return f"non_{item}"

    def __getattribute__(self, item):
        return super(Phone, self).__getattribute__(item)

    def __repr__(self):
        return f"{self.idx}({self.mname}::{self.purl})"

    @property
    def data(self):
        return self.kwargs

    @property
    def data_json(self):
        data = json.dumps(self.kwargs)
        return data

    @classmethod
    def load(cls, **kwargs):
        return cls(**kwargs)
