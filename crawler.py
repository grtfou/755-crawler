"""
Main function
"""
import os
import sys
import time
import asyncio
import argparse
from datetime import datetime

import requests


class Crawler(object):
    """
    Crawler for download 755 photos.
    """
    img_path = 'images'
    video_path = 'videos'

    def __init__(self, talk_id):
        self.session = requests.session()
        self.talk_id = talk_id
        self.url = f'https://api.7gogo.jp/web/v2/talks/{talk_id}/posts'

        # Created directories for store files
        self.dest_img_path = 'downloads{}{}{}{}'.format(
            os.sep, self.talk_id, os.sep, self.img_path)
        self.dest_video_path = 'downloads{}{}{}{}'.format(
            os.sep, self.talk_id, os.sep, self.video_path)
        if not os.path.isdir(self.dest_img_path):
            os.makedirs(self.dest_img_path)
        if not os.path.isdir(self.dest_video_path):
            os.makedirs(self.dest_video_path)
        # -

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

            output_path = f"{dest_path}{os.sep}{filename}"
            if not os.path.exists(output_path):
                with open(output_path, 'wb') as o_file:
                    for chunk in req.iter_content(1024):
                        dl_progress += len(chunk)
                        o_file.write(chunk)

                        # Download progress report
                        percent = dl_progress / int(total_length)
                        print(f"\r{filename}: {percent:.2%}", end='\r')

                print('')
            else:
                print(f'{filename}: File exist')
        else:
            print('Visit website fail')

    def __parse(self, raw_post, post_time):
        # if msg time too old, stop download
        # if int(post_time) < stop_time:
        #     break

        # Image
        raw_body = raw_post.get('body', [])
        for i in range(0, len(raw_body)):
            # Image & video
            image_url = raw_body[i].get('image', '')
            video_url = raw_body[i].get('movieUrlHq', '')

            # filename
            file_date = datetime.utcfromtimestamp(
                post_time).strftime("%y%m%d")
            rand_num = str(post_time)[-3:]  # prevent duplicate filename

            if image_url and image_url.startswith("http"):
                self.download_file(
                    image_url,
                    f"{file_date}_{rand_num}.jpg",
                    self.dest_img_path)

            if video_url and video_url.startswith("http"):
                self.download_file(
                    video_url,
                    f"{file_date}_{rand_num}.mp4",
                    self.dest_video_path)

    async def run(self, stop_time=0):
        page_limit = 100

        post_rec = 1
        while True:
            payload = {
                'direction': 'NEXT',   # NEXT, PREV
                'limit': page_limit,
                'targetId': post_rec,
            }
            post_rec += 100

            r = self.session.get(self.url, params=payload)
            if r.status_code != 200:
                # handle connection fail
                print('Error: Connection fail')
                break
            else:
                raw_data = r.json()
                content = raw_data['data']

                # handle no post
                if not content:
                    print('Finished !')
                    break

                for i in range(page_limit):
                    try:
                        post_time = int(content[i]['post']['time'])
                    except IndexError:
                        print('Finished !')
                        break

                    if 'post' in content[i]:
                        owner = content[i]['post']['owner']
                        if owner is None:  # postType = 100
                            # This post was deleted
                            continue
                        else:
                            self.__parse(
                                 content[i]['post'], post_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download 755 photos + videos.')
    parser.add_argument('url', type=str, nargs='?',
                        help='Target Url: ex. http://7gogo.jp/talks/examples')
    parser.add_argument('stop_time', type=str, nargs='?', default=None,
                        help='Date (yy/mm/dd): ex. 141105')
    args = parser.parse_args()

    if args.url and args.stop_time:
        try:
            args.stop_time = time.mktime(
                time.strptime(args.stop_time, "%y%m%d"))
        except ValueError:
            parser.print_help()
            print('Error: Stop Date format is wrong')
            sys.exit()

        talk_id = args.url.split('/')[-1]
        my_cwawler = Crawler(talk_id)

        loop = asyncio.get_event_loop()
        task = asyncio.Task(my_cwawler.run(args.stop_time))
        loop.run_until_complete(task)
    else:
        parser.print_help()
