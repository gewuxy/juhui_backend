# -*- coding: utf8 -*-
import requests


def create_buy_comm():
    url = 'https://jh.qiuxiaokun.com/api/account/createcommission0/'
    r = requests.get(url)
    print(r.content)


def create_sell_comm():
    url = 'https://jh.qiuxiaokun.com/api/account/createcommission1/'
    r = requests.get(url)
    print(r.content)


if __name__ == '__main__':
    create_buy_comm()
    create_sell_comm()