from django.shortcuts import render


def index(request):  # 主页
    return render(request, 'index/index.html')


def message(request):  # 动态
    return render(request, 'index/message.html')


def shopcart(request):  # 购物车
    return render(request, 'index/shopcart.html')


def allorder(request):  # 订单
    return render(request, 'index/allorder.html')