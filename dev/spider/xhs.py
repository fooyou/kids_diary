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

cookie = 'xhsTrackerId=84620b55-8e18-404d-c0bd-e118c1cd093d; extra_exp_ids=wx_launch_open_app_duration_origin,ques_exp2; xhsTracker=url=index&searchengine=baidu; a1=183b61e80f8cuhbj8xwocmjzoznis4rnn5x5z12m500000199893; gid=yYqDKydYWKI0yYqDKydY82yJiYS7xDVYCElSC626VuluI2883M4FIu888yjjYjq8f8JD24Y8; gid.sign=NnfMaopTWwzI0jFsZfjGICPtJV0=; gid.ss=gSMQ9UOnDuZwH2oRGJG6BW6e4grs67TaYpnrW+8Wmd32I71PMMYY2MqCe+nSTxc8; customerBeakerSessionId=464aca47c3d447fc6895a5ab1ba8690dd11c9ffcgAJ9cQAoWBAAAABjdXN0b21lclVzZXJUeXBlcQFLAVgOAAAAX2NyZWF0aW9uX3RpbWVxAkdB2NBDhlVwpFgJAAAAYXV0aFRva2VucQNYQQAAADFlOGFmYzQ1MjNhMzRiNmVhMDg3YWQ1ZmQ4MWFhZTI2LTU2MDczYmM3ZTZjMTQ5OGE4ZjE1ZjMwMzNiY2RhNWNlcQRYAwAAAF9pZHEFWCAAAAA2NDQ1YzZlMzcwNTY0ZDdhYTg0YTY5ODNkZjllNDFiY3EGWA4AAABfYWNjZXNzZWRfdGltZXEHR0HY0EOGVXCkWAYAAAB1c2VySWRxCFgYAAAANjE1ZmY4YTUwMDAwMDAwMDAyMDI1MmZjcQl1Lg==; customerClientId=547753442419221; timestamp2=1665207834118d2f88415009b466293f0c752125c54dd186e43b4cd87ee1fbb; timestamp2.sig=L0kySbn7Fx4yVqnhhsF10Q0mwxa9ql8hpzhAniNE77M; galaxy.creator.beaker.session.id=1665207834184001767618'

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
