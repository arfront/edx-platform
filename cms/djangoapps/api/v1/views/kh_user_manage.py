#coding=utf8
import logging
import csv
from django.utils.translation import ugettext_lazy as _
from rest_framework import views, response, status, permissions
from util.dintalkcompany import Dingtalkuserinfo
from dingtalkuser.models import DingtalkUserconfig

log = logging.getLogger(__name__)

error_msg_no_config_of_dingtalk_can_be_used = _('No config of dingtalk can be used')
error_msg_no_secret_or_key_in_config = _('No secret or key in config')
success_msg_successfully_deleted_user = _('Successfully deleted users')
success_msg_no_users_to_delete = _('No users to delete')
success_msg_import_user = _('Success Import user')

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
        

class ImportUserfromfileView(views.APIView):
    permission_classes = (permissions.IsAdminUser,)
    
    def post(self, request):
        print(request.FILES)
        file_obj = request.FILES['file']
        temp_file = '/openedx/data/temp.csv'
        
        with open(temp_file, 'w+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        
        data_list = []
        with open(temp_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            for i, rows in enumerate(reader):
                if i == 0:
                    continue
                line_list = rows[0].split('\t')
                data = {}
                data['name'] = line_list[0].replace(' ', '')
                data['email'] = line_list[1].replace(' ', '')
                data['real_name'] = line_list[2].replace(' ', '')
                data_list.append(data)

        user_info = Dingtalkuserinfo('', '')
        res = user_info.import_user_from_file_data(data_list)
        
        return response.Response(res, status=status.HTTP_200_OK)
