import time
import base64
import hmac
import json
import urllib
from hashlib import sha256
from social_core.backends.oauth import BaseOAuth2

class DingtalkOAuth2(BaseOAuth2):
    name = "DingTalk"
    AUTHORIZATION_URL = 'https://oapi.dingtalk.com/connect/qrconnect'
    ACCESS_TOKEN_URL = ''

    def auth_params(self, *args, **kwargs):
        params = super(DingtalkOAuth2, self).auth_params(*args, **kwargs)
        params['appid'] = params.pop('client_id')
        params['scope'] = 'snsapi_login'
        return params

    def request_access_token(self, *args, **kwargs):
        return {'access_token': self.data.get('code', '')}

    def user_data(self, access_token, *args, **kwargs):
        appid, appsecret = self.get_key_and_secret()
        now_timestamp = int(round(time.time() * 1000))
        signature = base64.b64encode(hmac.new(str(appsecret), str(now_timestamp), digestmod=sha256).digest())
        user_info_params_dict = {}
        user_info_params_dict['accessKey'] = appid
        user_info_params_dict['timestamp'] = now_timestamp
        user_info_params_dict['signature'] = signature
        user_info_params = urllib.urlencode(user_info_params_dict)
        userinfo_url = 'https://oapi.dingtalk.com/sns/getuserinfo_bycode?{params}'.format(params=user_info_params)
        params = json.dumps({'tmp_auth_code': str(access_token)})
        headers = {'Content-Type': 'application/json'}
        return self.get_json(userinfo_url, method='post', headers=headers, verify=False, data=params)

    def get_user_details(self, response):
        info = response.get('user_info')
        return {
            "username": info['nick'].encode('utf-8')
        }

    def get_user_id(self, details, response):
        return response.get('user_info').get('unionid')
