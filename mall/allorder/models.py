from django.db import models


class Transport(models.Model):
    name = models.CharField(max_length=50, verbose_name='运输名称')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='价格')
    add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'transport'
        verbose_name = '运输方式'
        verbose_name_plural = verbose_name


class Order(models.Model):
    order_status = (
        (0, '待付款'),
        (1, '待发货'),
        (2, '待评价'),
        (3, '取消订单'),
        (4, '申请退款'),
        (5, '已完成'),
        (6, '已评价'),
        (7, '已退款')
    )
    order_number = models.CharField(max_length=64, verbose_name='订单编号', unique=True)
    user = models.ForeignKey(to='myuser.User', verbose_name='用户ID')
    username = models.CharField(max_length=50, verbose_name='收货人')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    address = models.CharField(max_length=255, verbose_name='收货地址')
    status = models.SmallIntegerField(choices=order_status, default=0, verbose_name='订单状态')
    transport = models.CharField(max_length=50, verbose_name='运输方式')
    transport_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='运输价格')
    pay_method = models.ForeignKey(to='Paymethod', verbose_name='支付方式', null=True, blank=True)
    order_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='商品总金额')
    order_money = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='实际付款金额')
    add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.order_number

    class Meta:
        db_table = "order"
        verbose_name = '订单管理表'
        verbose_name_plural = verbose_name


class Paymethod(models.Model):
    name = models.CharField(max_length=50, verbose_name='支付方式')
    logo = models.ImageField(upload_to='logo/%Y', verbose_name='图片')
    add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'paymethod'
        verbose_name = '支付方式'
        verbose_name_plural = verbose_name


class OrderGoods(models.Model):
    order = models.ForeignKey(to='Order', verbose_name='订单ID')
    goods_sku = models.ForeignKey(to='goods.Sku', verbose_name='商品skuID')
    count = models.IntegerField(verbose_name='订单商品的数量')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='订单商品的价格')
    price_money = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='实际支付的总金额')
    add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.order.order_number

    class Meta:
        db_table = 'order_Goods'
        verbose_name = '订单商品管理表'
        verbose_name_plural = verbose_name