from django.conf.urls import url

from cart.views import *

urlpatterns = [
    url(r'^$', cart, name='cart'),  # 购物车
    url(r'^shopcart/$', shopcart, name='shopcart'),  # 购物车的方法
]