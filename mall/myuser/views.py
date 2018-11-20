import hashlib

from django.shortcuts import render, redirect

from myuser.forms import RegForm, LoginForm
from myuser.models import User


def member(request):  # 我的
    return render(request, 'index/member.html')


def step(request):  # 设置
    return render(request, 'member/step.html')


def login(request):  # 登录
    if request.method == "POST":
        # 获取对象
        data = request.POST
        # 获取from对象
        form = LoginForm(data)
        # 获取输入的值
        mobile = data.get('mobile')
        password = data.get('password')
        # 判断输入的参数是否为空
        if all([mobile, password]):
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
            if password != User.password:
                return redirect('user:login')
            # 保存session
            request.session['ID'] = user.id
            request.session['mobile'] = user.mobile
            # 登录成功返回个人中心
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


def reg(request):  # 注册
    #  判断是否为post保存数据
    if request.method == 'POST':
        data = request.POST
        #  创建form对象
        form = RegForm(data)
        mobile = data.get('mobile')
        password = data.get('password')
        # 将密码进行加密
        h = hashlib.md5(password.encode('utf-8'))
        password = h.hexdigest()
        # 保存在数据库
        if all([mobile, password]):
            User.objects.create(mobile=mobile, password=password)
            return redirect('user:login')
        else:
            # 提交错误信息
            context = {
                'errors': form.errors
            }
            return render(request, 'login/reg.html', context)
    return render(request, 'login/reg.html')


def records(request):  # 账户余额
    return render(request, 'member/records.html')


def integral(request):  # 积分
    return render(request, 'member/integral.html')


def yhq(request):   # 优惠券
    return render(request, 'member/yhq.html')


def collect(request):  # 我的收藏
    return render(request, 'member/collect.html')


def infor(request):  # 个人资料
    return render(request, 'member/infor.html')


def gladdress(request):  # 收货地址
    return render(request, 'member/gladdress.html')


def saftystep(request):  # 安全设置
    return render(request, 'member/saftystep.html')


def money(request):  # 我的钱包
    return render(request, 'member/money.html')


def job(request):  # 兼职
    return render(request, 'member/job.html')


def recommend(request):  # 推荐有奖
    return render(request, 'member/recommend.html')


def myrecommend(request):  # 我的推荐
    return render(request, 'member/myrecommend.html')