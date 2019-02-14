from django.conf import settings
import hashlib

from django.http import JsonResponse
from django.shortcuts import redirect


# 加密  用 setting  中的   SECRET_KEY  加盐
def set_password(password):
    strs = '{}{}'.format(password, settings.SECRET_KEY)
    h = hashlib.md5(strs.encode('utf-8'))
    return h.hexdigest()


def json_msg(code,msg=None,data=None):
    '''
    封装Json消息
    code 0 为正确
  其他为错误{"error": 1, "msg": "没有登录,请登录!"}
    '''
    return {'code':code,"error": 1,'msg':msg,'data':data}


# 判断登录的装饰器
def judgeSignIn(func):
    # 新函数
    def verify_login(request, *args, **kwargs):
        # 验证session中是否有登录标识
        if request.session.get("id") is None:
            # 将上个请求地址保存到session
            referer = request.META.get('HTTP_REFERER', None)
            if referer:
                request.session['referer'] = referer
            # 判断是否为ajax请求
            if request.is_ajax():
                return JsonResponse(json_msg(1, '未登录'))
            else:
                # 跳转到登录
                return redirect('users:login')
        else:
            # 调用原函数
            return func(request, *args, **kwargs)

    # 返回新函数
    return verify_login


# 获取购物车的key
def get_car_key(user_id):
    return "car_{}".format(user_id)