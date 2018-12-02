from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection

from goods.models import Sku


def shopcart(request):  # 购物车
    """
                1. 前端通过ajax post请求方式 将 sku_id (sku商品id)和 count(商品的数量)
                3. 验证是否登陆，如果没登陆，告诉ajax中的js代码实现跳转到登陆页面 location.href=url
                4. 验证数据的合法性，必须都为整数
                5. 验证商品是否存在
                6. 验证库存是否足够
                2. 保存到redis
                    配置是正确
                    使用 hash对象 保存
                    hset key 属性 值
                    hset cart_user_id 商品id 数量
            :return:
    """
    # 获取post数据
    sku_id = request.POST.get('sku_id')
    count = request.POST.get('count')
    # 验证是否登录
    # 从session获取用户信息判断是否登录
    id = request.session.get('ID')
    if id is None:
        return JsonResponse({'code': 1, 'err': '请登录'})
    # 验证数据必须为整数
    try:
        sku_id = int(sku_id)
        count = int(count)
    except Exception:
        return JsonResponse({'code': 2, 'err': '参数错误'})
    # 验证商品是否存在
    try:
        sku = Sku.objects.get(pk=sku_id)
    except Sku.DoesNotExist:
        return JsonResponse({'code': 3, 'err': '商品不存在'})
    # 验证库存是否足够
    if sku.sku_stock < count:
        return JsonResponse({'code': 4, 'err': '库存不足'})
    # 保存在Redis中
    # 使用hash来保存
    # 获取用户id
    user_id = request.session.get('ID')
    # 获取Redis连接
    cnn = get_redis_connection('default')
    # 传一个变量来保存数据库的id,使保存的id不被覆盖
    cart_key = 'cart_user_{}'.format(user_id)
    # 保存在数据库中
    sku_id_count = cnn.hincrby(cart_key, sku_id, count,)
    # 判断当前的sku_id的值是否等于0,是就删除sku_id对应的键
    if sku_id_count == 0:
        cnn.hdel(cart_key, sku_id)
    # 保存成功
    cart_count = 0
    # 取值
    cart_values = cnn.hvals(cart_key)
    # 遍历值对象,转型
    for v in cart_values:
        cart_count += int(v)
    return JsonResponse({'code': 0, 'err': '保存成功', 'cart_count': cart_count})


def cart(request):
    # 连接Redis
    cnn = get_redis_connection('default')
    # 获取id
    user_id = request.session.get('ID')
    # 获取对象
    cart_key = 'cart_user_{}'.format(user_id)
    # 得到的值为字典,都带有编码的键和值
    cart_data = cnn.hgetall(cart_key)
    # 获取Redis的键和值
    # 自定义一个列表
    goods = []
    for sku_id, count in cart_data.items():
        sku_id = int(sku_id)
        count = int(count)
        # 查询商品的信息
        sku = Sku.objects.get(pk=sku_id)
        # 自定义变量保存在商品中
        sku.count = count
        # 将数据保存在列表中
        goods.append(sku)
    context = {
        'goods': goods
    }
    return render(request, 'index/shopcart.html', context)
