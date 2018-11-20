from django.conf.urls import url

from myuser.views import *

urlpatterns = [
    url(r'^member/$', member, name='member'),  # 我的
    url(r'^step/$', step, name='step'),  # 我的-设置
    url(r'^login/$', login, name='login'),  # 登录
    url(r'^reg/$', reg, name='reg'),  # 注册
    url(r'^records/$', records, name='records'),  # 账户余额
    url(r'^integral/$', integral, name='integral'),  # 积分
    url(r'^yhq/$', yhq, name='yhq'),  # 优惠券
    url(r'^collect/$', collect, name='collect'),  # 我的收藏
    url(r'^infor/$', infor, name='infor'),  # 个人资料
    url(r'^gladdress/$', gladdress, name='gladdress'),  # 收货地址
    url(r'^saftystep/$', saftystep, name='saftystep'),  # 安全设置
    url(r'^money/$', money, name='money'),  # 我的钱包
    url(r'^job/$', job, name='job'),  # 兼职
    url(r'^recommend/$', recommend, name='recommend'),  # 推荐有奖
    url(r'^myrecommend/$', myrecommend, name='myrecommend'),  # 我的推荐
]