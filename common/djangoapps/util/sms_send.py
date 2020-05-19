# -*- coding=utf8 -*-
import json
import requests
import logging

SEND_URL = "http://api.feige.ee/SmsService/Template"

logger = logging.getLogger(__name__)

class SmsSend(object):
    
    def __init__(self, user, pwd, content, templateid, signid):
        self._user = user
        self._pwd = pwd
        self._content = content
        self._templateid = templateid
        self._signid = signid
        
    def send_sign_code(self, phonenumber, code):
        self._content = self._content.replace('@', str(code))
        request_body = {}
        request_body['Account'] = self._user
        request_body['Pwd'] = self._pwd
        request_body['Content'] = self._content
        request_body['Mobile'] = phonenumber
        request_body['TemplateId'] = self._templateid
        request_body['SignId'] = self._signid
        
        res = requests.post(SEND_URL, data=request_body)
        logging.info(res.content)
        res_content = json.loads(res.content)
        
        if res_content['Message'] == 'OK':
            return True
        else:
            return False

