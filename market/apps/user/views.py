from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from user.forms import RegisterModelForm, LoginModelForm
from user.helper import set_password, login
from user.models import Register


def register(request):
    # 判断登录方式
    if request.method == 'GET':
        return render(request, 'user/reg.html')
    else:
        # 获取数据
        register_form = RegisterModelForm(request.POST)
        # 判断数据是否合法
        if register_form.is_valid():
            # 获取清洗后的数据
            cleaned_data = register_form.cleaned_data
            user = Register()
            user.phone = cleaned_data.get('phone')
            user.password = set_password(cleaned_data.get('password1'))
            # 保存到数据库
            user.save()
            # 合成html
            # 自动跳转到登录页面
            return redirect('user:登录')

        else:
            context = {'errors': register_form.errors}
            return render(request, 'user/reg.html', context=context)


class LoginView(View):

    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 获取数据
        data = request.POST
        # 验证数据合法性
        login_form = LoginModelForm(data)
        if login_form.is_valid():
            # 操作数据库
            # 保存登录标识到session中
            user = login_form.cleaned_data['user']
            login(request, user)
            # 合成响应, 跳转到个人中心
            return redirect('user:个人中心')
        else:
            context = {'errors': login_form.errors}
            return render(request, 'user/login.html', context=context)


class MemberView(View):
    def get(self, request):
        return render(request, 'user/member.html')
