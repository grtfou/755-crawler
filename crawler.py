#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main function
"""
import os
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
    img_path = 'images'

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

            output_path = "{}{}{}".format(self.img_path, os.sep, filename)
            if not os.path.exists(output_path):
                with open(output_path, 'wb') as o_file:
                    for chunk in req.iter_content(1024):
                        dl_progress += len(chunk)
                        o_file.write(chunk)

                        # Download progress report
                        percent = 100.0 * dl_progress / int(total_length)
                        sys.stdout.write("\r%2d%%" % percent)
                        sys.stdout.flush()

                print('')
            else:
                print('File exist')
        else:
            print('Visit website fail')

    async def run(self, client, talk_id, stop_time=0):
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

            if not os.path.isdir(self.img_path):
                os.makedirs(self.img_path)

            count = 0
            for i in range(100):
                # if msg time too old, stop download
                if int(raw_data['posts'][i]['time']) < stop_time:
                    break

                url = raw_data['posts'][i]['body'][0].get('image', '')
                if url:
                    count += 1
                    file_date = url.split('/')[4]
                    self._download(url, "{}_{}.jpg".format(file_date, count))


if __name__ == '__main__':
    my_cwawler = Crawler()
    stop_time = 1445687490

    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    loop.run_until_complete(my_cwawler.run(client, talk_id, stop_time))
    client.close()
