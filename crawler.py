#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main function
"""
import os
import re
import sys
import time
import argparse
from datetime import datetime

import aiohttp
import asyncio
import requests

from talk_id import get_talk_id


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

    def download_file(self, url, filename, dest_path):
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

            output_path = "{}{}{}".format(dest_path, os.sep, filename)
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

    async def run(self, client, talk_id, username, stop_time=0):
        page_limit = 100

        img_count = 1
        video_count = 1
        last_image_t = 0
        last_video_t = 0
        for post_rec in range(1, 99999999, 100):
            payload = {
                'direction': 'NEXT',
                'limit': page_limit,
                'postId': post_rec,  # test 6000 (photos and videos)
                'talkId': talk_id,
            }

            r = self.session.get(self.url, params=payload)
            if r.status_code != 200:
                # handle connection fail
                print('Connection fail')
                return
            else:
                raw_data = r.json()

                # handle no post
                if not raw_data['posts']:
                    print('Finished !')
                    return

                # Created directories for store files
                dest_img_path = 'downloads{}{}{}'.format(
                    os.sep, username, os.sep, self.img_path)
                dest_video_path = 'downloads{}{}{}'.format(
                    os.sep, username, os.sep, self.video_path)
                if not os.path.isdir(dest_img_path):
                    os.makedirs(dest_img_path)
                if not os.path.isdir(dest_video_path):
                    os.makedirs(dest_video_path)

                for i in range(page_limit):
                    # handle one page doesn't have 100 posts
                    try:
                        post_time = int(raw_data['posts'][i]['time'])
                    except IndexError:
                        print('Finished !')
                        return

                    # if msg time too old, stop download
                    if int(post_time) < stop_time:
                        break

                    url = raw_data['posts'][i]['body'][0].get('image', '')
                    if url:
                        # file_date = url.split('/')[4]
                        file_date = datetime.utcfromtimestamp(post_time
                                                              ).strftime("%y%m%d%H%M%S")
                        # handle duplication file
                        if file_date == last_image_t:
                            img_count += 1
                        else:
                            img_count = 1
                            last_image_t = file_date

                        self.download_file(
                            url, "{}_{}.jpg".format(file_date, img_count), dest_img_path)

                    url = raw_data['posts'][i]['body'][0].get('movieUrlHq', '')
                    if url:
                        file_date = datetime.utcfromtimestamp(post_time
                                                              ).strftime("%y%m%d%H%M%S")
                        # handle duplication file
                        if file_date == last_video_t:
                            video_count += 1
                        else:
                            video_count = 1
                            last_video_t = file_date

                        self.download_file(
                            url, "{}_{}.mp4".format(file_date, video_count), dest_video_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download 755 photos + videos.')
    parser.add_argument('url', type=str, nargs='?',
                        help='Target Url: ex. http://7gogo.jp/talks/examples')
    parser.add_argument('stop_time', type=str, nargs='?', default=None,
                        help='Date (yy/mm/dd): ex. 141105')
    args = parser.parse_args()

    if args.url and args.stop_time:
        try:
            args.stop_time = time.mktime(time.strptime(args.stop_time, "%y%m%d"))
        except ValueError:
            parser.print_help()
            sys.exit()

        my_cwawler = Crawler()
        talk_id, username = get_talk_id(args.url)

        loop = asyncio.get_event_loop()
        with aiohttp.ClientSession(loop=loop) as client:
            loop.run_until_complete(my_cwawler.run(
                client, talk_id, username, args.stop_time))

    parser.print_help()
