from django.conf.urls import url

from sunmall.views import *

urlpatterns = [
    url(r'^index/$', index, name='index'),  # 主页
    url(r'^message/$', message, name='message'),  # 动态
    url(r'^shopcart/$', shopcart, name='shopcart'),  # 购物车
    url(r'^allorder/$', allorder, name='allorder'),  # 订单
]