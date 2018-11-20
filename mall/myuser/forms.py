from django import forms
from django.core import validators


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

    def clean(self):
        data = self.cleaned_data
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError({'password2': '密码不一致,请重新输入'})
        else:
            return data


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
                               max_length=32,
                               min_length=5,
                               error_messages={
                                   'required': '密码不能为空',
                                   'max_lenght': '密码最大不能超过32位',
                                   'min_lenght': '密码最小不能小于5位',
                               }
                               )