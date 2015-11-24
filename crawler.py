#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main function
"""
import aiohttp
import asyncio

from local_settings import talk_id

class Crawler(object):
    """
    crawler for download 755 photos
    """
    url = 'http://7gogo.jp/api/talk/post/list'
    def __init__(self):
        pass

    async def run(self, client, talk_id):
        payload = {
            'direction': 'PREV',
            'limit': 100,
            'postId': 2000,
            'talkId': talk_id,
        }
        async with client.get(self.url, params=payload) as resp:
            return await resp.read()

if __name__ == '__main__':
    my_cwawler = Crawler()

    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    raw_html = loop.run_until_complete(my_cwawler.run(client, talk_id))
    print(raw_html)
    client.close()

