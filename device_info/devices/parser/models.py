# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-14 10:48:41
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-15 15:10:44
# @github: https://github.com/longfengpili

import json


class Phone:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, item: str):
        return self.kwargs.get(item)

    def __getattribute__(self, item: str):
        return super(Phone, self).__getattribute__(item)

    def __repr__(self):
        return f"{self.pname}({self.mname}::{self.purl})"

    @property
    def data(self):
        return self.kwargs

    @property
    def attrs(self):
        return set(self.kwargs.keys())

    @property
    def data_json(self):
        data = json.dumps(self.kwargs)
        return data

    @classmethod
    def load(cls, **kwargs):
        return cls(**kwargs)

    def get(self, item: str):
        try:
            return self[item]
        except:
            return self.kwargs.get(item)

    def update(self, phone):
        update_status = True
        pdata = phone.data
        pmname = self.mname
        _pmname = pdata.get('mname')
        if pmname and pmname != _pmname:
            update_status = False
            return update_status

        for k, v in pdata.items():
            pv = self.kwargs.get(k)
            if isinstance(pv, list):
                self.kwargs[k].append(v)
            elif pv and pv != v:
                self.kwargs[k] = [pv, v]
            elif not pv:
                self.kwargs[k] = v
            else:
                pass

        return update_status

    @staticmethod
    def concat(*phones: tuple):
        length = len(phones)
        if length == 1:
            return phones[0]

        all_keys = set.union(*[phone.attrs for phone in phones])
        common_keys = set.intersection(*[phone.attrs for phone in phones])
        common_value_keys = []
        concat_values = {}

        for key in common_keys:
            values = [phone.get(key) for phone in phones]
            values_set = set(values)
            if len(values_set) == 1:
                common_value_keys.append(key)
                concat_values[key] = values[0]
            else:
                v_count = {value: values.count(value) for value in values_set}
                v_count_sorted = sorted(v_count.items(), key=lambda x: x[1], reverse=True)
                value, value_count = v_count_sorted[0]
                if value_count >= 2:
                    concat_values[key] = f"{value}({length}->{value_count})"

        special_keys = all_keys - set(common_value_keys)
        special = [{attr: phone.get(attr) for attr in phone.attrs if attr in special_keys} for phone in phones]
        concat_values['special'] = special
        return Phone(**concat_values)
