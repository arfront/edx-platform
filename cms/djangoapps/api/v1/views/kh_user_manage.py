#coding=utf8
import logging
from django.utils.translation import ugettext_lazy as _
from rest_framework import views, response, status, permissions
from util.dintalkcompany import Dingtalkuserinfo
from dingtalkuser.models import DingtalkUserconfig

log = logging.getLogger(__name__)

error_msg_no_config_of_dingtalk_can_be_used = _('No config of dingtalk can be used')
error_msg_no_secret_or_key_in_config = _('No secret or key in config')
success_msg_successfully_deleted_user = _('Successfully deleted users')
success_msg_no_users_to_delete = _('No users to delete')

class GetuserfromDingTalkView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        config = DingtalkUserconfig.current()
        if config.enabled:
            accessKey = config.get_setting('KEY')
            appSecret = config.get_setting('SECRET')
        else:
            return response.Response({'msg': error_msg_no_config_of_dingtalk_can_be_used}, status=status.HTTP_403_FORBIDDEN)

        if accessKey == '' or appSecret == '':
            return response.Response({'msg': error_msg_no_secret_or_key_in_config}, status=status.HTTP_403_FORBIDDEN)
        dingtalk_user_info = Dingtalkuserinfo(accessKey, appSecret)
        res = dingtalk_user_info.get_all_user_data()
        return response.Response(res)


class RemoveleavejobuserView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request):
        config = DingtalkUserconfig.current()
        if config.enabled:
            accessKey = config.get_setting('KEY')
            appSecret = config.get_setting('SECRET')
        else:
            return response.Response({'msg': error_msg_no_config_of_dingtalk_can_be_used}, status=status.HTTP_403_FORBIDDEN)
        
        if accessKey == '' or appSecret == '':
            return response.Response({'msg': error_msg_no_secret_or_key_in_config}, status=status.HTTP_403_FORBIDDEN)

        dingtalk_user_info = Dingtalkuserinfo(accessKey, appSecret)
        res = dingtalk_user_info.delete_leave_job_people()
        if res:
            return response.Response({'msg': success_msg_successfully_deleted_user, 'detail': res}, status=status.HTTP_200_OK)
        else:
            return response.Response({'msg': success_msg_no_users_to_delete, 'deatil': []}, status=status.HTTP_200_OK)
        
