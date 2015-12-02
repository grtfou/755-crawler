#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get talkID from main page
"""
import re
import requests

from local_settings import url


def __parser(raw_data):
    regex = re.compile(r'talkId\s*:(.*)')
    result = regex.search(raw_data)
    print(result.group(0))


def get_talk_id(url):
    session = requests.session()
    repo = session.get(url)

    if repo.status_code == 200:
        __parser(repo.text)

if __name__ == '__main__':
    get_talk_id(url)
