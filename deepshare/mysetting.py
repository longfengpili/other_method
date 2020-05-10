'''
@Author: longfengpili
@Date: 2019-11-04 07:54:40
@LastEditTime: 2019-11-04 07:59:33
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-




headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
    'App-Id': 'appuaAoe86p4947',
    'Connection': 'keep-alive',
    'Content-Length': '108',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': '',
    'Host': 'ai.deepshare.net',
    'Origin': 'https://ai.deepshare.net',
    'Referer': 'https://ai.deepshare.net/detail/p_5cd6789610455_BJKaYtXr/6',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

headers_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

headers_video = {
    "Host": "encrypt-k-vod.xiaoe-tech.com",
    "Origin": "https://ai.deepshare.net",
    "Referer": "https://ai.deepshare.net/detail/v_5dde024607f1a_kBgHo2E4/3?from=p_5cd6789610455_BJKaYtXr&type=6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
}

goods_url = 'https://ai.deepshare.net/page/464061'
main_api = 'https://ai.deepshare.net/api/xe.goods.relation.get/1.0.0'
page_api = 'https://ai.deepshare.net/api/xe.goods.detail.get/2.0.0'

app_id = 'appuaAoe86p4947'

# goods_id = {
#   # 'statistical': '{"page_size":20,"goods_id":"p_5da4286d52af8_sA6m5IDR","last_id":"","goods_type":6,"resource_type":[1,2,3,4]}',
#   # 'deeplearn_flower': '{"page_size":20,"goods_id":"p_5d72442b5f162_hKJypuaW","last_id":"","goods_type":6,"resource_type":[1,2,3,4]}',
#   'actual_ml': '{"page_size":20,"goods_id":"p_5cc55da2135c9_lBkG55A4","last_id":"","goods_type":6,"resource_type":[1,2,3,4]}',
#   'competition': '{"page_size":20,"goods_id":"p_5d2ef66d19c84_IXzIXjMm","last_id":"","goods_type":6,"resource_type":[1,2,3,4]}',
#   'ai_python_base': '{"page_size":20,"goods_id":"p_5d78a35ad92fc_QgzkKESa","last_id":"","goods_type":6,"resource_type":[1,2,3,4]}',
#   'stanford_CS224n_cv': '{"page_size":20,"goods_id":"p_5da42b4503718_H8p24cqF","last_id":"","goods_type":6,"resource_type":[1,2,3,4]}',
#   'paper_nlp': '{"page_size":20,"goods_id":"p_5ce3de7ff113d_1Pn4XBFO","last_id":"","goods_type":6,"resource_type":[1,2,3,4]}',
#   'paper_cv': '{"page_size":20,"goods_id":"p_5ce3df0c0a7ca_8y0GRPRx","last_id":"","goods_type":6,"resource_type":[1,2,3,4]}',

# }



