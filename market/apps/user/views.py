from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm, ForgetPasswordModelForm, InforForm, ReviseModelForm
from user.helper import set_password, login, check_login
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
            user.password = set_password(cleaned_data.get('password2'))
            # 保存到数据库
            user.save()
            # 合成html
            # 自动跳转到登录页面
            return redirect('user:登录')

        else:
            context = {'errors': register_form.errors}
            return render(request, 'user/reg.html', context=context)


# 完成登录
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
            # user = login_form.cleaned_data['user']
            # login(request, user)
            # 合成响应, 跳转到个人中心
            return redirect('user:个人中心')
        else:
            context = {'errors': login_form.errors}
            return render(request, 'user/login.html', context=context)


def forget_password(request):
    if request.method == 'GET':
        return render(request, 'user/forgetpassword.html')
    else:
        data = request.POST
        form = ForgetPasswordModelForm(data)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned_data = form.cleaned_data
            phone = cleaned_data.get('phone')
            # user = Register()
            password = set_password(cleaned_data.get('pwd1'))

            # 保存到数据库
            Register.objects.filter(phone=phone).update(password=password)
            # 合成html
            # 自动跳转到登录页面
            return redirect('user:登录')

        else:
            context = {'errors': form.errors}
            return render(request, 'user/forgetpassword.html', context=context)


# @check_login
def revise(request):
    if request.method == 'GET':
        return render(request, 'user/password.html')
    else:
        data = request.POST
        form = ReviseModelForm(data)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned_data = form.cleaned_data
            phone = cleaned_data.get('phone')
            password = set_password(cleaned_data.get('pwd1'))
            # 保存到数据库
            Register.objects.filter(phone=phone).update(password=password)
            # 合成html
            # 自动跳转到登录页面
            return redirect('user:登录')

        else:
            context = {'errors': form.errors}
            return render(request, 'user/password.html', context=context)


class InforView(View):
    """个人资料"""

    def get(self, request):
        return render(request, 'user/infor.html')

    def post(self, request):
        # 获取数据
        data = request.POST
        form = InforForm(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Register.objects.create(**cleaned_data)

        else:
            context = {'errors': form.errors}
            return render(request, 'user/infor.html', context=context)


# class MemberView(VerifyLoginView):
class MemberView(View):
    """个人中心"""

    # @method_decorator(check_login)
    def get(self, request):
        return render(request, 'user/member.html')

    # @method_decorator(check_login)
    def post(self, request):
        pass

    # @method_decorator(check_login)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)
