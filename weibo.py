# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

import requests
from pyquery import PyQuery as pq
from urllib import urlencode, unquote


host = 'm.weibo.cn'
base_url = 'https://%s/api/container/getIndex?' % host
user_agent = 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 wechatdevtools/0.7.0 MicroMessenger/6.3.9 Language/zh_CN webview/0'

headers = {
    'Host': host,
    'Referer': 'https://m.weibo.cn/u/1665372775',
    'User-Agent': user_agent
}


# Get the info of user
def get_user_info(page):
    params = [
        ('type', 'uid'),
        ('value', 6576856192),
        ('containerid', 1076036576856192),
        ('page', page)
    ]

    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)


# Get the basic info for each mblog
# 目前没有解决的问题(04/29/2019)：text中的文本为Unicode编码，暂时无法显示成中文（单独print text时可解码）
# 暂时保存几个主要人员的Unicode编码用于信息提取
# 孟美岐： \u5b5f\u7f8e\u5c90
# 吴宣仪： \u5434\u5ba3\u4eea
# 杨超越： \u6768\u8d85\u8d8a
def parse_page(json):
    items = json.get('data').get('cards')
    for item in items:
        item = item.get('mblog')
        if item:
            content = pq(item.get("text")).text()  # 仅提取内容中的文本
            # print content
            data = {
                'id': item.get('id'),
                'text': content,
                'attitudes': item.get('attitudes_count'),
                'comments': item.get('comments_count'),
                'reposts': item.get('reposts_count')
            }
            yield data


def get_page_info(page_id, max_id):
    if max_id != None:
        params = [
            ('id', page_id),
            ('mid', page_id),
            ('max_id', max_id),
            ('max_id_type', 0)
        ]
    else:
        params = [
            ('id', page_id),
            ('mid', page_id),
            ('max_id_type', 0)
        ]

    url = 'http://' + host + '/comments/hotflow?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('抓取错误', e.args)


def get_comments(json):
    global max_id
    max_id = json.get('data').get('max_id')

    items = json.get('data').get('data')
    for item in items:
        data = {
            'id': item.get( 'id' ),
            'time': item.get( 'created_at' ),
            'floor': item.get( 'floor_number' ),
            'like': item.get( 'like_count' ),
            'likeByAuthor': item.get( 'isLikedByMblogAuthor' ),
            'text': pq(item.get("text")).text()
        }
        yield data

max_id = None

if __name__ == '__main__':
    for page in range(1, 2): 
        json = get_user_info(page)
        results = parse_page(json)
        for result in results:
            max_id = None
            for i in range(2):
                print result['id'], max_id, i
                json_page = get_page_info(result['id'], max_id)
                comments = get_comments( json_page )
                for comment in comments:
                    print comment

    # results = results.drop_duplicates()
    print "中文测试"