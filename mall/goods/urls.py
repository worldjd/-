from django.conf.urls import url

from goods.views import *

urlpatterns = [
    url(r'^index/$', index, name='index'),  # 主页
    url(r'^category/(?P<cate_id>\d+)/(?P<order>\d)/$', category, name='category'),  # 超市
    url(r'^detail/(?P<id>\d+)/$', detail, name='detail'),  # 详情
]