import time
import random
import requests

POST_ID = "1"
TALK_ID = "test"
INIT_TOKEN = "abc="

# cookies = {
#     "NANAGOGOSESSIONID": "",
#     "NANAGOGOTRACKINGSESSIONID": "",
#     "_ga": "",
#     "_gat_UA-47494750-1": "",
#     "_gid": ""
# }

headers = {
    'Origin': 'https://7gogo.jp',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)'
                   ' AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/70.0.3538.110 Safari/537.36'),
    'Referer': f'https://7gogo.jp/{TALK_ID}',
    'X-7gogo-WebAuth': INIT_TOKEN
}


def get_token(s=requests.Session()):
    url = 'https://api.7gogo.jp/web/v2/token/security/publish'
    token_data = 'category=talk&pageId=talk&pageModuleId='
    repo = s.post(url, data=token_data, headers=headers)
    return repo.json()['data']['token']


def main():
    with requests.Session() as s:
        url = (f'https://api.7gogo.jp/web/v2/talks/'
               f'{TALK_ID}/posts/{POST_ID}/good')

        for i in range(random.randint(30, 100)):  # requests
            try:
                add_rate = random.randint(1, 32)  # clap hands
                data = f"talkId={TALK_ID}&postId={POST_ID}&count={add_rate}"
                repo = s.post(url, data=data, headers=headers)
                if 'data' not in repo.json():
                    print('Refresh token')
                    token = get_token(s)
                    headers['X-7gogo-WebAuth'] = token
                else:
                    print(repo.json()['data'])
            except ConnectionResetError:
                # sleep to avoid server block
                time.sleep(random.randint(40, 120))


if __name__ == '__main__':
    main()
