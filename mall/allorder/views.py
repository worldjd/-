import time

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect

from allorder.models import Transport, Order, OrderGoods
from goods.models import Sku
from myuser.helper import verify_login_required
from myuser.models import Gladdress
from django_redis import get_redis_connection
from datetime import datetime
import random
from alipay import AliPay
import os
from django.conf import settings


@verify_login_required
def allorder(request):  # 订单
    return render(request, 'index/allorder.html')


# 确认订单
@transaction.atomic()
def tureorder(request):
    # 判断请求方式
    if request.method == 'GET':
        # 判断是否登录
        user_id = request.session.get('ID')
        if user_id is None:
            return redirect('user:login')
        # 获取收货地址
        glad = Gladdress.objects.filter(user_id=user_id).order_by('-isDefault').first()
        # 获取商品信息
        sku_ids = request.GET.getlist('sku_id')
        # sku_ids = [int(sku_id) for sku_id in sku_ids]
        # 连接对象
        cnn = get_redis_connection('default')
        # 创建键
        cart_key = 'cart_user_{}'.format(user_id)
        # 设置总价格
        price = 0
        # 查询商品信息
        sk = []
        for sku_id in sku_ids:
            try:
                sku_id = int(sku_id)
            except:
                return redirect('index:index')
            # 获取模型对象
            sku = Sku.objects.get(id=sku_id)
            # 获取数量
            count = cnn.hget(cart_key, sku_id)
            # 转换类型
            try:
                count = int(count)
            except:
                redirect('index:index')
            # 将变量添加到sku对象上
            sku.count = count
            # 获取价格
            price += sku.sku_price*count
            sk.append(sku)
        # 查询运输方式
        trans = Transport.objects.filter(isDelete=False).order_by('price')
        context = {
            'glad': glad,
            'sku': sk,
            'price': price,
            'trans': trans
        }
        return render(request, 'index/tureorder.html', context)
    if request.method == "POST":
        # 判断是否登录
        user_id = request.session.get('ID')
        if user_id is None:
            return JsonResponse({'code': 1, 'err': '请登录!'})
        # 接受参数
        address = request.POST.get('address_id')
        sku_ids = request.POST.getlist('sku_id')
        transport = request.POST.get('transport')
        if not all([address, sku_ids, transport]):
            return JsonResponse({'code': 2, 'err': '参数错误'})
        # 判断是否为整数
        try:
            address = int(address)
            sku_ids_int = [int(sku_id) for sku_id in sku_ids]
            transport = int(transport)
        except:
            return JsonResponse({'code': 3, 'err': '参数错误'})
        # 判断收货地址和运输方式必须存在
        try:
            address = Gladdress.objects.get(id=address, isDelete=False)
        except Gladdress.DoesNotExist:
            return JsonResponse({'code': 4, 'err': '收货地址不存在'})
        try:
            trans = Transport.objects.get(id=transport, isDelete=False)
        except Transport.DoesNotExist:
            return JsonResponse({'code': 5, 'err': '运输方式不存在'})
        # 准备订单编号
        order_number = '{}{}{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'),
                                       user_id,
                                       random.randint(10000, 99999)
                                       )
        # 准备详细地址
        address_detail = '{}{}{}{}'.format(address.hcity,
                                           address.hproper,
                                           address.harea,
                                           address.detail
                                           )
        # 保存数据到订单表中
        # 控制事务
        sid = transaction.savepoint()
        order = Order.objects.create(
            order_number=order_number,
            user_id=user_id,
            username=address.username,
            phone=address.phone,
            address=address_detail,
            transport=trans.name,
            transport_price=trans.price,
        )
        # 连接数据库Redis
        cnn = get_redis_connection('default')
        # 获取键
        # 保存商品的总价格
        order_amount = 0
        cart_user = 'cart_user_{}'.format(user_id)
        for sku_id in sku_ids_int:
            try:
                sku = Sku.objects.select_for_update().get(id=sku_id, sku_is_delete=False, sku_is_upper=True)
            except Sku.DoesNotExist:
                # 回滚
                transaction.savepoint_rollback(sid)
                return JsonResponse({'code': 6, 'err': '商品不存在'})
            # 获取数据库中的数量
            count = cnn.hget(cart_user, sku_id)
            count = int(count)
            # 保证库存足够
            if sku.sku_stock < count:
                # 回滚
                transaction.savepoint_rollback(sid)
                return JsonResponse({'code': 8, 'err': '库存不足'})
            # 保存商品表中
            # 实际付款金额
            price_money = sku.sku_price*count+order.transport_price
            OrderGoods.objects.create(
                order=order,
                goods_sku=sku,
                count=count,
                price=sku.sku_price,
                price_money=price_money,
            )
            # 销量增加
            sku.sku_Sales_volume += count
            # 库存减少
            sku.sku_stock -= count
            # 保存
            sku.save()
            # 统计总价格
            order_amount += sku.sku_price*count
        # 将总金额和实际付款金额保存在数据库中
        try:
            order.order_amount = order_amount
            order.order_money = order_amount+order.transport_price
            order.save()
        except:
            # 回滚
            transaction.savepoint_rollback(sid)
            return JsonResponse({'code': 7, 'err': '保存商品价格失败'})
        # 所有都成功, 删除提交的数据
        cnn.hdel(cart_user, *sku_ids_int)
        # 提交事务
        transaction.savepoint_commit(sid)
        # 成功后跳转至确认支付页面
        return JsonResponse({'code': 0, 'err': '申请订单成功', 'order_number': order_number})


