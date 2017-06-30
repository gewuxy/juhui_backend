# -*- coding: utf8 -*-
import redis
import requests
import json
import time

REDIS_CLIENT = redis.StrictRedis(host='localhost', port=6379, db=1)


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


def listen():
    ps = REDIS_CLIENT.pubsub()
    ps.subscribe(['token'])
    for item in ps.listen():
        if item['type'] == 'message':
            params = item['data']
            try:
                print('item data is {0}'.format(params))
                params = json.loads(params.decode('utf8').replace('\'', '\"'))
                token_info = get_access_token(
                    params['url'],
                    params['username'],
                    params['password'],
                    params['client_id'],
                    params['client_secret']
                )
                print('username access_token is {0}'.format(token_info))
            except Exception:
                pass


if __name__ == '__main__':
    print('redis pubsub listening...')
    listen()
