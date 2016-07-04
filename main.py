#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import asyncio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from crawler import Crawler
# from talk_id import get_talk_id


class CrawlerWidget(BoxLayout):
    def check_status(self, url, stop_date=160704):
        print('URL is: {txt}'.format(txt=url))
        # print('Stop Date is: {txt}'.format(txt=stop_date))

        if url and stop_date:
            try:
                stop_date = time.mktime(time.strptime(stop_date, "%y%m%d"))
                talk_id = url.split('/')[-1]
                my_cwawler = Crawler(talk_id)
                # talk_id, username = get_talk_id(url)

                loop = asyncio.get_event_loop()
                task = asyncio.async(my_cwawler.run(stop_date))
                loop.run_until_complete(task)
            except ValueError:
                print('Error: Stop time format')


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

    def build(self):
        return CrawlerWidget()

if __name__ == '__main__':
    Window.size = (900, 600)
    MainApp().run()
