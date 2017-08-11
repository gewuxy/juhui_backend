# -*- coding: utf8 -*-
import redis
import requests
import json
import time
import traceback

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=1)
SAVE_MSG_URL = 'https://jh.qiuxiaokun.com/api/chat/save/'
GET_DETAIL_INFO = 'https://jh.qiuxiaokun.com/api/wine/detail/'
EMIT_DETAIL_INFO = 'http://39.108.142.204:8001/last_price/'


# 请求url（/o/token/）获取access_token，并将它存到redis中
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


# 存储公众号中的聊天记录
def save_chat_msg(user_id, wine_code, msg_type, content, video_img, create_at):
    data = {
        'user_id': user_id,
        'wine_code': wine_code,
        'msg_type': msg_type,
        'content': content,
        'video_img': video_img,
        'create_at': create_at
    }
    # headers = {
    #     'Content-type': 'application/json; charset=utf-8'
    # }
    r = requests.post(url=SAVE_MSG_URL, data=data)
    try:
        save_info = r.json()
        print('save_info r.json is {0}'.format(save_info))
        if save_info['code'] == '000000':
            return True
        else:
            return False
    except Exception:
        traceback.print_exc()
        return False


# 获取最新详情数据，用于广播
def get_detail_info(code):
    print('enter get_detal_info===')
    data = {
        'code': code
    }
    # headers = {
    #     'Content-type': 'application/json; charset=utf-8'
    # }
    r = requests.post(url=GET_DETAIL_INFO, data=data)
    try:
        save_info = r.json()
        print('get_detail_info save_info is {0}'.format(save_info))
        if save_info['code'] == '000000':
            return True, save_info
        else:
            return False, save_info
    except Exception:
        traceback.print_exc()
        return False, {}

def listen():
    ps = REDIS_CLIENT.pubsub()
    ps.subscribe(['save_msg', 'last_price', 'token'])
    for item in ps.listen():
        print('item is {0}'.format(item))
        if item['type'] == 'message':
            params = item['data']
            print('item data is {0}'.format(params))
            try:
                params = json.loads(params.decode('utf8').replace('\'', '\"'))
                print('params is {0}'.format(params))
                if item['channel'].decode('utf8') == 'token':
                    token_info = get_access_token(
                        params['url'],
                        params['username'],
                        params['password'],
                        params['client_id'],
                        params['client_secret']
                    )
                    print('username access_token is {0}'.format(token_info))
                elif item['channel'].decode('utf8') == 'save_msg':
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
                    rval, save_info = get_detail_info(params['code'])
                    if rval:
                        save_info['data']['code'] = params['code']
                        save_info['data']['time'] = params['time']
                        print('last price info is {0}'.format(save_info))
                        url = 'http://39.108.142.204:8001/last_price/'
                        r = requests.post(url, data=save_info['data'])
                        print('get last_price content is {0}'.format(r.content))
                        if r.content == b'000000':
                            print('广播最新详情信息<<<成功>>>！')
                        else:
                            print('广播最新详情信息<<<失败>>>！')
                    '''
                    save_info = (
                        params['code'],
                        params['price'],
                        params['time']
                    )
                    '''
                else:
                    pass
            except Exception:
                traceback.print_exc()
                pass


if __name__ == '__main__':
    print('redis pubsub listening...')
    listen()
