from django.core.validators import RegexValidator
from django.db import models


# 用户表
class User(models.Model):
    sex_choices = (
        (1, "男"),
        (2, "女"),
        (3, "保密"),
    )
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=20, null=True, blank=True)
    sex = models.SmallIntegerField(choices=sex_choices, default=3, blank=True)
    school = models.CharField(max_length=20, null=True, blank=True)
    home = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    revise_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    image = models.ImageField(upload_to='shop/%Y%m/%d', default='infortx.png', verbose_name='头像LOGO')

    def __str__(self):
        return self.mobile


# 收货地址
class Gladdress(models.Model):
    hcity = models.CharField(max_length=50, null=True, blank=True, verbose_name='省')
    hproper = models.CharField(max_length=50, null=True, blank=True, verbose_name='市')
    harea = models.CharField(max_length=50, verbose_name='县或区')
    detail = models.CharField(max_length=255, verbose_name='详细地址')
    username = models.CharField(max_length=50, verbose_name='收货人')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    user = models.ForeignKey(to=User, verbose_name='用户id')
    isDefault = models.BooleanField(default=False, verbose_name='是否为默认地址')
    add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')
    revise_time = models.DateField(auto_now=True, verbose_name='修改时间')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.username