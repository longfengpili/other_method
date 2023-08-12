# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 15:48:11
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-11 18:28:46
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

    def get_elems(self, elems: list[elem], *paths: tuple[tuple[str, str]], isfirst: bool = True):
        _elems = {}
        for _elem, _paths in itertools.product(elems, paths):
            name, path = _paths
            _elems[name] = self.get_elem(_elem, *path, isfirst=isfirst)

        return _elems
