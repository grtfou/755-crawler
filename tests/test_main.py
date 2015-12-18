#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing main function
"""
import aiohttp
import asyncio

from crawler import Crawler
from talk_id import get_talk_id


def test_main_funtion():
    url = "http://7gogo.jp/talks/YtykfykuJfMT"

    my_tester = Crawler()
    talk_id, username = get_talk_id(url)

    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as client:
        loop.run_until_complete(my_tester.run(client, talk_id, username, 1417268169))
