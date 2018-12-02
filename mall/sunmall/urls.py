from django.conf.urls import url

from sunmall.views import *

urlpatterns = [
    url(r'^message/$', message, name='message'),  # 动态
]