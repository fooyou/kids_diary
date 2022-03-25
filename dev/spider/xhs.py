#!/usr/bin/env python
# coding: utf-8
"""
@file: xhs.py
@author: Joshua Liu
@email: liuchaozhen@haier.com
@create: 2022-03-13 15:03:55
@update: 2022-03-25 20:03:09
@desc: 爬取小红书视频的 <video>标签地址
"""
import re
import json
import requests

cookie = 'xhsTrackerId=b6201c54-c340-47ab-c75d-735fdaee0ee6; customerClientId=893568014906763; xhsTracker=url=noteDetail&xhsshare=CopyLink; smidV2=20220228190953cacbedd0b3bafe2b144a50f644868f84001dad92a8fe92410; timestamp2=20220323aacf02b07ee68714aa4f6e9b; timestamp2.sig=tl-8Bf0TqmF_YYTOuzg3EBQNcxsDgUQelbk4oHOCrk8; galaxy.creator.beaker.session.id=1648017873099052025511; extra_exp_ids=supervision_exp,supervision_v2_exp,commentshow_clt1,gif_clt1,ques_clt2'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': cookie,
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
}

base_url = "https://www.xiaohongshu.com/discovery/item/{}"
regex = r'"video":{(.*?)}'
patten = re.compile(regex)
session = requests.Session()

def get_video_url(items):
    for i, item in enumerate(items):
        url = base_url.format(item["name"])
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            continue
        matches = patten.findall(response.text)
        if matches:
            content = "{%s}" % matches[0]
            obj = json.loads(content)
            item["value"] = obj.get("url")
            print(item)
    return items


def read_json(path):
    with open(path, encoding="utf-8") as f:
        items = json.load(f)
    return items


def write_json(path, items):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=4)


def main():
    data_path = "../../_data/video.json"
    items = read_json(data_path)
    items = get_video_url(items)
    write_json(data_path, items)


if __name__ == "__main__":
    main()
