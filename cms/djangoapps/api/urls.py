"""
URLs for the Studio API app
"""


from django.conf.urls import include, url
from cms.djangoapps.api.v1.views.kh_user_manage import GetuserfromDingTalkView, RemoveleavejobuserView, ImportUserfromfileView, WeiHouaccountView, GetfullnamefromusernameView
from cms.djangoapps.api.v1.views.youtube_account import YoutubeAccountView

app_name = 'cms.djangoapps.api'

urlpatterns = [
    url(r'^v1/', include('cms.djangoapps.api.v1.urls', namespace='v1')),
    url(r'^v1/kh_insert_dingtalk_user/', GetuserfromDingTalkView.as_view()),
    url(r'^v1/kh_remove_leave_job_user/', RemoveleavejobuserView.as_view()),
    url(r'^v1/youtube_account_info/', YoutubeAccountView.as_view()),
    url(r'^v1/importuserfromfile/', ImportUserfromfileView.as_view()),
    url(r'^v1/weihouaccount/', WeiHouaccountView.as_view()),
    url(r'^v1/getfullnamefromusername/', GetfullnamefromusernameView.as_view()),
]
