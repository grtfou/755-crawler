# 755-Crawler
A web crawler that visit [755 website][1] for download photo and video.

## Requirements
* Python >= 3.4
* requests >= 2.8.1

## How to Use
#### [Source code]
Download the source code and uncompress
```
$ pip install -r requirements.txt
$ python crawler.py [url] [stop time (yy/mm/dd)]

# for example
$ python crawler.py  https://7gogo.jp/hori-miona 160303
```
#### [GUI]
Please install [Kivy][2] in your platform.

You could see **requirements_gui.txt** to check Kivy libraries.

## Licence
MIT License

[1]: http://7gogo.jp "755"
[2]: http://kivy.org "kivy"
