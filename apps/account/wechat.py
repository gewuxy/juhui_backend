# -*- coding: utf8 -*-
from weixin.client import WeixinAPI
# from config.settings.common import APP_ID, APP_SECRET

APP_ID = 'wx53502d888764b329'
APP_SECRET = '018d5c10649a2eae7356013549f9fab1'
REDIRECT_URI = 'https://jh.qiuxiaokun.com'
CODE = 'E6E6E5'


def login():
    # scope = ("snsapi_login", )
    api = WeixinAPI(appid=APP_ID,
                    app_secret=APP_SECRET,
                    redirect_uri=REDIRECT_URI)
    # authorize_url = api.get_authorize_url(scope=scope)
    auth_info = api.exchange_code_for_access_token(code=CODE)
    api = WeixinAPI(access_token=auth_info['access_token'])
    user = api.user(openid=auth_info["openid"])
    return user


if __name__ == '__main__':
    print(login())
