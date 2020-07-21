import time
import urllib
import rsa
import base64
from django.utils.translation import ugettext_lazy as _
from rest_framework import views, response, status, permissions
from arfrontconfig.models import Youtubeaccountconfig

rsa_public_key_file_path = "/openedx/edx-platform/"
rsa_public_key_file_name = 'rsapublickey.pem'

success_msg_get_arfront_youtube_account_info_success = _('Successfully get arfront youtube account info')
error_msg_no_config_of_youtube_account = _('No config of arfront youtube account')


class YoutubeAccountView(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]
    
    def get(self, request):
        config = Youtubeaccountconfig.current()
        if config.enabled:
            username = config.username
            password = config.password
            streamersite = config.streamersite
            target_url = config.target_url
        else:
            return response.Response({'status': 10002, 'msg': error_msg_no_config_of_youtube_account}, status=status.HTTP_200_OK)
        
        if username == "" or password == "" or streamersite == "":
            return response.Response({'status': 10002, 'msg': error_msg_no_config_of_youtube_account}, status=status.HTTP_200_OK)
        
        last_time = int(time.time())
        data_str = "user={user}&pass={password}&siteURL={streamersite}&timestamp={timestamp}".\
            format(user=username, password=password, streamersite=streamersite, timestamp=last_time)
        
        with open(rsa_public_key_file_path + rsa_public_key_file_name, 'r') as f:
            public_key = f.read()

        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(public_key.encode('utf8'))
        crypto = rsa.encrypt(data_str.encode('utf8'), pub_key=pubkey)  # 使用PKCS加密给定的消息,返回类型bytes
        secret_msg = base64.b64encode(crypto).decode('utf8')  # 加密后的文本信息
        param_data = {
            'user': username,
            'secret': secret_msg,
            'timestamp': last_time
        }
        param_res = urllib.urlencode(param_data)
        target_url = target_url + "?" + param_res
        param_data['target_url'] = target_url
        return response.Response({'data':param_data, 'status': 10001, 'msg': success_msg_get_arfront_youtube_account_info_success}, status=status.HTTP_200_OK)
