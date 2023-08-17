# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-14 10:48:41
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-17 17:11:22
# @github: https://github.com/longfengpili


import time
import json


class Phone:
    dumpfile = f"phone{time.time()}.csv"

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, item: str):
        return self.kwargs.get(item)

    def __getattribute__(self, item: str):
        return super(Phone, self).__getattribute__(item)

    def __repr__(self):
        pname = f"[{self.idx:0>4d}]{self.pname}"
        
        mname, pkidx, purl = self.mname, self.pkidx, self.purl
        mname = mname if pkidx is None else f"{mname}::{pkidx}"
        mname = f"{mname}::{purl}" if purl else mname
        return f"{pname}({mname})"

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
    def load_from_json(cls, jsondata: str):
        kwargs = json.loads(jsondata)
        return cls(**kwargs)

    def dump(self, dumpfile: str = None):
        dumpfile = dumpfile or self.dumpfile
        with open(dumpfile, 'a', encoding='utf-8') as f:
            f.write(f"{self.data_json}\n")

    def get(self, item: str):
        try:
            return self[item]
        except:
            return self.kwargs.get(item)

    def update(self, other):
        update_status = True
        pdata = other.data
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
    def concat(*others: tuple):
        length = len(others)
        if length == 1:
            return others[0]

        all_keys = set.union(*[other.attrs for other in others])
        common_keys = set.intersection(*[other.attrs for other in others])
        common_value_keys = []
        concats = {}

        for key in common_keys:
            values = [other.get(key) for other in others]
            values_set = set(values)
            if len(values_set) == 1:
                common_value_keys.append(key)
                concats[key] = values[0]
            else:
                vcount = ((value, values.count(value)) for value in values_set)
                vcount_sorted = sorted(vcount, key=lambda x: (x[1], x[0]), reverse=True)
                value, vcount = vcount_sorted[0]
                if vcount >= 2:
                    concats[key] = f"{value}({length}->{vcount})"

        special_keys = all_keys - set(common_value_keys)
        specials = [{attr: other.get(attr) for attr in other.attrs if attr in special_keys} for other in others]
        specials = [{k: concats.get(k) if concats.get(k) and concats.get(k).startswith(v) else v 
                    for k, v in special.items()} for special in specials]
        concats['specials'] = specials
        return Phone(**concats)
