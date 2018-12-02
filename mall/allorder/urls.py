from django.conf.urls import url

from allorder.views import *

urlpatterns = [
    url(r'^allorder/$', allorder, name='allorder'),  # 订单
    url(r'^tureorder/$', tureorder, name='tureorder'),  # 确认订单
    url(r'^showorder/$', showorder, name='showorder'),  # 支付订单
    url(r'^pay/$', pay, name='pay'),  # 支付完成
    url(r'^success/$', success, name='success'),  # 支付结果
]