import uuid
import random

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from django.views import View
import re

from django_redis import get_redis_connection

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm, ForgetPasswordModelForm, ReviseModelForm, \
    MemberModelForm, AddressAddForm
from user.helper import set_password, login, check_login, send_sms
from user.models import Register, UserAddress


# 发送短消验证码
class SendMsm(View):

    def post(self, request):
        # 1, 接收参数
        phone = request.POST.get('phone', '')
        rs = re.search('^1[3-9]\d{9}$', phone)
        # 判断参数合法性
        if rs is None:
            return JsonResponse({'error': 1, 'errmsg': '电话号码格式错误!'})
        # 2. 处理数据

        # 模拟,最后接入运营商

        # 1. 生成随机验证码字符串
        random_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        print(random_code)

        # 2. 保存验证码到redis中
        # 获取连接
        r = get_redis_connection()
        # 保存手机号码对应的验证码
        r.set(phone, random_code)
        r.expire(phone, 60)  # 设置60秒后过期

        # 首先获取当前手机号码的发送次数
        key_times = "{}_times".format(phone)
        now_times = r.get(key_times)
        # 从redis获取的二进制,需要转换
        if now_times is None or int(now_times) < 6:
            # 保存手机发送验证码的次数, 不能超过6次
            r.incr(key_times)
            # 设置一个过期时间
            r.expire(key_times, 360)
        else:
            # 返回,告知用户发送次数过多
            return JsonResponse({"error": 1, "errmsg": "发送次数过多"})

        # 3. 接入运营商
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"超市\"}" % random_code
        rs = send_sms(__business_id, phone, "注册验证", "SMS_2245271", params)
        print(rs.decode('utf-8'))
        # 3. 合成响应
        return JsonResponse({'error': 0})


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
            user = login_form.cleaned_data['user']
            login(request, user)
            referer = request.session.get('referer')
            if referer:
                #     跳转回去
                del request.session['referer']
                return redirect(referer)
            else:
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


@check_login
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


"""个人资料"""


class InforView(VerifyLoginView):

    def get(self, request):
        id = request.session.get('ID')
        user = Register.objects.get(pk=id)
        context = {'user': user}
        return render(request, 'user/infor.html', context=context)

    def post(self, request):
        # 获取数据
        data = request.POST
        head = request.FILES.get('logo')
        id = request.session.get('ID')
        form = MemberModelForm(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nickname = data.get('nickname')
            gender = data.get('gender')
            birthday = cleaned_data.get('birthday')
            school = data.get('school')
            hometown = data.get('hometown')

            phone = request.session.get('phone')

            # 保存到数据库
            Register.objects.filter(phone=phone).update(nickname=nickname,
                                                        gender=gender,
                                                        birthday=birthday,
                                                        school=school,
                                                        hometown=hometown)

            user = Register.objects.get(pk=id)
            if head is not None:
                user.logo = head
                user.save()
            login(request, user)
            return redirect('user:个人中心')

        else:
            context = {'errors': form.errors}
            return render(request, 'user/infor.html', context=context)


# 个人中心


class MemberView(VerifyLoginView):

    def get(self, request):
        id = request.session.get('ID')
        user = Register.objects.get(pk=id)
        context = {'user': user}
        return render(request, 'user/member.html', context=context)

    def post(self, request):
        pass


class AddressView(VerifyLoginView):
    def get(self, request):
        return render(request, 'user/address.html')

    def post(self, request):
        # 获取数据
        # 强制转化为字典
        data = request.POST.dict()
        data['use_id'] = request.session.get('ID')
        form = AddressAddForm(data)
        if form.is_valid():
            form.instance.user = Register.objects.get(pk=data['use_id'])
            form.save()
            return redirect('user:地址列表')
        else:
            return HttpResponse('失败')


#  收货地址列表页
class Addresslist(VerifyLoginView):

    def get(self, request):
        # 获取收货地址,所有的, 当前用户的
        user_id = request.session.get("ID")
        # 查询
        addresses = UserAddress.objects.filter(user_id=user_id, is_delete=False).order_by("-isDefault")

        # 渲染数据
        context = {
            'addresses': addresses
        }
        return render(request, 'user/gladdress.html', context)


#  收货地址添加页
class AddressAddView(VerifyLoginView):

    def get(self, request):
        return render(request, 'user/address.html')

    def post(self, request):
        # 接收参数
        data = request.POST.dict()
        data['user_id'] = request.session.get("ID")
        # 验证参数
        form = AddressAddForm(data)
        # 处理数据
        if form.is_valid():
            form.instance.user_id = request.session.get("ID")
            # modelform对象上有个save()方法,直接就能保存数据
            form.save()
            # 返回响应 返回收货地址列表页面
            return redirect("user:address")
        else:
            context = {
                "form": form,
            }
            return render(request, "user/address.html", context)


# 收货地址修改页
class AddressEditView(VerifyLoginView):

    def get(self, request, id):
        # 查询当前用户的 当前id的收货地址
        user_id = request.session.get("ID")
        # 查询
        try:
            address = UserAddress.objects.get(user_id=user_id, pk=id)
        except UserAddress.DoesNotExist:
            return redirect("user:address")

        # 渲染到页面
        context = {
            "address": address
        }

        return render(request, 'user/address_edit.html', context)

    def post(self, request, id):
        # 接收数据
        data = request.POST.dict()
        # 验证数据
        user_id = request.session.get("ID")
        data['user_id'] = user_id
        form = AddressAddForm(data)
        # 处理数据
        if form.is_valid():
            # 更新 根据主键id
            cleaned_data = form.cleaned_data
            id = data.get('id')
            UserAddress.objects.filter(user_id=user_id, pk=id).update(**cleaned_data)

            # 跳转
            return redirect("user:address")
        else:
            # 返回响应
            context = {
                "form": form,
                "address": data
            }
            return render(request, 'user/address_edit.html', context)


# 删除收货地址
def delAddress(request):
    if request.method == "POST":
        # 必须登陆
        user_id = request.session.get('ID')
        id = request.POST.get("id")
        if user_id is None:
            return JsonResponse({"code": 1, "errmsg": "没有登陆!"})
        # 删除的时候最好 用户的id条件加上
        UserAddress.objects.filter(user_id=user_id, pk=id).update(isDelete=True)
        # 返回结果
        return JsonResponse({"code": 0})
    else:
        return JsonResponse({"code": 2, "errmsg": "请求方式错误"})
