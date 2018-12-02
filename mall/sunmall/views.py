from django.shortcuts import render


def message(request):  # 动态
    return render(request, 'index/message.html')