# 支付订单
def showorder(request):
    if request.method == "GET":
        # 获取参数
        user_id = request.session.get('ID')
        order_number = request.GET.get('order_number')
        # 判断是否登录
        if user_id is None:
            return redirect('user:login')
        # 查询数据库,渲染页面
        order = Order.objects.get(user_id=user_id, order_number=order_number)
        context = {
            'order': order,
        }
        return render(request, 'index/showorder.html', context)


# 支付跳转
def pay(request):
    # 判断是否登录
    user_id = request.session.get('ID')
    if user_id is None:
        return redirect('user:login')
    # 获取请求中的order_number
    order_number = request.GET.get('order_number')
    # 查询数据库
    try:
        order = Order.objects.get(user_id=user_id, order_number=order_number, status=0)
    except Order.DoesNotExist:
        redirect('index:index')
    # 订单总金额
    total = order.transport_price+order.order_amount
    # 订单描述
    brief = '小超市'
    app_private_key_string = open(os.path.join(settings.BASE_DIR, 'allorder/private_key.txt')).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'allorder/public_key.txt')).read()
    # 创建对象
    alipay = AliPay(
        appid="2016092300576148",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    # 发起支付
    # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=order.order_number,  # 订单编号
        total_amount=str(total),
        subject=brief,
        return_url="http://127.0.0.1:8000/allorder/success/",
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    # 跳转支付
    return redirect("https://openapi.alipaydev.com/gateway.do?{}".format(order_string))


def success(request):
    # 验证登录
    user_id = request.session.get('ID')
    if user_id is None:
        return redirect('user:login')
    # 发起一次支付请求
    app_private_key_string = open(os.path.join(settings.BASE_DIR, 'allorder/private_key.txt')).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'allorder/public_key.txt')).read()
    # 创建对象
    alipay = AliPay(
        appid="2016092300576148",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    # 获取参数
    out_trade_no = request.GET.get('out_trade_no')
    paid = False
    for i in range(3):
        result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            paid = True
            break
        else:
            time.sleep(3)

    if paid is False:
        context = {
            "message": "支付失败"
        }
    else:
        # 支付成功
        # 修改状态
        Order.objects.filter(order_number=out_trade_no, user_id=user_id, status=0).update(status=1)

        # 渲染数据
        context = {
            "message": "支付成功"
        }

    # 支付成功之后返回的页面
    return render(request, 'index/pay.html', context)

