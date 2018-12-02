from django import forms
from django.core import validators
import hashlib

from myuser.models import User, Gladdress
from django_redis import get_redis_connection


class RegForm(forms.Form):
    mobile = forms.CharField(required=True,
                             validators=[
                                 validators.RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误")
                             ],
                             error_messages={
                                 'required': "账号或手机号不能为空",
                             }
                             )
    password = forms.CharField(required=True,
                               max_length=32,
                               min_length=5,
                               error_messages={
                                   'required': '密码不能为空',
                                   'max_lenght': '密码最大不能超过32位',
                                   'min_lenght': '密码最小不能小于5位',
                               }
                               )
    password2 = forms.CharField(required=True,
                                max_length=32,
                                min_length=5,
                                error_messages={
                                   'required': '密码不能为空',
                                   'max_lenght': '密码最大不能超过32位',
                                   'min_lenght': '密码最小不能小于5位',
                               }
                               )
    code = forms.CharField(error_messages={'required': '验证码不能为空'})

    def clean(self):  # 验证两次密码是否一致
        data = self.cleaned_data
        if data.get('password') and data.get('password2') and data.get('password') != data.get('password2'):
            raise forms.ValidationError({'password2': '密码不一致,请重新输入'})
        else:
            return data

    def clean_mobile(self):  # 验证手机号是否注册
        mobile = self.cleaned_data.get('mobile')
        res = User.objects.filter(mobile=mobile).exists()
        if res:
            raise forms.ValidationError('手机号已被注册!')
        else:
            return mobile

    # 验证码验证
    def clean_code(self):
        # 获取输入的手机号码
        mobile = self.cleaned_data.get('mobile')
        # 获取验证码
        code = self.cleaned_data.get('code')
        # 创建连接对象
        cnn = get_redis_connection('default')
        if mobile:
            # 从数据库获取验证码
            code1 = cnn.get(mobile)
            # 对验证码转码
            code1 = code1.decode('utf-8')
            # 判断验证码是否存在
            if code1 is None:
                raise forms.ValidationError('验证码过期或错误!')
            if code != code1:
                raise forms.ValidationError('验证码错误!')
            return code
        else:
            return code


class LoginForm(forms.Form):
    mobile = forms.CharField(required=True,
                             validators=[
                                 validators.RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误")
                             ],
                             error_messages={
                                 'required': "账号或手机号不能为空",
                             }
                             )
    password = forms.CharField(required=True,
                               error_messages={
                                   'required': '密码不能为空',
                               }
                               )

    def clean(self):
        # 获取输入的密码
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        mobile = self.cleaned_data.get('mobile')
        # 对密码进行加密
        try:
            h = hashlib.md5(password.encode('utf-8'))
            password = h.hexdigest()
        except:
            raise forms.ValidationError('密码不能为空!')
        # 从数据库中获取密码
        try:
            res = User.objects.get(mobile=mobile)
            if res:
                password1 = res.password
                if password != password1:
                    raise forms.ValidationError({'password': '密码错误'})
                else:
                    return data
            else:
                raise forms.ValidationError({'mobile': '手机号码不存在!'})
        except User.DoesNotExist:
            raise forms.ValidationError({'mobile': '手机号码不存在!'})


class ForgetpasswordFoem(forms.Form):
    mobile = forms.CharField(required=True,
                             validators=[
                                 validators.RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误")
                             ],
                             error_messages={
                                 'required': "账号或手机号不能为空",
                             }
                             )
    password = forms.CharField(required=True,
                               max_length=32,
                               min_length=5,
                               error_messages={
                                   'required': '密码不能为空',
                                   'max_lenght': '密码最大不能超过32位',
                                   'min_lenght': '密码最小不能小于5位',
                               }
                               )
    password2 = forms.CharField(required=True,
                                max_length=32,
                                min_length=5,
                                error_messages={
                                    'required': '密码不能为空',
                                    'max_lenght': '密码最大不能超过32位',
                                    'min_lenght': '密码最小不能小于5位',
                                }
                                )
    cod = forms.CharField(error_messages={'required': '验证码不能为空'})

    def clean(self):  # 验证两次密码是否一致
        data = self.cleaned_data
        if data.get('password') and data.get('password2') and data.get('password') != data.get('password2'):
            raise forms.ValidationError({'password2': '密码不一致,请重新输入'})
        else:
            return data

    # 验证手机号码是否注册
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        res = User.objects.filter(mobile=mobile).exists()
        if res is False:
            raise forms.ValidationError('手机号未注册')
        return mobile

    # 验证码验证
    def clean_cod(self):
        # 获取输入的手机号码
        mobile = self.cleaned_data.get('mobile')
        # 获取验证码
        cod = self.cleaned_data.get('cod')
        # 创建连接对象
        cnn = get_redis_connection('default')
        if mobile:
            # 从数据库获取验证码
            code1 = cnn.get(mobile)
            # 对验证码转码
            code1 = code1.decode('utf-8')
            # 判断验证码是否存在
            if code1 is None:
                raise forms.ValidationError('验证码过期或错误!')
            if cod != code1:
                raise forms.ValidationError('验证码错误!')
            return cod
        else:
            return cod


# 添加地址
class AddressForm(forms.Form):
    hcity = forms.CharField()
    hproper = forms.CharField()
    harea = forms.CharField(error_messages={'required': '省市区必填!'})
    detail = forms.CharField(error_messages={'required': '详细地址必填!'})
    username = forms.CharField(error_messages={'required': '收货人必填!'})
    phone = forms.CharField(error_messages={'required': '联系电话必填!'},
                            validators=[validators.RegexValidator(r'^1[3-9]\d{9}$', '联系电话格式错误')]
                            )
    isDefault = forms.BooleanField()

    def clean(self):
        # 获取用户的id
        user_id = self.data.get('user_id')
        count = Gladdress.objects.filter(user_id=user_id, isDelete=False).count()
        if count > 6:
            raise forms.ValidationError('收货地址只能有6个!')

        # 设置默认是否是默认地址
        isDefault = self.cleaned_data.get('isDefault')
        # 判断是否为True,如果是就将其他的True改为False
        if isDefault:
            Gladdress.objects.filter(user_id=user_id).update(isDefault=False)
        return self.cleaned_data


class Editdress(forms.Form):
    hcity = forms.CharField()
    hproper = forms.CharField()
    harea = forms.CharField(error_messages={'required': '省市区必填!'})
    detail = forms.CharField(error_messages={'required': '详细地址必填!'})
    username = forms.CharField(error_messages={'required': '收货人必填!'})
    phone = forms.CharField(error_messages={'required': '联系电话必填!'},
                            validators=[validators.RegexValidator(r'^1[3-9]\d{9}$', '联系电话格式错误')]
                            )
    isDefault = forms.BooleanField()

    def clean(self):
        # 设置默认是否是默认地址
        user_id = self.data.get('user_id')
        isDefault = self.cleaned_data.get('isDefault')
        # 判断是否为True,如果是就将其他的True改为False
        if isDefault:
            Gladdress.objects.filter(user_id=user_id).update(isDefault=False)
        else:
            return self.cleaned_data