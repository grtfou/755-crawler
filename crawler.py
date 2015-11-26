#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main function
"""
import re
import random
import sys

import aiohttp
import asyncio
import requests

from local_settings import talk_id

class Crawler(object):
    """
    crawler for download 755 photos
    """
    url = 'http://7gogo.jp/api/talk/post/list'
    def __init__(self):
        self.session = requests.session()
        pass

    def _download(self, url, filename):
        """
        Download photo

        Args:
            (String) url
            (String) file name (output)
        """
        # urllib.urlretrieve(url, filename, self._report_hook)

        req = self.session.get(url, stream=True)
        if req.status_code == 200:
            total_length = req.headers.get('content-length')
            dl_progress = 0

            with open(filename, 'wb') as o_file:
                for chunk in req.iter_content(1024):
                    dl_progress += len(chunk)
                    o_file.write(chunk)

                    # Download progress report
                    percent = 100.0 * dl_progress / int(total_length)
                    sys.stdout.write("\r%2d%%" % percent)
                    sys.stdout.flush()
        else:
            print('Visit website fail')

    async def run(self, client, talk_id):
        page_limit = 100

        payload = {
            'direction': 'PREV',
            'limit': page_limit,
            'postId': 6000,  # test 6000
            'talkId': talk_id,
        }

        r = self.session.get(self.url, params=payload)
        if r.status_code != 200:
            # handle connection fail
            sys.exit()
        else:
            raw_data = r.json()

            # handle no post
            if not raw_data['posts']:
                sys.exit()

            count = 0
            for i in range(100):
                url = raw_data['posts'][i]['body'][0].get('image', '')
                if url:
                    count += 1
                    file_date = url.split('/')[4]
                    self._download(url, "{}_{}.jpg".format(file_date, count))


if __name__ == '__main__':
    my_cwawler = Crawler()

    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    loop.run_until_complete(my_cwawler.run(client, talk_id))
    client.close()

