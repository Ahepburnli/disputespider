import requests
import time
import schedule
import base64
import json
import logging
from pymysql import *
import datetime




def get_access_token():
    '''
    return access_token
    通过账号密码得到access_token
    access_token有过期时间,所以要每次先获取access_token再请求账单和纠纷信息

    每天获取access_token的次数有限

    '''
    client_id = "ARNu3TILlA-NqpqSuN2KSzUordeuNDK3d1NR8gx1zOMGJXeW3NdwT0o_Scovltku-nBFt_KJjsNGZ6ED"
    client_secret = "EDg5KBlTD5igpK_ecP1P7TjLh9q6ZUlO1sFEs9AUZXO0tYSepLBB_kdJSmCXz0izD3mJkHwTpdLXr21k"

    credentials = "%s:%s" % (client_id, client_secret)
    encode_credential = base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")

    headers = {
        "Authorization": ("Basic %s" % encode_credential),
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'Connection': 'close'
    }

    param = {
        'grant_type': 'client_credentials',
    }

    url = 'https://api.paypal.com/v1/oauth2/token'
    # requests.adapters.DEFAULT_RETRIES = 5
    requests.packages.urllib3.disable_warnings()  # 防止出现warning信息
    response = requests.post(url, headers=headers, data=param, verify=False)

    text = response.content.decode()
    text = json.loads(text)
    access_token = text['access_token']
    # logging.debug('成功获取access_token')
    print('成功获取access_token')

    return access_token






