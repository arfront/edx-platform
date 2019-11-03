#coding=utf8
import sys
import os
import json
import urllib
import requests
import uuid
import pypinyin
import datetime
import random
import traceback
import logging
from django.conf import settings
from django.db import connections, transaction
from dingtalkuser.models import DingtalkUserconfig
from django.utils.translation import ugettext_lazy as _
from rest_framework import views, response, status, permissions

log = logging.getLogger(__name__)

reload(sys)
sys.setdefaultencoding("utf8")

accessKey = ''
appSecret = ''
ACCESS_TOKEN_URL = 'https://oapi.dingtalk.com/gettoken'
USER_AMOUNT_URL = 'https://oapi.dingtalk.com/user/get_org_user_count'
USER_LIST_URL = 'https://oapi.dingtalk.com/user/listbypage'
user_data_file_path = '/openedx/data/dingtalk_company_user_data/'

error_msg1 = _('No config of dingtalk can be used')
error_msg2 = _('No secret or key in config')
error_msg3 = _('No email information')
error_msg4 = _('User existed in databases')
error_msg5 = _('Failed to get the number of users')
error_msg6 = _('Failed to get user list')
success_msg1 = _('Synchronous user successful')
success_msg2 = _('User created successfuly')

class GetuserfromDingTalkView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        config = DingtalkUserconfig.current()
        if config.enabled:
            accessKey = config.get_setting('KEY')
            appSecret = config.get_setting('SECRET')
        else:
            return response.Response({'msg': error_msg1}, status=status.HTTP_403_FORBIDDEN)

        if accessKey == '' or appSecret == '':
            return response.Response({'msg': error_msg2}, status=status.HTTP_403_FORBIDDEN)
        dingtalk_user_info = Dingtalkuserinfo(accessKey, appSecret)
        res = dingtalk_user_info.main()
        return response.Response(res)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class Dingtalkuserinfo:

    def __init__(self, accessKey, appSecret):
        self.user_count = 0
        self.access_token_url_param = {
            'appkey': accessKey,
            'appsecret': appSecret
        }
        self._token = self._get_access_token()
        self.user_amount_url_param = {
            'access_token': self._token,
            'onlyActive': 1
        }
        self.user_list_url_param = {
            'access_token': self._token,
            'department_id': 1,
            'offset': 0,
            'size': 100
        }
        self._unsuccess_insert_list = []
        self._success_insert_list = []

    def _get_user_amount(self):
        if not self._token:
            return None

        data = self.deal_url_encode(self.user_amount_url_param)
        user_amount_url = USER_AMOUNT_URL + '?' + data
        res = self.get_request_data(user_amount_url)
        if res:
            self.user_count = res['count']
            return True
        else:
            return False

    def _get_user_list(self):
        if not self._token:
            return None

        if self.user_count == 0:
            return []

        offset = int(self.user_count / 100)
        user_data = []
        for i in range(offset + 1):
            self.user_list_url_param['offset'] = i
            data = self.deal_url_encode(self.user_list_url_param)
            user_list_url = USER_LIST_URL + '?' + data
            res = self.get_request_data(user_list_url)
            if res:
                user_data += res['userlist']
        return user_data

    def _get_access_token(self):
        data = self.deal_url_encode(self.access_token_url_param)
        access_token_url = ACCESS_TOKEN_URL + "?" + data
        return self.get_request_data(access_token_url)['access_token']

    def deal_url_encode(self, param):
        return urllib.urlencode(param)

    def get_request_data(self, url):
        try:
            res = requests.request('get', url)
            res = json.loads(res.content)
            if 'errcode' in res:
                if res['errcode'] == 0:
                    return res
                else:
                    log.error({'errmsg': res['errmsg'], 'url': url})
        except Exception:
            log.error(traceback.format_exc())

        return None

    def _save_data_to_file(self, data):
        if not os.path.exists(user_data_file_path):
            os.makedirs(user_data_file_path)

        with open(user_data_file_path + 'data.json', 'w') as f:
            f.write(json.dumps(data))

    def _clean_data(self, data):
        new_data = {}
        new_data['unionid'] = data['unionid']
        new_data['email'] = data['email']
        new_data['real_name'] = data['name']
        s = ''
        for i in pypinyin.pinyin(data['name'], style=pypinyin.NORMAL):
            s += ''.join(i)
        new_data['name'] = s

        return new_data

    def _create_user_to_database(self, data):
        cursor = self._db_cursor()
        try:
            with transaction.atomic():
                now_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                sql = """
                    select * from social_auth_usersocialauth where uid='{uid}'
                """.format(uid=data['unionid'])
                cursor.execute(sql)
                result = dictfetchall(cursor)
                if result:
                    user_detail = {
                        'name': data['real_name'],
                        'msg': error_msg4
                    }
                    self._unsuccess_insert_list.append(user_detail)
                    return True

                sql = """
                    select * from auth_user where username='{username}'
                """.format(username=data['name'])
                cursor.execute(sql)
                result = dictfetchall(cursor)
                if result:
                    data['name'] = data['name'] + str(random.randint(0, 100))

                sql = """
                    insert into auth_user(password,last_login,is_superuser,username,email,is_staff,is_active,date_joined) values \
                    ('pbkdf2_sha256$36000$hGRbvCdc8t1e$QJcK3qNinTn7+WC0TFnrt+ovXSzywyzQhRouaYDMegA=','{last_login}',0,'{name}','{email}',0,1,'{date_joined}');
                """.format(last_login=now_time, name=data['name'], email=data['email'], date_joined=now_time)
                cursor.execute(sql)
                user_id = cursor.lastrowid

                activation_key = uuid.uuid4().hex
                sql = """
                    insert into auth_registration(activation_key, user_id) values('{activation_key}', {user_id});
                """.format(activation_key=activation_key, user_id=user_id)
                cursor.execute(sql)

                sql = """
                    insert into auth_userprofile(name,courseware,gender,level_of_education, mailing_address, city, country, goals, allow_certificate, user_id) values \
                    ('{name}', 'course.xml','','','','','','',1,{user_id});
                """.format(name=data['real_name'], user_id=user_id)
                cursor.execute(sql)

                sql = """
                    insert into social_auth_usersocialauth(provider, uid, extra_data, user_id) values('DingTalk','{uid}','', {user_id});
                """.format(uid=data['unionid'], user_id=user_id)
                cursor.execute(sql)

                sql = """
                    insert into user_api_userpreference(`key`,value,user_id) values('pref-lang','zh-cn', {user_id});
                """.format(user_id=user_id)
                cursor.execute(sql)

                user_detail = {
                    'name': data['real_name'],
                    'msg': success_msg2
                }
                self._success_insert_list.append(user_detail)

        except Exception:
            log.error(traceback.format_exc())
            return False

        return True

    def _db_cursor(self):
        db_alias = (
            'read_replica'
            if 'read_replica' in settings.DATABASES
            else 'default'
        )
        return connections[db_alias].cursor()

    def main(self):
        get_amount_result = self._get_user_amount()
        if not get_amount_result:
            return {
                'status': 10002,
                'msg': error_msg5,
            }
        data = self._get_user_list()
        if not data:
            return {
                'status': 10003,
                'msg': error_msg6
            }
        new_data = []
        for i in data:
            if 'email' not in i or i['email'] == '':
                user_detail = {
                    'name': i['name'],
                    'msg': error_msg3
                }
                self._unsuccess_insert_list.append(user_detail)
                continue

            single_data = self._clean_data(i)
            new_data.append(single_data)

        self._save_data_to_file(new_data)
        for data in new_data:
            self._create_user_to_database(data)

        result = {
            'status': 10001,
            'msg': success_msg1,
            'result': {
                'success_user_info': self._success_insert_list,
                'fail_user_info': self._unsuccess_insert_list
            }
        }

        return result
