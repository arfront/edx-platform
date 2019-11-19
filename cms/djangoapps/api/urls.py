from django.conf.urls import include, url
from cms.djangoapps.api.v1.views.kh_user_manage import GetuserfromDingTalkView, RemoveleavejobuserView

urlpatterns = [
    url(r'^v1/', include('cms.djangoapps.api.v1.urls', namespace='v1')),
    url(r'^v1/kh_insert_dingtalk_user/', GetuserfromDingTalkView.as_view()),
    url(r'^v1/kh_remove_leave_job_user/', RemoveleavejobuserView.as_view()),
]
