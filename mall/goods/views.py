from django.shortcuts import render, redirect

# 主页
from goods.models import Sku, Banner, Activity, ActivityArea, Shop
from django_redis import get_redis_connection


def index(request):
    # 首页轮播
    banner = Banner.objects.filter(banner_is_delete=False).order_by('banner_order')
    # 活动专区
    act = Activity.objects.filter(Activity_is_delete=False)
    # 活动商品专区
    area = ActivityArea.objects.filter(activityshop__ActivityShop_sku_id__sku_is_upper=True, ActivityArea_is_delete=False).order_by('-ActivityArea_order')
    context = {
        'banner': banner,
        'act': act,
        'area': area,
    }
    return render(request, 'index/index.html', context)


# 超市
def category(request, cate_id, order):
    try:
        cate_id = int(cate_id)
        order = int(order)
    except:
        redirect('index:index')
    # 显示分类所有
    shop = Shop.objects.filter(shop_is_delete=False)
    # 查询某个分类下的所有商品
    if cate_id == 0:
        cate = shop.first()
        cate_id = cate.pk
    # 所有商品
    sku = Sku.objects.filter(sku_is_delete=False, sku_is_upper=True, sku_shop_id_id=cate_id)
    # 定义一个列表完成对综合,销量,价格,新品进行排序
    order_rule = ['id', '-sku_Sales_volume', '-sku_price', 'sku_price', '-sku_add_time']
    try:
        sku_order = order_rule[order]
    except:
        sku_order = order_rule[0]
        order = 0
    sku = sku.order_by(sku_order)

    # 完成商品的显示在购物车上, 没有登陆显示0
    cart_count = 0
    # 登陆就显示有多少个商品
    if request.session.get('ID'):
        user_id = request.session.get('ID')
        # 获取连接
        cnn = get_redis_connection('default')
        # 获取键
        cart_key = 'cart_user_{}'.format(user_id)
        # 取值
        cart_values = cnn.hvals(cart_key)
        # 遍历值对象,转型
        for v in cart_values:
            cart_count += int(v)

    context = {
        'shop': shop,
        'sku': sku,
        'cate_id': cate_id,
        'order': order,
        'cart_count': cart_count
    }
    return render(request, 'index/category.html', context)


def detail(request, id):
    # 详情页
    sku = Sku.objects.get(pk=id)
    context = {
        'sku': sku
    }
    return render(request, 'index/detail.html', context)