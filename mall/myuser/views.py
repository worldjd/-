import hashlib
import random
import re
from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from myuser.forms import RegForm, LoginForm, ForgetpasswordFoem, AddressForm, Editdress
from myuser.helper import verify_login_required, send_sms
from myuser.models import User, Gladdress


# 我的
@verify_login_required
def member(request):
    context = {
        'mobile': request.session['mobile'],
        'image': request.session['image'],
    }
    return render(request, 'index/member.html', context)


# 设置
def step(request):
    return render(request, 'member/step.html')


# 登录
def login(request):
    if request.method == "POST":
        # 获取对象
        data = request.POST
        # 获取from对象
        form = LoginForm(data)
        if form.is_valid():
            data1 = form.cleaned_data
            # 获取输入的值
            mobile = data1.get('mobile')
            password = data1.get('password')
            try:
                user = User.objects.get(mobile=mobile)
            except User.MultipleObjectsReturned:
                return redirect('user:login')
            except User.DoesNotExist:
                return redirect('user:login')
            # 验证密码
            # 对密码加密
            h = hashlib.md5(password.encode('utf-8'))
            password = h.hexdigest()
            # 判断密码
            if password != user.password:
                return redirect('user:login')
            # 保存session
            request.session['ID'] = user.id
            request.session['mobile'] = user.mobile
            request.session['image'] = user.image
            # 登录成功返回个人中心
            res = request.GET.get('next')
            if res:
                return redirect(res)
            else:
                return redirect('user:member')
        else:
            # 错误信息
            context = {
                'errors': form.errors
            }
            return render(request, 'login/login.html', context)
    else:
        # 回显
        return render(request, 'login/login.html')


# 短信地址
def send_mobile(request):
    if request.method == "POST":
        # 获取手机号码
        mobile = request.POST.get('mobile', '')
        # 验证手机号码格式是否错误
        mobile_re = re.compile('^1[3-9]\d{9}$')
        res = re.search(mobile_re, mobile)
        if res is None:
            return JsonResponse({'err': 1, 'mag': '手机号码格式错误!'})
        # 随机生成随机码
        random_code = "".join([str(random.randint(0, 9)) for _ in range(4)])
        # 保存在session中
        # 连接Redis
        cnn = get_redis_connection('default')
        cnn.set(mobile, random_code)
        # 设置过期时间
        cnn.expire(mobile, 120)
        # 发送短信
        # __business_id = uuid.uuid1()
        # params = "{\"code\":\"%s\",\"product\":\"阿里验证\"}" % random_code
        # send_sms(__business_id, mobile, "注册验证", "SMS_2245271", params)
        print(random_code)

        return JsonResponse({'err': 0})
    else:
        return JsonResponse({'err': 1, 'mag': '请求方式错误'})


# 注册
def reg(request):
    #  判断是否为post保存数据
    if request.method == 'POST':
        data = request.POST
        #  创建form对象
        form = RegForm(data)
        if form.is_valid():
            data1 = form.cleaned_data
            # 获取值
            mobile = data1.get('mobile')
            password = data1.get('password')
            # 将密码进行加密
            h = hashlib.md5(password.encode('utf-8'))
            password = h.hexdigest()
            # 保存在数据库
            User.objects.create(mobile=mobile, password=password)
            # 跳转到个人中心
            return redirect('user:login')
        else:
            # 提交错误信息
            context = {
                'errors': form.errors
            }
            return render(request, 'login/reg.html', context)
    return render(request, 'login/reg.html')


# 忘记密码
def forgetpassword(request):
    if request.method == "POST":
        data = request.POST
        form = ForgetpasswordFoem(data)
        if form.is_valid():
            data1 = form.cleaned_data
            mobile = data1.get('mobile')
            if mobile:
                try:
                    password = data1.get('password')
                    # 对密码进行加密
                    h = hashlib.md5(password.encode('utf-8'))
                    password = h.hexdigest()
                except:
                    return redirect('user:forgetpassword')
                User.objects.filter(mobile=mobile).update(password=password)
                return redirect('user:login')
            else:
                return redirect('user:forgetpassword')
        else:
            context = {
                'errors': form.errors
            }
            return render(request, 'login/forgetpassword.html', context)
    return render(request, 'login/forgetpassword.html')


# 账户余额
def records(request):
    return render(request, 'member/records.html')


# 积分
def integral(request):
    return render(request, 'member/integral.html')


# 优惠券
def yhq(request):
    return render(request, 'member/yhq.html')


# 我的收藏
def collect(request):
    return render(request, 'member/collect.html')


