from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings


# 分类商品
class Shop(models.Model):
    shop_username = models.CharField(max_length=50, verbose_name='分类名')
    shop_describe = models.CharField(max_length=255, null=True, blank=True, verbose_name='分类介绍')
    shop_add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    shop_revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    shop_is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.shop_username

    class Meta:
        verbose_name = '分类商品'
        verbose_name_plural = verbose_name


# 商品单位表
class Unit(models.Model):
    unit_name = models.CharField(max_length=50, verbose_name='单位名')
    unit_add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    unit_revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    unit_is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = '商品单位表'
        verbose_name_plural = verbose_name


# 商品spu表
class Spu(models.Model):
    spu_name = models.CharField(max_length=50,verbose_name='名称')
    spu_details = RichTextUploadingField(verbose_name='详情')

    def __str__(self):
        return self.spu_name

    class Meta:
        verbose_name = '商品spu表'
        verbose_name_plural = verbose_name


# 商品sku表
class Sku(models.Model):
    sku_trade_name = models.CharField(max_length=20, verbose_name='商品名')
    sku_introduce = models.CharField(max_length=255, null=True, blank=True, verbose_name='简介')
    sku_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='价格')
    sku_unit_id = models.ForeignKey(to='Unit', verbose_name='单位id')
    sku_stock = models.IntegerField(default=0, verbose_name='库存')
    sku_Sales_volume = models.IntegerField(verbose_name='销量',default=0)
    sku_logo_address = models.ImageField(upload_to='shop_image/%Y%m/%d', verbose_name='logo地址')
    sku_is_upper = models.BooleanField(default=True, verbose_name='是否上架')
    sku_shop_id = models.ForeignKey(to='Shop', verbose_name='商品分类id')
    sku_spu_id = models.ForeignKey(to="Spu", verbose_name='商品spu_id')
    sku_add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    sku_revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    sku_is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def show_logo(self):
        return "<img style='width:80px' src= '{}{}'/>".format(settings.MEDIA_URL, self.sku_logo_address)

    show_logo.allow_tags = True
    show_logo.short_description = "LOGO"

    def __str__(self):
        return self.sku_trade_name

    class Meta:
        verbose_name = '商品sku表'
        verbose_name_plural = verbose_name


# 商品相册
class ShopImage(models.Model):
    shopImage_image = models.ImageField(upload_to='shop_image/%Y%m/%d', verbose_name='商品图片')
    shopImage_Sku_id = models.ForeignKey(to='Sku', verbose_name='商品id')
    shopImage_add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    shopImage_revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    shopImage_is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '商品相册'
        verbose_name_plural = verbose_name


# 首页轮播图
class Banner(models.Model):
    banner_name = models.CharField(max_length=50, verbose_name='名称')
    banner_sku_id = models.ForeignKey(to='Sku', verbose_name='商品id')
    banner_image = models.ImageField(upload_to='shop_image/%Y%m/%d', verbose_name='图片')
    banner_order = models.IntegerField(default=0, verbose_name='排序')
    banner_add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    banner_revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    banner_is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.banner_name

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name


# 首页活动表
class Activity(models.Model):
    activity_name = models.CharField(max_length=50, verbose_name='名称')
    activity_image = models.ImageField(upload_to='shop_image/%Y%m/%d', verbose_name='图片')
    activity_url = models.URLField(verbose_name='地址')
    Activity_add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    Activity_revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    Activity_is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.activity_name

    class Meta:
        verbose_name = '首页活动表'
        verbose_name_plural = verbose_name


# 活动专区
class ActivityArea(models.Model):
    ActivityArea_name = models.CharField(max_length=50, verbose_name='名称')
    ActivityArea_describe = models.CharField(max_length=255, verbose_name='描述')
    ActivityArea_order = models.IntegerField(default=0, verbose_name='排序')
    ActivityArea_add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    ActivityArea_revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    ActivityArea_is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.ActivityArea_name

    class Meta:
        verbose_name = '活动专区'
        verbose_name_plural = verbose_name


# 专区活动商品
class ActivityShop(models.Model):
    ActivityShop_ActivityArea_id = models.ForeignKey(to='ActivityArea', verbose_name='活动专区id')
    ActivityShop_sku_id = models.ForeignKey(to='Sku', verbose_name='商品id')
    ActivityShop_add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    ActivityShop_revise_time = models.DateField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '专区活动商品'
        verbose_name_plural = verbose_name


