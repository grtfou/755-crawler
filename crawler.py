#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main function
"""
import os
import re
import sys
from datetime import datetime

import aiohttp
import asyncio
import requests

from local_settings import talk_id


class Crawler(object):
    """
    Crawler for download 755 photos.
    """
    url = 'http://7gogo.jp/api/talk/post/list'
    img_path = 'images'
    video_path = 'videos'

    def __init__(self):
        self.session = requests.session()
        pass

    def download_file(self, url, filename, file_type):
        """
        Download photo.

        Args:
            (String) url
            (String) file name (output)
        """
        req = self.session.get(url, stream=True)
        if req.status_code == 200:
            total_length = req.headers.get('content-length')
            dl_progress = 0

            if file_type == 'images':
                folder = self.img_path
            else:
                folder = self.video_path
            output_path = "{}{}{}".format(folder, os.sep, filename)
            if not os.path.exists(output_path):
                with open(output_path, 'wb') as o_file:
                    for chunk in req.iter_content(1024):
                        dl_progress += len(chunk)
                        o_file.write(chunk)

                        # Download progress report
                        percent = dl_progress / int(total_length)
                        sys.stdout.write("\r{}: {:.2%}".format(filename, percent))
                        sys.stdout.flush()

                print('')
            else:
                print('{}: File exist'.format(filename))
        else:
            print('Visit website fail')

    async def run(self, client, talk_id, stop_time=0):
        page_limit = 100

        for post_rec in range(0, 99999999, 100):
            payload = {
                'direction': 'PREV',
                'limit': page_limit,
                'postId': post_rec,  # test 6000 (photos and videos)
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
                    print('Finished !')
                    sys.exit()

                # Created directories for store files
                if not os.path.isdir(self.img_path):
                    os.makedirs(self.img_path)
                if not os.path.isdir(self.video_path):
                    os.makedirs(self.video_path)

                img_count = 1
                video_count = 1
                last_image_t = 0
                last_video_t = 0
                for i in range(page_limit):
                    # if msg time too old, stop download
                    post_time = int(raw_data['posts'][i]['time'])
                    if int(post_time) < stop_time:
                        break

                    url = raw_data['posts'][i]['body'][0].get('image', '')
                    if url:
                        # file_date = url.split('/')[4]
                        file_date = datetime.utcfromtimestamp(post_time).strftime("%Y%m%d")
                        # handle duplication file
                        if file_date == last_image_t:
                            img_count += 1
                        else:
                            img_count = 1
                            last_image_t = file_date

                        self.download_file(url, "{}_{}.jpg".format(file_date, img_count), 'images')

                    url = raw_data['posts'][i]['body'][0].get('movieUrlHq', '')
                    if url:
                        file_date = datetime.utcfromtimestamp(post_time).strftime("%Y%m%d")
                        # handle duplication file
                        if file_date == last_video_t:
                            video_count += 1
                        else:
                            video_count = 1
                            last_video_t = file_date

                        self.download_file(url, "{}_{}.mp4".format(file_date, video_count), 'videos')


if __name__ == '__main__':
    my_cwawler = Crawler()
    stop_time = 1445687490

    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as client:
        loop.run_until_complete(my_cwawler.run(client, talk_id, stop_time))
