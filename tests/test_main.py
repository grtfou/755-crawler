#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing main function
"""
import asyncio

from crawler import Crawler
from talk_id import get_talk_id


def test_main_funtion():
    url = "http://7gogo.jp/talks/YtykfykuJfMT"

    my_tester = Crawler()
    talk_id, username = get_talk_id(url)

    loop = asyncio.get_event_loop()
    task = asyncio.async(my_tester.run(talk_id, username, 1417268169))
    loop.run_until_complete(task)
