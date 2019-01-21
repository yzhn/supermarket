import hashlib

from django.shortcuts import redirect

from market.settings import SECRET_KEY


def set_password(password):
    # 循环加密 + 加盐
    for _ in range(1000):
        pass_str = "{}{}".format(password, SECRET_KEY)
        h = hashlib.md5(pass_str.encode('utf-8'))
        password = h.hexdigest()

    # 返回密码
    return password


# 保存session的方法
def login(request, user):
    request.session['ID'] = user.pk
    request.session['phone'] = user.phone
    # 关闭浏览器就消失
    request.session.set_expiry(0)


def check_login(func):  # 登录验证装饰器
    # 新函数
    def verify_login(request, *args, **kwargs):
        # 验证session中是否有登录标识
        if request.session.get("ID") is None:
            # 跳转到登录
            return redirect('user:登录')
        else:
            # 调用原函数
            return func(request, *args, **kwargs)

    # 返回新函数
    return verify_login
