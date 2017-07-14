# -*- coding: utf8 -*-
import redis
import requests
import json
import time

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=1)
SAVE_MSG_URL = 'https://jh.qiuxiaokun.com/api/chat/save/'


def get_access_token(url, username, password, client_id, client_secret):
    data = {
        'username': username,
        'password': password,
        'grant_type': 'password',
        'client_id': client_id,
        'client_secret': client_secret
    }
    r = requests.post(url=url, data=data)
    token_info = r.json()
    token_info['create_time'] = str(time.time())
    REDIS_CLIENT.set(
        'juhui_access_token_' + username, token_info)
    return token_info


def save_chat_msg(user_id, wine_code, msg_type, content, video_img, create_at):
    data = {
        'user_id': user_id,
        'wine_code': wine_code,
        'msg_type': msg_type,
        'content': content,
        'video_img': video_img,
        'create_at': create_at
    }
    r = requests.post(url=SAVE_MSG_URL, data=data)
    try:
        save_info = r.json()
        if save_info['code'] == '000000':
            return True
        else:
            return False
    except Exception:
        return False


def listen():
    ps = REDIS_CLIENT.pubsub()
    ps.subscribe(['save_msg', 'last_price'])
    for item in ps.listen():
        print('item is {0}'.format(item))
        if item['type'] == 'message':
            params = item['data']
            print('item data is {0}'.format(params))
            try:
                params = json.loads(params.decode('utf8').replace('\'', '\"'))
                if item['channel'].decode('utf8') == 'save_msg':
                    save_info = save_chat_msg(
                        params['user_id'],
                        params['wine_code'],
                        params['type'],
                        params['content'],
                        params['video_img_url'],
                        params['create_at']
                    )
                    print('Save chat message is successful? {0}'.format(save_info))
                elif item['channel'].decode('utf8') == 'last_price':
                    save_info = (
                        params['code'],
                        params['price'],
                        params['time']
                    )
                    print('last price info is {0}'.format(save_info))
                else:
                    pass
            except Exception:
                pass


if __name__ == '__main__':
    print('redis pubsub listening...')
    listen()
