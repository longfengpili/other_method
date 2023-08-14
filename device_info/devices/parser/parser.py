# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 15:48:11
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-08-14 16:51:41
# @github: https://github.com/longfengpili

from lxml import etree
from lxml.etree import Element as elem


class Parser:

    def __init__(self):
        pass

    def etree_html(self, res: str):
        html = etree.HTML(res)
        return html

    def get_elem(self, elem: elem, *paths: tuple[str]):
        infos = []
        if elem is None:
            return elem

        for path in paths:
            _infos = elem.xpath(path)
            if _infos:
                infos.extend(_infos)

        infos = [info.strip().replace('\n', ' ') if isinstance(info, str) else info for info in infos]
        return infos

    def get_elem_mpath(self, elem: elem, *mpaths: tuple[tuple[str, tuple[str]]]):
        elem_mpath = {}
        for mpath in mpaths:
            name, paths = mpath
            infos = self.get_elem(elem, *paths)
            # if name == 'size':
            #     print(etree.tostring(elem))
            #     print(infos)
            value = '||'.join(infos) if infos and isinstance(infos[0], str) else '' if not infos else infos
            elem_mpath[name] = value

        return elem_mpath

    def get_elems_kv(self, elems: list[elem], kpaths: tuple[str], vpaths: tuple[str]):
        meles = {}
        for _elem in elems:
            name = self.get_elem(_elem, *kpaths)[0]
            value = self.get_elem(_elem, *vpaths)[0]
            meles[name] = value

        return meles
