#coding=utf8
import sys
import json
import urllib
import requests
import uuid
import pypinyin
import imp
import datetime
import random
import traceback
import logging
from django.contrib.auth.models import User
from django.conf import settings
from django.db import connections, transaction
from django.utils.translation import ugettext_lazy as _

imp.reload(sys)

log = logging.getLogger(__name__)

accessKey = ''
appSecret = ''
ACCESS_TOKEN_URL = 'https://oapi.dingtalk.com/gettoken'
USER_DEPARTMENT_LISTIDS_URL = 'https://oapi.dingtalk.com/department/list_ids'
USER_LIST_IDS_LIST_URL = 'https://oapi.dingtalk.com/user/getDeptMember'
USER_DETAIL_URL = 'https://oapi.dingtalk.com/user/get'
USER_ID_BY_UNIONID_URL = 'https://oapi.dingtalk.com/user/getUseridByUnionid'
AUTO_LOGIN_USER_INFO_URL = "https://oapi.dingtalk.com/user/getuserinfo"

error_msg_no_email_info = _('No email information')
error_msg_user_existed_in_database = _('User existed in databases')
error_msg_email_existed_in_database = _("Email existed in database")
error_msg_fail_to_get_the_number_of_users = _('Failed to get the number of users')
error_msg_fail_to_get_user_list = _('Failed to get user list')
success_msg_sychornous_user_successful = _('Synchronous user successful')
success_msg_user_created_successful = _('User created successfuly')

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
        self._department_ids_list = [1]
        self._user_id_list = []
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
        self.user_id_by_unionid_url_param = {
            'access_token': self._token,
            'unionid': ''
        }
        self.user_department_listids_url_param = {
            'access_token': self._token,
            'id': 1
        }
        self.user_list_ids_param = {
            'access_token': self._token,
            'deptId': 1
        }
        self.user_detail_url_param = {
            'access_token': self._token,
            'userid': ''
        }
        self.auto_login_user_info_param = {
            'access_token': self._token,
            'code': ''
        }
        self._unsuccess_insert_list = []
        self._success_insert_list = []
        
    def get_all_department_id(self, parent_id=1):
        if not self._token:
            return None

        self.user_department_listids_url_param['id'] = parent_id
        param = self.deal_url_encode(self.user_department_listids_url_param)
        user_department_listids_url = USER_DEPARTMENT_LISTIDS_URL + "?" + param
        res = self.get_request_data(user_department_listids_url)
        if res:
            self._department_ids_list += res['sub_dept_id_list']
            for i in res['sub_dept_id_list']:
                self.get_all_department_id(i)
            return True
        else:
            return False
        
    def _get_department_user_list(self, department_id=1):
        if not self._token:
            return None
        
        self.user_list_ids_param['deptId'] = department_id
        param = self.deal_url_encode(self.user_list_ids_param)
        user_list_ids_list_url= USER_LIST_IDS_LIST_URL + "?" + param
        res = self.get_request_data(user_list_ids_list_url)
        if res:
            return res['userIds']
        else:
            return False
    
    def get_all_user_data(self):
        self.get_all_department_id(1)
        for i in self._department_ids_list:
            self._user_id_list += self._get_department_user_list(i)
        
        self._user_id_list = list(set(self._user_id_list))
        for userid in self._user_id_list:
            data = self._get_user_detail_data(userid)
            if data:
                if ('email' not in data or data['email'] == '') and ('orgEmail' not in data or data['orgEmail'] == ""):
                    user_detail = {
                        'name': data['name'],
                        'msg': error_msg_no_email_info
                    }
                    self._unsuccess_insert_list.append(user_detail)
                    continue
                    
                data = self._clean_data(data)
                self._create_user_to_database(data, 'dingtalk')

        result = {
            'status': 10001,
            'msg': success_msg_sychornous_user_successful,
            'result': {
                'success_user_info': self._success_insert_list,
                'fail_user_info': self._unsuccess_insert_list
            }
        }
        return result
    
    def _get_user_detail_data(self, userid):
        if not self._token:
            return None
        
        self.user_detail_url_param['userid'] = userid
        param = self.deal_url_encode(self.user_detail_url_param)
        user_detail_url = USER_DETAIL_URL + '?' + param
        res = self.get_request_data(user_detail_url)
        if res:
            return res
        else:
            return False

    def _get_access_token(self):
        data = self.deal_url_encode(self.access_token_url_param)
        access_token_url = ACCESS_TOKEN_URL + "?" + data
        res = self.get_request_data(access_token_url)
        if isinstance(res, dict)  and 'access_token' in res:
            return res['access_token']
        
        log.error('dingtalk access token get error, dingtalk server msg: ' + str(res))
        return None

    def deal_url_encode(self, param):
        return urllib.urlencode(param)
    
    def get_unionid_from_code(self, code):
        self.auto_login_user_info_param['code'] = code
        data = self.deal_url_encode(self.auto_login_user_info_param)
        auto_login_url = AUTO_LOGIN_USER_INFO_URL + "?" + data
        res = self.get_request_data(auto_login_url)
        if res and 'userid' in res:
            userid = res['userid']
        else:
            return None
        
        res = self._get_user_detail_data(userid)
        if res  and 'unionid' in res:
            unionid = res['unionid']
            return unionid
        else:
            return None

    def get_request_data(self, url):
        try:
            res = requests.request('get', url)
            res = json.loads(res.content)
            log.info({'url': url, 'type': 'get', 'result': str(res)})
            if 'errcode' in res:
                if res['errcode'] == 0:
                    return res
                else:
                    log.error({'errmsg': res['errmsg'], 'url': url})
        except Exception:
            log.error(traceback.format_exc())

        return None

    def _clean_data(self, data):
        new_data = {}
        new_data['unionid'] = data['unionid']
        if 'orgEmail' in data and data['orgEmail'] != '':
            new_data['email'] = data['orgEmail']
        else:
            new_data['email'] = data['email']
        new_data['real_name'] = data['name']
        s = ''
        for i in pypinyin.pinyin(data['name'], style=pypinyin.NORMAL):
            s += ''.join(i)
        new_data['name'] = s

        return new_data

    def _create_user_to_database(self, data, type):
        cursor = self._db_cursor()
        try:
            with transaction.atomic():
                now_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                if type == 'dingtalk':
                    sql = """
                        select * from social_auth_usersocialauth where uid='{uid}'
                    """.format(uid=data['unionid'])
                    cursor.execute(sql)
                    result = dictfetchall(cursor)
                    if result:
                        user_detail = {
                            'name': data['real_name'],
                            'msg': error_msg_user_existed_in_database
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
                    select * from auth_user where email='{email}'
                """.format(email=data['email'])
                cursor.execute(sql)
                result = dictfetchall(cursor)
                if result:
                    user_detail = {
                        'name': data['real_name'],
                        'msg': error_msg_email_existed_in_database
                    }
                    self._unsuccess_insert_list.append(user_detail)
                    return True

                sql = """
                    insert into auth_user(password, last_login, is_superuser, username, email, is_staff, is_active, date_joined, first_name, last_name) values \
                    ('pbkdf2_sha256$36000$5MWWT8MF6gMs$AJlC7Ff/0Dkg5rCw5Mnom/6BQjqAf8kPen836uvyGtg=','{last_login}',0,'{name}','{email}',0,1,'{date_joined}', '', '');
                """.format(last_login=now_time, name=data['name'], email=data['email'], date_joined=now_time)
                cursor.execute(sql)
                user_id = cursor.lastrowid

                activation_key = uuid.uuid4().hex
                sql = """
                    insert into auth_registration(activation_key, user_id) values('{activation_key}', {user_id});
                """.format(activation_key=activation_key, user_id=user_id)
                cursor.execute(sql)

                sql = """
                    insert into auth_userprofile(name,courseware,gender,level_of_education, mailing_address, city, country, goals, allow_certificate, user_id, meta, language, location) values \
                    ('{name}', 'course.xml', '', '', '', '', '', '', 1, {user_id}, '', '', '');
                """.format(name=data['real_name'], user_id=user_id)
                cursor.execute(sql)
                
                if type == 'dingtalk':
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
                    'msg': success_msg_user_created_successful
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
    
    def import_user_from_file_data(self, data):
        for i in data:
            self._create_user_to_database(i, 'csvfile')

        result = {
            'status': 10001,
            'msg': success_msg_sychornous_user_successful,
            'result': {
                'success_user_info': self._success_insert_list,
                'fail_user_info': self._unsuccess_insert_list
            }
        }
        return result
    
    def delete_leave_job_people(self):
        '''
        删除离职用户
        '''
        cursor = self._db_cursor()
        try:
            with transaction.atomic():
                sql = """
                    select sau.uid, sau.user_id, au.username, au.email, aup.name from \
                    social_auth_usersocialauth as sau left join auth_user as au on au.id=sau.user_id \
                    left join auth_userprofile as aup on sau.user_id=aup.user_id
                """
                cursor.execute(sql)
                result = dictfetchall(cursor)
                if not result or len(result) == 0:
                    return None
                
                delete_people_list = []
                for user_info in result:
                    user_id = user_info['user_id']
                    unionid = user_info['uid']
                    
                    self.user_id_by_unionid_url_param['unionid'] = unionid
                    user_id_by_unionid_url = USER_ID_BY_UNIONID_URL + '?' + self.deal_url_encode(self.user_id_by_unionid_url_param)
                    res = self.get_request_data(user_id_by_unionid_url)
                    if not res:
                        sql = """
                            delete from social_auth_usersocialauth where user_id={user_id}
                        """.format(user_id=user_id)
                        cursor.execute(sql)
                        User.objects.filter(id=user_id).delete()
                        
                        delete_people = {
                            'username': user_info['username'],
                            'email': user_info['email'],
                            'real_name': user_info['name']
                        }
                        delete_people_list.append(delete_people)
                
                return delete_people_list
        except Exception:
            log.error(traceback.format_exc())
        
        return None
    
    def import_user_from_data(self, path):
        
        return
        
