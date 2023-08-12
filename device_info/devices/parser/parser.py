# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 15:48:11
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-08-12 15:25:29
# @github: https://github.com/longfengpili


import itertools

from lxml import etree
from lxml.etree import Element as elem


class Parser:

    def __init__(self):
        pass

    def etree_html(self, res: str):
        html = etree.HTML(res)
        return html

    def get_elem(self, elem: elem, *paths: tuple[str]):
        if elem is None:
            return elem

        for path in paths:
            infos = elem.xpath(path)
            if infos:
                break

        infos = [info.strip().replace('\n', ' ') if isinstance(info, str) else info for info in infos]
        return infos

    def get_elems(self, elem: elem, *mpaths: tuple[tuple[str, tuple[str]]]):
        elems = {}
        for mpath in mpaths:
            name, paths = mpath
            infos = self.get_elem(elem, *paths)
            value = '||'.join(infos) if isinstance(infos[0], str) else infos
            elems[name] = value

        return elems
