# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-08-11 15:27:12
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2023-08-12 15:26:19
# @github: https://github.com/longfengpili


from lxml.etree import Element as elem

from devices.parser import Parser
from devices.requester import Requester

import logging
glogger = logging.getLogger(__name__)


class Geekbench(Requester, Parser):

    def __init__(self):
        super(Geekbench, self).__init__()

    @property
    def base_url(self):
        base_url = 'https://browser.geekbench.com'
        return base_url

    @property
    def headers(self):
        headers = {
            'Cookie': '_browse_session=B7U7kJoPc9ZGhUOnI87iXXoBGVOSFB7cdLqCePaN9nRrbrKurIKjJNM000s%2B3Hn%2F1X%2Fzuxeq%2Bnzheuiij0Ocb9E6rV2p7M5NWV51bnSq%2F1cq5cSrrQv0cU0ea6KtfxhGucqmplFHLWFWevZgqqhaJAWJ%2BasGb5QvSz%2Fm--rtR%2FHvz22%2BtTGsrA--SBxnSdo6e8EsST1U8Z0Aaw%3D%3D',  # noqa: E501
            'Host': 'browser.geekbench.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        return headers

    def request(self, pname: str):
        url = f"{self.base_url}/search"
        params = {
            'utf8': '✓',
            'q': pname
        }

        res = self.base_request(url, params)
        nomatch = 'not match any Geekbench 6 CPU'
        if nomatch in res:
            glogger.warning(f'{pname} {nomatch} !')
            params['k'] = 'v5_cpu'
            res = self.base_request(url, params)

        return res

    def get_pkinds(self, idx: int, pname: str):
        res = self.request(pname)
        html = self.etree_html(res)
        # main page
        pkinds = self.get_elem(html, './/div[@class="col-12 list-col"]')
        return pkinds

    def parse_pkind(self, pkind: elem):
        mpaths = (
            ('pname', ('.//div[@class="col-12 col-lg-4"]/a/text()', )),
            ('purl', ('.//div[@class="col-12 col-lg-4"]/a/@href', )),
            ('psoc', ('.//div[@class="col-12 col-lg-4"]/span[2]/text()', )),
            ('sc_score', ('.//div[@class="col-6 col-md-3 col-lg-2"][3]/span[2]/text()', )),
            ('mc_score', ('.//div[@class="col-6 col-md-3 col-lg-2"][4]/span[2]/text()', ))
        )

        pkind = self.get_elems(pkind, *mpaths)
        pkind['purl'] = self.base_url + pkind['purl']
        return pkind