# 个人资料
@verify_login_required
def infor(request):
    if request.method == "POST":
        data = request.POST
        # 获取用户输入的值
        id = request.session['ID']
        username = data.get('username')
        birthday = data.get('birthday')
        home = data.get('home')
        school = data.get('school')
        sex = data.get('sex')
        # 根据session保存的id来传入到数据库
        User.objects.filter(pk=id).update(username=username, school=school, home=home, sex=sex, birthday=birthday)
        return redirect('user:infor')
    # 根据session里的id来获取对象
    id1 = request.session['ID']
    res = User.objects.get(pk=id1)
    if res.birthday:
        res.birthday = res.birthday.strftime("%Y-%m-%d")
    context = {
        'user': res,
        'birthday': res.birthday,
    }
    return render(request, 'member/infor.html', context)


# 上传头像
def UploadImg(request):
    try:
        user = User.objects.get(pk=request.session.get('ID'))
        user.image = request.FILES['file']
        user.save()
        request.session['image'] = user.image
        return redirect('user:infor')
    except MultiValueDictKeyError:
        return redirect('user:infor')


# 收货地址
@verify_login_required
def gladdress(request):
    # 显示数据在页面上
    # 获取对象
    user_id = request.session.get('ID')
    glad = Gladdress.objects.filter(user_id=user_id, isDelete=False).order_by('-isDefault')
    context = {
        'glad': glad
    }
    return render(request, 'member/gladdress.html', context)


# 添加地址
@verify_login_required
def address(request):
    if request.method == "POST":
        # 获取参数
        data = request.POST.dict()
        data['user_id'] = request.session.get("ID")
        # 创建form对象
        form = AddressForm(data)
        if form.is_valid():
            # 获取过滤后的数据
            data1 = form.cleaned_data
            data1['user_id'] = request.session.get("ID")
            Gladdress.objects.create(**data1)
            return redirect('user:gladdress')
        else:
            # 回显错误信息
            context = {
                'form': form
            }
            return render(request, 'member/address.html', context)
    return render(request, 'member/address.html')


# 修改地址
@verify_login_required
def editdress(request, id):
    if request.method == "GET":
        user_id = request.session.get('ID')
        try:
            glad = Gladdress.objects.get(user_id=user_id, id=id)
        except Gladdress.DoesNotExist:
            return redirect('user:address')
        context = {
            'glad': glad,
        }
        return render(request, 'member/editdress.html', context)
    if request.method == "POST":
        # 获取参数
        data = request.POST.dict()
        data['user_id'] = request.session.get("ID")
        form = Editdress(data)
        if form.is_valid():
            data1 = form.cleaned_data
            user_id = data.get('user_id')
            Gladdress.objects.filter(user_id=user_id, id=id).update(**data1)
            return redirect('user:gladdress')
        else:
            context = {
                'form': form,
                'glad': data
            }
            return render(request, 'member/editdress.html', context)


# 删除地址
@verify_login_required
def deldress(request):
    if request.method == "POST":
        # 必须登录才能删除
        user_id = request.session.get("ID")
        id = request.POST.get('id')
        if user_id is None:
            return JsonResponse({'code': 1, 'err': '请登录!'})
        # 删除数据
        Gladdress.objects.filter(user_id=user_id, id=id).update(isDelete=True)
        # 返回数据
        return JsonResponse({'code': 0, 'err': '删除成功'})
    else:
        return JsonResponse({'code': 2, 'err': '请求参数错误!'})


# 设置默认
@verify_login_required
def setdefault(request):
    if request.method == "POST":
        # 获取数据
        id = request.POST.get('id')
        user_id = request.session.get('ID')
        # 判断是否登录
        if user_id is None:
            return JsonResponse({'code': 1, 'err': '请登录!'})
        # 处理数据
        default = Gladdress.objects.filter(user_id=user_id, isDelete=False).update(isDefault=False)
        if default:
            Gladdress.objects.filter(user_id=user_id, id=id).update(isDefault=True)
            return JsonResponse({'code': 0, 'err': '设置成功!'})
        return JsonResponse({'code': 2, 'err': '设置失败!'})
    return JsonResponse({'code': 3, 'err': '请求参数错误!'})


# 安全设置
@verify_login_required
def saftystep(request):
    return render(request, 'member/saftystep.html')


# 我的钱包
def money(request):
    return render(request, 'member/money.html')


# 兼职
def job(request):
    return render(request, 'member/job.html')


# 推荐有奖
def recommend(request):
    return render(request, 'member/recommend.html')


# 我的推荐
def myrecommend(request):
    return render(request, 'member/myrecommend.html')




