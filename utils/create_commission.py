# -*- coding: utf8 -*-
import requests
import datetime


def create_buy_comm():
    url = 'https://jh.qiuxiaokun.com/api/account/createcommission0/'
    r = requests.get(url)
    print('create buy commission: {0}'.format(r.content))


def create_sell_comm():
    url = 'https://jh.qiuxiaokun.com/api/account/createcommission1/'
    r = requests.get(url)
    print('create sell commission: {0}'.format(r.content))


if __name__ == '__main__':
    print(datetime.datetime.now())
    create_buy_comm()
    create_sell_comm()
