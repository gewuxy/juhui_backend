# -*- coding: utf8 -*-
import requests
import json
import time


def test_register():
    mobile = str(time.time())[:11]
    print(mobile)
    # return
    password = '123456'
    code = '1234'
    data = {'mobile': mobile, 'password': password, 'code': code}
    url = 'http://127.0.0.1:9991/apis/account/register/'
    r = requests.post(url=url, data=json.dumps(data))
    print(r)
    print(r.text)


def test_login():
    mobile = '15913152794'
    print(mobile)
    # return
    password = '123456'
    code = '1234'
    data = {'mobile': mobile, 'password': password, 'code': code}
    url = 'http://127.0.0.1:9991/apis/account/login/'
    r = requests.post(url=url, data=json.dumps(data))
    print(r)
    print(r.text)


if __name__ == '__main__':
    test_login()
